from database_schema import database_schema_setup
from coupon_creation import coupon_creation
import time


if __name__ == '__main__':
    #Wait for database to start accepting TCP connections
    time.sleep(10)

    try:
        #Create database schema in PostGress
        database_schema_setup()

        #Create current week coupon
        coupon_creation()

    except Exception as error:
        print(error)




