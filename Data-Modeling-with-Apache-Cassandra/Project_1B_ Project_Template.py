#!/usr/bin/env python
# coding: utf-8

# # Part I. ETL Pipeline for Pre-Processing the Files

# ## PLEASE RUN THE FOLLOWING CODE FOR PRE-PROCESSING THE FILES

# #### Import Python packages 

# In[1]:


# Import Python packages 
import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv


# #### Creating list of filepaths to process original event csv data files

# In[2]:


# checking your current working directory
print(os.getcwd())

# Get your current folder and subfolder event data
filepath = os.getcwd() + '/event_data'

# Create a for loop to create a list of files and collect each filepath
for root, dirs, files in os.walk(filepath):
    
# join the file path and roots with the subdirectories using glob
    file_path_list = glob.glob(os.path.join(root,'*'))
    print(file_path_list)


# #### Processing the files to create the data file csv that will be used for Apache Casssandra tables

# In[3]:


# initiating an empty list of rows that will be generated from each file
full_data_rows_list = [] 
    
# for every filepath in the file path list 
for f in file_path_list:

# reading csv file 
    with open(f, 'r', encoding = 'utf8', newline='') as csvfile: 
        # creating a csv reader object 
        csvreader = csv.reader(csvfile) 
        next(csvreader)
        
 # extracting each data row one by one and append it        
        for line in csvreader:
            #print(line)
            full_data_rows_list.append(line) 
            
# uncomment the code below if you would like to get total number of rows 
print(len(full_data_rows_list))
# uncomment the code below if you would like to check to see what the list of event data rows will look like
#print(full_data_rows_list)

# creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
# Apache Cassandra tables
csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

with open('event_datafile_new.csv', 'w', encoding = 'utf8', newline='') as f:
    writer = csv.writer(f, dialect='myDialect')
    writer.writerow(['artist','firstName','gender','itemInSession','lastName','length',                'level','location','sessionId','song','userId'])
    for row in full_data_rows_list:
        if (row[0] == ''):
            continue
        writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))


# In[4]:


# check the number of rows in your csv file
with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
    print(sum(1 for line in f))


# In[5]:


# Let print the columns names of our data.

for line in list(pd.read_csv('event_datafile_new.csv').columns):
    print(line)


# # Part II. Complete the Apache Cassandra coding portion of your project. 
# 
# ## Now you are ready to work with the CSV file titled <font color=red>event_datafile_new.csv</font>, located within the Workspace directory.  The event_datafile_new.csv contains the following columns: 
# - artist 
# - firstName of user
# - gender of user
# - item number in session
# - last name of user
# - length of the song
# - level (paid or free song)
# - location of the user
# - sessionId
# - song title
# - userId
# 
# The image below is a screenshot of what the denormalized data should appear like in the <font color=red>**event_datafile_new.csv**</font> after the code above is run:<br>
# 
# <img src="images/image_event_datafile_new.jpg">

# ## Begin writing your Apache Cassandra code in the cells below

# #### Creating a Cluster

# In[6]:


# This should make a connection to a Cassandra instance your local machine 
# (127.0.0.1)

from cassandra.cluster import Cluster
cluster = Cluster()

# To establish connection and begin executing queries, need a session
session = cluster.connect()


# #### Create Keyspace

# In[7]:


# TO-DO: Create a Keyspace 
# Let name our cluster udacity

