from venv import create
import psycopg2, os
from configparser import ConfigParser
from dotenv import load_dotenv

load_dotenv()


def database_schema_setup():
        
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = os.getenv('COUPON_HOST'),
            dbname = os.getenv('COUPON_DB_NAME'),
            user = os.getenv('COUPON_DB_USER'),
            password = os.getenv('COUPON_DB_PASSWORD'),
            port = os.getenv('COUPON_DB_PORT')
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


    try:
        conn = psycopg2.connect(
        host = os.getenv('COUPON_HOST'),
        dbname = os.getenv('COUPON_DB_NAME'),
        user = os.getenv('COUPON_DB_USER'),
        password = os.getenv('COUPON_DB_PASSWORD'),
        port = os.getenv('COUPON_DB_PORT')
        )

        cur = conn.cursor()

        create_script = '''CREATE TABLE "member_coupons" (
            "id" serial NOT NULL,
            PRIMARY KEY ("id"),
            "user_id" character varying NOT NULL,
            "1" boolean NULL DEFAULT NULL,
            "x" boolean NULL DEFAULT NULL,
            "2" boolean NULL DEFAULT NULL)'''

        cur.execute(create_script)
        conn.commit()
        

    except Exception as error:
        return error

    finally:
        if cur is not None:
            cur.close()
        
        if conn is not None:
            conn.close()

