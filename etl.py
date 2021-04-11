import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    copy the data from s3 bucket to staging tables
    --------
    Param:
        cur: the cursor object. 
        conn: the connection to the database
    Return:
        None.
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    insert the data from staging tables to the database
    --------
    Param:
        cur: the cursor object. 
        conn: the connection to the database
    Return:
        None.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Copy all the data from S3 to the staging tables.
    
    - Insert the data from the staging tables to the database tables.
    
    - Finally, closes the connection. 
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()