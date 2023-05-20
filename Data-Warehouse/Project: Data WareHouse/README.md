# Project: Data Warehouse

## Introduction 
``Sparkify``, a music streaming startup, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Assignation

As a data engineer, our assignment is to build an ``ETL pipeline`` that extracts data from their current location (here ``S3``), stages them in ``Redshift``, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. We'll be able to test your database and ``ETL pipeline`` by running queries given to you by the analytics team from ``Sparkify`` and compare your results with their expected results.

``Sparkify`` data are a collection of information stored in an organized manner for easy retrieval and use. These data are store into tables  and related to each other. ``Relational databases`` are tools for storing various types of information that are related to each other in some way. 

 Data engineers build and design relational databases to assist organizations in collecting, storing, and analyzing data. Then, data analysts and data scientists use them for digesting large amounts of data and identifying meaningful insights. You can learn more about relational database features, use cases, and know much mùore about users preferences. For example, what is the most played song? When is the highest usage time of day by hour for songs?etc ...

 ## Schema for Song Play Analysis
 Using the song and event datasets, we've created a star schema optimized for queries on song play analysis. This includes the following tables. 
 ### Fact Table
1. songplays - records in event data associated with song plays i.e. records with page NextSong
* songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
### Dimension Tables
1. users - users in the app
* user_id, first_name, last_name, gender, level
2. songs - songs in music database
* song_id, title, artist_id, year, duration
3. artists - artists in music database
* artist_id, name, location, lattitude, longitude
4. time - timestamps of records in songplays broken down into specific units
* start_time, hour, day, week, month, year, weekday
 ## How to run