from database_schema import database_schema_setup
from data import coupon_creation
import time

#Create database schema in PostGress
database_schema_setup()

coupon_creation()

if __name__ == '__main__':
    time.sleep(10)

    try:
        coupon_creation()
    except Exception as error:
        print(error)

