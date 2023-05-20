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
1. **fact_songplays** - records in event data associated with song plays i.e. records with page NextSong
### Dimension Tables
1. **dim_users** - users in the app
2. **dim_songs** - songs in music database
3. **dim_artists** - artists in music database
4. **dim_time** - timestamps of records in songplays broken down into specific units

The overall schema can be resume below:

<p align="center">
  <img src="./fig/schema.png" alt=".." title="Optional title" width="66%" height="70%"/>  
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

$ python create_iam_cluster.py
````log
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

Run the create_tables script to set up the database staging and analytical tables

$ python create_tables.py

Finally, run the etl script to extract data from the files in S3, stage it in redshift, and finally store it in the dimensional tables.

$ python create_tables.py