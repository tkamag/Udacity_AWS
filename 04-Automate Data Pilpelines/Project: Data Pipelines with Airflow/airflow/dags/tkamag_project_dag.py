from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

from operators.stage_redshift import StageToRedshiftOperator
from operators.load_fact      import LoadFactOperator
from operators.load_dimension import LoadDimensionOperator
from operators.data_quality   import DataQualityOperator
from helpers import SqlQueries, create_tables


default_args = {
    'owner': 'udacity-thierry-kamagne',
    'start_date': datetime(2023, 8, 16),
    'depends_on_past': False,
    'email': ['thierry.kamagne@gmail.com'],
    'email_on_retry': True,
    'retries': 3,
    'catchup': False,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'Songify_pipeline',
    default_args=default_args,
    description='Transform and Load data in Redshift with Airflow',
    schedule_interval='0 * * * *'
)

start_operator = DummyOperator(
    task_id='Begin_execution',
    dag=dag
)

stage_events_to_redshift = StageToRedshiftOperator(
    description='This stage copy events data to Redshift Cluster',
    task_id='Stage_events',
    dag=dag,
    table='staging_events',
    redshift_conn_id = 'redshift',
    s3_bucket = 'udacity-dend',
    s3_key = 'log_data',
    delimiter = '',
    ignore_headers = '',
    aws_credentials_id = ''
)

stage_songs_to_redshift = StageToRedshiftOperator(
    description='This stage copy songs data to Redshift Cluster',
    task_id='Stage_songs',
    dag=dag,
    table='staging_songs',
    redshift_conn_id = 'redshift',
    s3_bucket="udacity-dend",
    s3_key="song_data",
    delimiter = '',
    ignore_headers = '',
    aws_credentials_id = ''
)

# Creating table
create_artist_table_task=PostgresOperator(
       task_id="Create_Artist_table",
        postgres_conn_id="redshift",  dag=dag, 
        sql=create_tables.CREATE_ARTIST_TABLE_SQL
    )

create_songplays_table_task=PostgresOperator(
       task_id="Create_SongPlays_table",
        postgres_conn_id="redshift",  dag=dag, 
        sql=create_tables.CREATE_SONGPLAYS_TABLE_SQL
    )

create_song_table_task=PostgresOperator(
       task_id="Create_Songs_table",
        postgres_conn_id="redshift",  dag=dag, 
        sql=create_tables.CREATE_SONGS_TABLE_SQL
    )

create_staging_events_table_task=PostgresOperator(
       task_id="Create_staging_events_table",
        postgres_conn_id="redshift",  dag=dag, 
        sql=create_tables.CREATE_STAGING_EVENTS_TABLE_SQL
    )

create_staging_songs_table_task=PostgresOperator(
       task_id="Create_staging_songs_table",
        postgres_conn_id="redshift",  dag=dag, 
        sql=create_tables.CREATE_STAGING_SONGS_TABLE_SQL
    )

create_time_table_task=PostgresOperator(
       task_id="Create_Time_table",
        postgres_conn_id="redshift",  dag=dag, 
        sql=create_tables.CREATE_TIME_TABLE_SQL
    )

create_users_task=PostgresOperator(
       task_id="Create_Users_table",
        postgres_conn_id="redshift",  dag=dag, 
        sql=create_tables.CREATE_USERS_TABLE_SQL
    )

end_table_operator = DummyOperator(
    task_id='End_sCreating_table',
    dag=dag
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id='redshift',
    query = SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    query = SqlQueries.user_table_insert,
    table = 'users',
    truncate = False

)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    query = SqlQueries.song_table_insert,
    table = 'songs',
    truncate = False,
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    query = SqlQueries.artist_table_insert,
    table = 'artists',
    truncate = False,
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    query = SqlQueries.time_table_insert,
    table = 'time',
    truncate = False,
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    tables= ['songplays', 'artists', 'users', 'time', 'songs'],
    redshift_conn_id = 'redshift'
)

end_operator = DummyOperator(
    task_id='Stop_execution',
    dag=dag
)


# Group all stages
end_table_operator >> [stage_events_to_redshift, stage_songs_to_redshift]
[stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table

load_songplays_table >> [load_user_dimension_table, load_song_dimension_table,
                         load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks

run_quality_checks >> end_operator
start_operator >> create_artist_table_task >> end_table_operator

start_operator >> create_songplays_table_task >> end_table_operator
start_operator >> create_song_table_task >> end_table_operator
start_operator >> create_staging_events_table_task >> end_table_operator
start_operator >> create_staging_songs_table_task >> end_table_operator
start_operator >> create_time_table_task >> end_table_operator
start_operator >> create_users_task >> end_table_operator