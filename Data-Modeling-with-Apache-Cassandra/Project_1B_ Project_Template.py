#!/usr/bin/env python
# coding: utf-8

# # Part I. ETL Pipeline for Pre-Processing the Files
# #### Import Python packages 
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
# checking your current working directory
print(os.getcwd())

# Get your current folder and subfolder event data
filepath = os.getcwd() + '/event_data'

# Create a for loop to create a list of files and collect each filepath
for root, dirs, files in os.walk(filepath):
    
# join the file path and roots with the subdirectories using glob
    file_path_list = glob.glob(os.path.join(root,'*'))
    print(file_path_list)

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
print(full_data_rows_list)

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

# check the number of rows in your csv file
with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
    print(sum(1 for line in f))

# Let print the columns names of our data.

for line in list(pd.read_csv('event_datafile_new.csv').columns):
    print(line)

# #### Creating a Cluster

from cassandra.cluster import Cluster
cluster = Cluster()

# To establish connection and begin executing queries, need a session
session = cluster.connect()

# #### Create Keyspace
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

try:
    session.set_keyspace('udacity')
except Exception as e:
    print(e)

# Query 1

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
try:
    rows = session.execute(select_song_details, (338, 4))
except Exception as e:
    print(e)
    
for row in rows:
    print("Artist: "+row.artist, "\nSong Title: "+row.song, "\nSong Length: "+str(row.length))

# Query 2

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
with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
        query = "INSERT INTO song_users (userId, sessionId, itemInSession, artist, song, firstName, lastName)"
        query = query + " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        artist, firstName, gender, itemInSession, lastName, length, level, location, sessionId, song, userId = line
        session.execute(query, (int(userId), int(sessionId), int(itemInSession), artist, song, firstName, lastName))

try:
    rows = session.execute(select_song_users, (10, 182))
except Exception as e:
    print(e)
    
for row in rows:
    print("Artist: "+row.artist, "\nSong Title: "+row.song, "\nUser First Name: "+row.firstname, "\nUser Last Name: "+row.lastname)    
    print('=========================')


# Query 3

create_users_history = "CREATE TABLE IF NOT EXISTS users_history"
create_users_history = create_users_history + (""" (song TEXT, userId INT, firstName TEXT, lastName TEXT, 
                                        PRIMARY KEY ((song), userId)
                )""")
try:
    session.execute(create_users_history)
except Exception as e:
    print(e)

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

try:
    rows = session.execute(select_users_history, ('All Hands Against His Own', ))
except Exception as e:
    print(e)

for row in rows:
    print("User First Name: "+row.firstname, "\nUser Last Name: "+row.lastname)


# ### Drop the tables before closing out the sessions
session.execute("DROP TABLE IF EXISTS song_details")
session.execute("DROP TABLE IF EXISTS song_users")
session.execute("DROP TABLE IF EXISTS users_history")

# ### Close the session and cluster connection¶
session.shutdown()
cluster.shutdown()
