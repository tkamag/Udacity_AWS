import configparser
import logging

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

# CONFIG
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

# GET PARAMS
LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")
# IAM_ROLE = config.get("IAM_ROLE","DWH_ARN")
REGION = config.get("AWS", "ACCESS_REGION")
DWH_ARN = config.get("IAM_ROLE", "DWH_ARN")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS fact_songplays"
user_table_drop = "DROP TABLE IF EXISTS dim_users"
song_table_drop = "DROP TABLE IF EXISTS dim_songs"
artist_table_drop = "DROP TABLE IF EXISTS dim_artists"
time_table_drop = "DROP TABLE IF EXISTS dim_time"


# CREATE TABLES

# For the staging tables we will not apply the 'NOT NULL' constraint as
# we want to ensure to pull in all available data from S3 and not be
# affected by any missing data errors that may arise.
staging_events_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_events (
        artist             VARCHAR(500),
        auth               VARCHAR(20),
        firstName          VARCHAR(50),
        gender             VARCHAR(1),
        itemInSession      SMALLINT,
        lastName           VARCHAR(50),
        length             FLOAT,
        level              VARCHAR(5),
        location           VARCHAR(350),
        method             VARCHAR(6),
        page               VARCHAR(255),
        registration       FLOAT,
        sessionId          SMALLINT,
        song               VARCHAR(255),
        status             SMALLINT,
        ts                 BIGINT,
        userAgent          VARCHAR(255),
        userId             INT
    )
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        song_id            VARCHAR(30) PRIMARY KEY,
        num_songs          INTEGER,
        artist_id          VARCHAR(30),
        artist_latitude    DECIMAL(8,6),
        artist_longitude   DECIMAL(9,6),
        artist_location    VARCHAR(350),
        artist_name        VARCHAR(500),
        title              VARCHAR(300),
        duration           FLOAT,
        year               SMALLINT
    )
""")

# records in event data associated with song plays i.e. records with page NextSong
songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS fact_songplays (
        songplay_id     VARCHAR(20) PRIMARY KEY,
        start_time      TIMESTAMP,
        user_id         INT NOT NULL,
        level           VARCHAR(5),
        song_id         VARCHAR(20) NOT NULL,
        artist_id       VARCHAR(20) NOT NULL,
        session_id      INT NOT NULL,
        location        VARCHAR(350),
        user_agent      VARCHAR(255)
    )
""")

# users in the app
user_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_users (
        user_id         INT PRIMARY KEY,
        first_name      VARCHAR(50),
        last_name       VARCHAR(50),
        gender          VARCHAR(1),
        level           VARCHAR(5)
    )
""")

# songs in the music database
song_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_songs (
        song_id         VARCHAR(20) PRIMARY KEY,
        title           VARCHAR(300),
        artist_id       VARCHAR(20) NOT NULL,
        year            SMALLINT,
        duration        FLOAT
    )
""")

# artists in music database
artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_artists (
        artist_id       VARCHAR(20) PRIMARY KEY,
        name            VARCHAR(500),
        location        VARCHAR(500),
        latitude        DECIMAL(8,6),
        longitude       DECIMAL(9,6)
    )
""")

# timestamps of records in songplays broken down into specific units
time_table_create = ("""
    CREATE TABLE IF NOT EXISTS dim_time (
        start_time      TIMESTAMP PRIMARY KEY,
        hour            SMALLINT,
        day             SMALLINT,
        week            SMALLINT,
        month           SMALLINT,
        year            SMALLINT,
        weekday         SMALLINT
    )
""")


# STAGING TABLES

staging_songs_copy = ("""
    COPY staging_songs FROM {}
    credentials 'aws_iam_role={}'
    region {}
    format as json 'auto';
""").format(SONG_DATA, DWH_ARN, REGION)


staging_events_copy = ("""
    COPY staging_events FROM {}
    credentials 'aws_iam_role={}'
    region {}
    format as json {};
""").format(LOG_DATA, DWH_ARN, REGION, LOG_JSONPATH)


# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO fact_songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT
        ss.song_id AS songplay_id,
        TIMESTAMP 'epoch' + CAST(se.ts AS BIGINT)/1000 * interval '1 second' AS start_time, 
        se.userId AS user_id,
        se.level AS level,
        ss.song_id AS song_id,
        ss.artist_id AS artist_id,
        se.sessionId AS session_id,
        se.location AS location,
        se.userAgent AS user_agent
    FROM staging_songs ss
    LEFT JOIN staging_events se
    ON ss.artist_name = se.artist AND ss.title = se.song
    WHERE se.page = 'NextSong'
""")

user_table_insert = ("""
    INSERT INTO dim_users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT
        userId AS userId,
        firstName AS first_name,
        lastName AS last_name,
        gender,
        level
    FROM staging_events se
    WHERE se.page = 'NextSong'
""")

song_table_insert = ("""
    INSERT INTO dim_songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
""")

artist_table_insert = ("""
    INSERT INTO dim_artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT
        artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs
""")

time_table_insert = ("""
    INSERT INTO dim_time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT
        TIMESTAMP 'epoch' + CAST(ts AS BIGINT)/1000 * interval '1 second' AS start_time, 
        DATE_PART(hour, start_time) AS hour,
        DATE_PART(day, start_time) AS day,
        DATE_PART(week, start_time) AS week,
        DATE_PART(month, start_time) AS month,
        DATE_PART(year, start_time) AS year,
        DATE_PART(weekday, start_time) AS weekday
    FROM staging_events se
    WHERE se.page = 'NextSong'
""")


count_staging_events = ("""
    SELECT COUNT(*) FROM staging_events
""")


count_staging_songs = ("""
    SELECT COUNT(*) FROM staging_songs 
""")

year_song_count = ("""
    SELECT year AS "Year_Released", SUM(num_songs) AS "Total_Songs"
    FROM staging_songs
    GROUP BY year
    HAVING Total_Songs < 1000
    ORDER BY Total_Songs desc
    LIMIT 10
""")

# GET NUMBER OF ROWS IN EACH TABLE
get_all_staging_events = ("""
    SELECT COUNT(*) FROM staging_events
""")

get_all_staging_songs = ("""
    SELECT COUNT(*) FROM staging_songs
""")

get_all_songplays = ("""
    SELECT COUNT(*) FROM fact_songplays
""")

get_all_users = ("""
    SELECT COUNT(*) FROM dim_users
""")

get_all_songs = ("""
    SELECT COUNT(*) FROM dim_songs
""")

get_all_artists = ("""
    SELECT COUNT(*) FROM dim_artists
""")

get_all_time = ("""
    SELECT COUNT(*) FROM dim_time
""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create,
                        songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]

select_all_rows_queries = [get_all_staging_events, get_all_staging_songs,
                           get_all_songplays, get_all_users, get_all_songs, get_all_artists, get_all_time]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop,
                      songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
staging_table_info = ['Log event dataset', 'Song dataset']
insert_table_queries = [user_table_insert, song_table_insert,
                        artist_table_insert, time_table_insert, songplay_table_insert]
insert_table_info = ['User table', 'Song table',
                     'Artist table', 'Time table', 'Song play table']
sample_queries = [count_staging_events, count_staging_songs, year_song_count]
sample_query_info = ['Total count of the Staging Events table:',
                     'Total count of the Staging Songs table:',
                     'Total number of records released in a given year:']
