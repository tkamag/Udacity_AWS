# Project: Data Pipelines with Airflow

## Introduction 
``Sparkify``, a music streaming startup, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Assignation

As a data engineer, our assignment is to build an ``ETL pipeline`` that extracts data from their current location (here ``S3``), stages them in ``Redshift``, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. We'll be able to test your database and ``ETL pipeline`` by running queries given to you by the analytics team from ``Sparkify`` and compare your results with their expected results.

``Sparkify`` data are a collection of information stored in an organized manner for easy retrieval and use. These data are store into tables  and related to each other. ``Relational databases`` are tools for storing various types of information that are related to each other in some way. 

 Data engineers build and design relational databases to assist organizations in collecting, storing, and analyzing data. Then, data analysts and data scientists use them for digesting large amounts of data and identifying meaningful insights. You can learn more about relational database features, use cases, and know much mùore about users preferences. For example, what is the most played song? When is the highest usage time of day by hour for songs?etc ...

## Schema for Song Play Analysis
 Using the song and event datasets, we've created a **star schema** optimized for queries on song play analysis. 
 The purpose of a **star schemas** is to denormalize the data, which means adding redundant columns to dimension tables to make querying and working with the data faster and easier. The goal is to trade some redundancy (duplication of data) in the data model for increased query speed, by avoiding computationally expensive join operations.

  Buy using a **star schema**, we can easily answer some suqestion like /
 * Count and order the most 10 songs title, and artist namelistened by women in 2018.

````SQL
SELECT
	dim_artists.name,
    dim_songs.title,
	COUNT(fact_songplays.songplay_id) as number_of_songplays

FROM fact_songplays 

INNER JOIN dim_artists 	      ON (fact_songplays.artist_id = dim_artists.artist_id)
INNER JOIN dim_songs 	      ON (fact_songplays.song_id = dim_songs.song_id)
INNER JOIN dim_users 	      ON (fact_songplays.user_id = dim_users.user_id)
INNER JOIN dim_time  	      ON (fact_songplays.start_time = dim_time.start_time)

where dim_time.year = 2018 and dim_users.gender = 'F'

GROUP BY
	dim_artists.name,  dim_songs.title
order by 
    number_of_songplays desc
limit 10
````
 
 
 This includes the following tables. 
 ### Fact Table
1. **fact_songplays** - records in event data associated with song plays i.e. records with page NextSong
### Dimension Tables
1. **dim_users** - users in the app
2. **dim_songs** - songs in music database
3. **dim_artists** - artists in music database
4. **dim_time** - timestamps of records in songplays broken down into specific units

The overall schema can be resume below:

<p align="center">
  <img src="./fig/schema.png" alt=".." title="Optional title" width="80%" height="70%"/>  
</p> 
