import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries, staging_table_info
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
        # logger.info("Creating tables...")
        # print(query)
        cur.execute(query)
        conn.commit()


def drop_tables(cur, conn):
    """
        This function iterates over sql_queries.py and drop all existing tables.
    """
    logger.info("Dropping any existing tables...")
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


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
        logger.info("Connecting to database....")

        drop_tables(cur, conn)
        create_tables(cur, conn)
        logger.info("Completed creating all tables!")

        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.info(f'{error}')


if __name__ == "__main__":
    main()
