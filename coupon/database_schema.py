from sys import get_coroutine_origin_tracking_depth
from venv import create
import psycopg2, os
from configparser import ConfigParser

config = ConfigParser(os.environ)
config.read('coupon/config.ini')


def database_schema_setup():
        
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(


            host = config['postgres']['host'],
            dbname = config['postgres']['dbname'],
            user = config['postgres']['user'],
            password = config['postgres']['password'],
            port = config['postgres']['port']
        
        )

        cur = conn.cursor()

        create_script = '''CREATE TABLE IF NOT EXISTS coupons
        (id SERIAL PRIMARY KEY, 
        couponId int NOT NULL, 
        regCloseTime TIMESTAMP NOT NULL, 
        matchNumber int NOT NULL, 
        homeTeam varchar(30) NOT NULL, 
        awayTeam varchar(30)  NOT NULL)'''

        cur.execute(create_script)
        conn.commit()
        

    except Exception as error:
        return error

    finally:
        if cur is not None:
            cur.close()
        
        if conn is not None:
            conn.close()

