import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, staging_table_info, drop_table_queries, create_table_queries, insert_table_info, select_all_rows_queries
import logging

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def create_tables(cur, conn):
    """
        This function iterates over sql_queries.py and create staging and dimensional tables.
    """
    logger.info("Creating dimensional and staging tables...")
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
    logger.info("Creating all tables is completed!")


def drop_tables(cur, conn):
    """
        This function iterates over sql_queries.py and drop all existing tables.
    """
    logger.info("Dropping any existing tables...")
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
    logger.info("Dropping all tables is completed!")


def insert_tables(cur, conn):
    """
        This function iterates over sql_queries.py and runs each one.
    """
    logger.info(
        "Beginning loading of dimensional data from staging to production analytics tables...")
    for query, info in list(zip(insert_table_queries, insert_table_info)):
        print("Loading data from {}...".format(info))
        cur.execute(query)
        conn.commit()
    logger.info("Completed inserting data into the dimensional tables!")


def load_staging_tables(cur, conn):
    """
        This function iterates over sql_queries.py and runs each one.
        staging_table_info, contains headings of what the function is.
    """
    logger.info("Loading data from S3 into the staging tables...")
    for query, info in list(zip(copy_table_queries, staging_table_info)):
        logger.info(query)
        logger.info(
            "Currently loading the {} from S3 to the staging table...".format(info))
        cur.execute(query)
        conn.commit()
    logger.info("Loading all data into the staging tables is completed!")


def run_sample(cur, conn):
    """
        This function iterates over sql_queries.py containing the variables to be run.
    """
    logger.info("Run some sample queries as a test...")
    for query, info in list(zip(sample_queries, sample_query_info)):
        logger.info(f"{info}")
        cur.execute(query)
        row = cur.fetchone()
        while row:
            logger.info(list(row))
            row = cur.fetchone()


def fetch_results(cur, conn):
    """
    Get the number of rows for each table
    """
    for query in select_all_rows_queries:
        logger.info('Running ' + query)
        cur.execute(query)
        results = cur.fetchone()

        for row in results:
            logger.info("   ", row)


def main():
    """
        This main function reads variables within the dwh.cfg file and uses them to connect to the Postgresql database.
        Created cursor encapsulates the entire SQL query to process each individual row from the result.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
            *config['CLUSTER'].values()))
        cur = conn.cursor()
        logger.info("Connecting to database: {}\n".format(conn))

        load_staging_tables(cur, conn)
        insert_tables(cur, conn)
        
        logger.info("Completed loading and insering data in all tables!")
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.info(f'{error}')


if __name__ == "__main__":
    main()
