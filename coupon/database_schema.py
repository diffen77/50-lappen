#from sys import get_coroutine_origin_tracking_depth
from venv import create
import psycopg2, os
from configparser import ConfigParser

config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
print(config_file)
coupon_config = ConfigParser()
coupon_config.read(config_file)

satan = input("SVen:")

print(satan)
def database_schema_setup():
        
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = coupon_config['POSTGRES']['host'],
            dbname = coupon_config['POSTGRES']['dbname'],
            user = coupon_config['POSTGRES']['user'],
            password = coupon_config['POSTGRES']['password'],
            port = coupon_config['POSTGRES']['port']
        
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

