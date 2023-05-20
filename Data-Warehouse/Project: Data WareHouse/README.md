# Project: Data Warehouse

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

````python
SELECT
	dim_artists.name,
    dim_songs.title,
	COUNT(fact_songplays.songplay_id)

FROM fact_songplays 

INNER JOIN dim_artists 	      ON (fact_songplays.artist_id = dim_artists.artist_id)
INNER JOIN dim_songs 	      ON (fact_songplays.song_id = dim_songs.song_id)
INNER JOIN dim_users 	      ON (fact_songplays.user_id = dim_users.user_id)
INNER JOIN dim_time  	      ON (fact_songplays.start_time = dim_time.start_time)

where dim_time.year = 2018 and dim_users.gender = 'F'

GROUP BY
	dim_artists.name,  dim_songs.title
order by count desc
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

 ## How to run
 1. The project folder includes several files where the main important is ``dwh.cfg``, wher you have to fill the some informations, and save it as ``dwh.cfg`` in the project root folder.

 ````cfg
[CLUSTER]
HOST='dwhclusterproject.XXXXXXXXXXX.us-west-2.redshift.amazonaws.com'
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=5439

[CLUSTER_PRO]
#DWH_CLUSTER_TYPE=single-node
DWH_CLUSTER_TYPE=multi-node
#DWH_NUM_NODES=1
DWH_NUM_NODES=4
DWH_NODE_TYPE=dc2.large
DWH_CLUSTER_IDENTIFIER=dwhClusterProject

[IAM_ROLE]
DWH_IAM_ROLE_NAME=dwhRole
DWH_ARN=arn:aws:iam::XXXXXXXXXXXX:role/dwhRole

[S3]
LOG_DATA='s3://udacity-dend/log-data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song-data'

[AWS]
ACCESS_KEY=
SECRET_KEY=
ACCESS_REGION = 'us-west-2'
````
2. Create an activate **python environment** with the dependencies listed on requirements.txt.

````python
python3 -m venv ~/.UdacityProject

source  ~/.UdacityProject/bin/activate
````

3. Run the ``create_iam_cluster.py`` script to set up all the infrastructure for this project.
````python
$ python create_iam_cluster.py
````

````python
W:\MOOC\Udacity\AWS Data Engineering with AWS\02.Cloud Data Warehouses\06.Project Data Warehouse>python create_iam_cluster.py
2023-05-19 14:58:37,119: INFO: 1.1 Creating a new IAM Role
2023-05-19 14:58:37,615: INFO: 1.2 Attaching Policy
2023-05-19 14:58:37,779: INFO: 1.3 Get the IAM role ARN
2023-05-19 14:58:37,911: INFO: IAM role created with ID:  arn:aws:iam:XXXXXXXXXXXX:role/dwhRole
2023-05-19 14:58:37,911: INFO: Creating Redshift Cluster...
2023-05-19 15:01:14,476: INFO: Redshift Cluster endpoint: dwhclusterproject.xxxxxxxxxxxx.us-west-2.redshift.amazonaws.com
2023-05-19 15:01:14,476: INFO: Redshift Cluster arn:    arn:aws:iam::XXXXXXXXXXXX:role/dwhRole
2023-05-19 15:01:14,477: INFO: Redshift Cluster dwhClusterProject was created !!!
2023-05-19 15:01:14,477: INFO: Update clusters security group...
'VpcId'
2023-05-19 15:01:14,479: INFO: None
2023-05-19 15:01:14,480: INFO: postgresql://dwhuser:XXXXXXXX@dwhclusterproject.XXXXXXXXXXXX.us-west-2.redshift.amazonaws.com:5439/dwh
2023-05-19 15:01:15,763: INFO: Connected to the Cluster for testing.
2023-05-19 15:01:15,764: INFO: Connection OK.!!!
````

4. Run the ``create_tables script.py`` to set up the database staging and analytical tables. This script will build the overall **ETL pipeline**
````python
$ python create_tables.py
````

````python
W:\MOOC\Udacity\AWS Data Engineering with AWS\02.Cloud Data Warehouses\06.Project Data Warehouse>python create_tables.py
2023-05-19 15:04:19,376: INFO: Connecting to database....
2023-05-19 15:04:19,377: INFO: Dropping any existing tables...
2023-05-19 15:04:22,908: INFO: Creating dimensional and staging tables...
2023-05-19 15:04:26,902: INFO: Completed creating all tables!
````

5. Finally, run the ``etl.py`` script to extract data from the files in S3, stage it in redshift, and store it in the dimensional tables.
````python
$ python create_tables.py
````

````python
2023-05-19 15:06:03,139: INFO: Connecting to database: <connection object at 0x000002322FAF2790; 
dsn: 'user=dwhuser password=xxx dbname=dwh host=dwhclusterproject.XXXXXXXXXXXX.us-west-2.redshift.amazonaws.com port=5439', 
closed: 0>

2023-05-19 15:06:03,140: INFO: Loading data from S3 into the staging tables...
2023-05-19 15:06:03,140: INFO:
    COPY staging_events FROM 's3://udacity-dend/log-data'
    credentials 'aws_iam_role=arn:aws:iam::XXXXXXXXXXXX:role/dwhRole'
    region 'us-west-2'
    format as json 's3://udacity-dend/log_json_path.json';

2023-05-19 15:06:03,140: INFO: Currently loading the Log event dataset from S3 to the staging table...
2023-05-19 15:06:34,046: INFO:
    COPY staging_songs FROM 's3://udacity-dend/song-data'
    credentials 'aws_iam_role=arn:aws:iam::XXXXXXXXXXXX:role/dwhRole'
    region 'us-west-2'
    format as json 'auto';

2023-05-19 15:06:34,047: INFO: Currently loading the Song dataset from S3 to the staging table...
2023-05-19 17:17:04,416: INFO: Loading all data into the staging tables is completed!
2023-05-19 17:17:04,423: INFO: Beginning loading of dimensional data from staging to production analytics tables...
Loading data from User table...
Loading data from Song table...
Loading data from Artist table...
Loading data from Time table...
Loading data from Song play table...
2023-05-19 17:18:07,284: INFO: Completed inserting data into the dimensional tables!
2023-05-19 17:18:07,287: INFO: Completed loading and insering data in all tables!
````

6. For some uses cases analysis(like counting the numbers of rows in each tables) , run ``query_results.py``.
````python
$ python query_results.py
````

````python
W:\MOOC\Udacity\AWS Data Engineering with AWS\02.Cloud Data Warehouses\06.Project Data Warehouse>python query_results.py
2023-05-19 19:21:40,576: INFO:
Running:
    SELECT COUNT(*) FROM staging_events
         8056 rows
2023-05-19 19:21:40,764: INFO:
Running:
    SELECT COUNT(*) FROM staging_songs
         385252 rows
2023-05-19 19:21:40,952: INFO:
Running:
    SELECT COUNT(*) FROM fact_songplays
         6962 rows
2023-05-19 19:21:41,134: INFO:
Running:
    SELECT COUNT(*) FROM dim_users
         104 rows
2023-05-19 19:21:41,318: INFO:
Running:
    SELECT COUNT(*) FROM dim_songs
         384995 rows
2023-05-19 19:21:41,506: INFO:
Running:
    SELECT COUNT(*) FROM dim_artists
         45266 rows
2023-05-19 19:21:41,692: INFO:
Running:
    SELECT COUNT(*) FROM dim_time
         6813 rows
 ````

7. Delete your redshift cluster when finished. You also need to detach role policy and delete role created.
   
````python
redshift.delete_cluster( ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,  SkipFinalClusterSnapshot=True)
iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME, PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
````