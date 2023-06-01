import configparser
import psycopg2
import logging
from sql_queries import select_all_rows_queries

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')


def fetch_results(cur, conn):
    """
    Get the number of rows for each table
    """
    for query in select_all_rows_queries:
        cur.execute(query)
        results = cur.fetchone()

        for row in results:
            logger.info(f"\nRunning: \n{query}  \t {row } rows")


def main():
    """
    Run queries on dimensional and staging tables
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(
            *config['CLUSTER'].values()))
        cur = conn.cursor()

        fetch_results(cur, conn)

        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'{error}')


if __name__ == "__main__":
    main()