try:
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS udacity 
    WITH REPLICATION = 
    { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"""
)

except Exception as e:
    print(e)


# #### Set Keyspace

# In[8]:


# TO-DO: Set KEYSPACE to the keyspace specified above

try:
    session.set_keyspace('udacity')
except Exception as e:
    print(e)


# ### Now we need to create tables to run the following queries. Remember, with Apache Cassandra you model the database tables on the queries you want to run.

# ## Create queries to ask the following three questions of the data
# 
# ### 1. Give me the artist, song title and song's length in the music app history that was heard during  sessionId = 338, and itemInSession  = 4
# 
# 
# ### 2. Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
#     
# 
# ### 3. Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
# 
# 
# 

# ## Query 1
# 
# > Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4
# 
# Let's call our new table song_details.
# 
# In CQL, to answer this question we will need to obtain (select) the artist name, song name, and song length from out table, and we will need to filter by sessionId and itemInSession. Here's what we obtain:
# 
# ````sql
# SELECT artist, song, length FROM session_songs WHERE sessionId = 338 AND itemInSession = 4
# ````
# 
# * Our **primary key** will consist of two items: 
#     * Partition key name **sessionId**, 
#     * Clustering key identify by **itemInSession** so that we can filter by this attributes later on.
# * Other"s columns of our table will be: sessionId, itemInSession, artist, song and length.

# In[17]:


## TO-DO: Query 1:  Give me the artist, song title and song's length in the music app history that was heard during \
## sessionId = 338, and itemInSession = 4


create_song_details = "CREATE TABLE IF NOT EXISTS song_details"
create_song_details = create_song_details + (""" (sessionId INT, itemInSession INT, artist TEXT, song TEXT,
                                        length FLOAT, PRIMARY KEY (sessionId, itemInSession))""")
try:
    session.execute(create_song_details)
except Exception as e:
    print(e)
    
select_song_details = """ 
                    SELECT  artist, 
                            song  , 
                            length 
                    FROM  song_details
                    WHERE sessionId = %s 
                    AND   itemInSession = %s 
                """


# In[18]:


# We have provided part of the code to set up the CSV file. Please complete the Apache Cassandra code below#
file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
## TO-DO: Assign the INSERT statements into the `query` variable
        query = "INSERT INTO song_details(sessionId, itemInSession, artist, song, length)"
        query = query + "VALUES (%s, %s, %s, %s, %s)"
        ## TO-DO: Assign which column element should be assigned for each column in the INSERT statement.
        artist, firstName, gender, itemInSession, lastName, length, level, location, sessionId, song, userId = line
        session.execute(query, (int(sessionId), int(itemInSession), artist, song, float(length)))


# #### Do a SELECT to verify that the data have been inserted into each table

# In[19]:


## TO-DO: Add in the SELECT statement to verify the data was entered into the table
try:
    rows = session.execute(select_song_details, (338, 4))
except Exception as e:
    print(e)
    
for row in rows:
    print("Artist: "+row.artist, "\nSong Title: "+row.song, "\nSong Length: "+str(row.length))


# ### COPY AND REPEAT THE ABOVE THREE CELLS FOR EACH OF THE THREE QUESTIONS

# ## Query 2
# 
# > Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
# 
# Let's call our new table song_users.
# 
# In CQL, to answer this question we will need to obtain (select) the artist name, song name, and song length from out table, and we will need to filter by sessionId and itemInSession. Here's what we obtain:
# 
# ````sql
# SELECT artist, song, firstName, lastName FROM song_users WHERE userId = 10 AND sessionId = 182
# ````
# 
# * Our **primary key** will consist of two items: 
#     * Composite partition key name **(userId, sessionId)**, 
#     * Clustering key identify by **itemInSession** so that we can filter by this attributes later on.

# In[31]:


## TO-DO: Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name)\
## for userid = 10, sessionid = 182

create_song_users = "CREATE TABLE IF NOT EXISTS song_users"
create_song_users = create_song_users + (""" (userId INT, sessionId INT, itemInSession INT, 
                                        artist TEXT, song TEXT, firstName TEXT, 
                                        lastName TEXT, PRIMARY KEY ((userId, sessionId), itemInSession))""")
try:
    session.execute(create_song_users)
except Exception as e:
    print(e)
    
select_song_users = """ SELECT  artist   , 
                                song     , 
                                firstName, 
                                lastName 
                        FROM song_users
                        WHERE userId = %s
                        AND   sessionId = %s 
                    """                


# In[32]:


with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
        query = "INSERT INTO song_users (userId, sessionId, itemInSession, artist, song, firstName, lastName)"
        query = query + " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        artist, firstName, gender, itemInSession, lastName, length, level, location, sessionId, song, userId = line
        session.execute(query, (int(userId), int(sessionId), int(itemInSession), artist, song, firstName, lastName))


# In[41]:


## TO-DO: Query 3: Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'

try:
    rows = session.execute(select_song_users, (10, 182))
except Exception as e:
    print(e)
    
for row in rows:
    print("Artist: "+row.artist, "\nSong Title: "+row.song, "\nUser First Name: "+row.firstname, "\nUser Last Name: "+row.lastname)    
    print('=========================')


# ## Query 3
# Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
# 
# Let's call our new table users_history.
# 
# In CQL, to answer this question we will need to obtain (select) the first and last name, who listened to the song 'All Hands Against His Own'. Here's what we obtain:
# ````sql
# SELECT firstName, lastName FROM users_history WHERE song = 'All Hands Against His Own'
# ````
# * Our primary key will consist of **partition key** song, 
# * **Clustering key** userId. This uniquely identifies our rows.
# * The columns of our table will be: song, firstName, lastName and userId.

# In[42]:


create_users_history = "CREATE TABLE IF NOT EXISTS users_history"
create_users_history = create_users_history + (""" (song TEXT, userId INT, firstName TEXT, lastName TEXT, 
                                        PRIMARY KEY ((song), userId)
                )""")
try:
    session.execute(create_users_history)
except Exception as e:
    print(e)


# In[49]:


# Insertion for Table 3
file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
        query = "INSERT INTO users_history(song, userId, firstName, lastName)"
        query = query + "VALUES (%s, %s, %s, %s)"
        ## Assign which column element should be assigned for each column in the INSERT statement.
        session.execute(query, (line[9], int(line[10]), line[1], line[4]))
        
select_users_history = """ SELECT   firstName, 
                                    lastName 
                           FROM users_history 
                           WHERE song = %s;
                       """


# In[56]:


try:
    rows = session.execute(select_users_history, ('All Hands Against His Own', ))
except Exception as e:
    print(e)

for row in rows:
    print("User First Name: "+row.firstname, "\nUser Last Name: "+row.lastname)


# ### Drop the tables before closing out the sessions

# In[57]:


## TO-DO: Drop the table before closing out the sessions


# In[58]:


session.execute("DROP TABLE IF EXISTS song_details")
session.execute("DROP TABLE IF EXISTS song_users")
session.execute("DROP TABLE IF EXISTS users_history")


# ### Close the session and cluster connection¶

# In[59]:


session.shutdown()
cluster.shutdown()


# In[ ]:




