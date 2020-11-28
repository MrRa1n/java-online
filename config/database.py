import configparser
import psycopg2

from psycopg2 import pool

class DbInstance:
    __instance = None

    @staticmethod
    def getInstance():
        if DbInstance.__instance == None:
            DbInstance()
        return DbInstance.__instance

    def __init__(self):
        read_credentials()
        if DbInstance.__instance != None:
            raise Exception("Instance already exists!")
        else:
            DbInstance.__instance = self

def read_credentials():
    config = configparser.ConfigParser()
    try:
        config.read('./config/etc/database.cfg')
        user = config['postgres_credentials']['user']
        password = config['postgres_credentials']['password']
        host = config['postgres_credentials']['host']
        port = config['postgres_credentials']['port']
        database = config['postgres_credentials']['database']
        
        create_connection(user, password, host, port, database)

    except Exception as e:
        print('Could not read database config!', e)

def create_connection(user, password, host, port, database):
    try:
        postgres_pool = psycopg2.pool.SimpleConnectionPool(1, 10, user=user, password=password, host=host, port=port, database=database)

        if (postgres_pool):
            print('Connection pool created successfully')
        
        ps_connection = postgres_pool.getconn()

        if (ps_connection):
            print('Successfully retrieved connection')

            ps_cursor = ps_connection.cursor()

            ps_cursor.execute('select * from users')

            users = ps_cursor.fetchall()

            print ("Displaying rows from users table")
            for row in users:
                print(row)

            ps_cursor.close()

            #Use this method to release the connection object and send back to connection pool
            postgres_pool.putconn(ps_connection)
            print("Putting away current connection...")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        #closing database connection.
        # use closeall method to close all the active connection if you want to turn of the application
        if (postgres_pool):
            postgres_pool.closeall()
        print("PostgreSQL connection pool is closed")




