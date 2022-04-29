from ast import While
from cgitb import text
import datetime
from distutils.log import error
from logging import exception
import urllib.request
import json, psycopg2, os, time
from xmlrpc.client import DateTime
#from database_schema import database_schema_setup
from flatten_json import flatten
from configparser import ConfigParser


def coupon_creation():

    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    print(config_file)

    coupon_config = ConfigParser()
    coupon_config.read(config_file)

    #Create database schema in PostGress
#    database_schema_setup()

    try:
            

        conn = psycopg2.connect(
            host = os.getenv('COUPON_HOST'),
            dbname = os.getenv('COUPON_DB_NAME'),
            user = os.getenv('COUPON_DB_USER'),
            password = os.getenv('COUPON_DB_PASSWORD'),
            port = os.getenv('COUPON_DB_PORT')
        )

        cur = conn.cursor()
    
    except Exception as error:
        print(error)



    urlData = "https://api.www.svenskaspel.se/draw/stryktipset/draws"

    operUrl = urllib.request.urlopen(urlData)
    data = operUrl.read()
    jsonData = json.loads(data)
    jsonData = flatten(jsonData)

    i = 0
    matchNumber = 1
    couponId = jsonData['draws_0_drawNumber']
    regCloseTime = jsonData['draws_0_regCloseTime']


    print("Kupong ID: " + str(couponId) + ", Spelstopp: " + str(regCloseTime))
    while i < 13:
        homeTeam = 'draws_0_drawEvents_' + str(i) + '_match_participants_0_name'
        awayTeam = 'draws_0_drawEvents_' + str(i) + '_match_participants_1_name'

        selectQuery = "Select matchNumber from coupons WHERE couponID = " + str(couponId) + " AND matchNumber = " + str(matchNumber)
                
        try:
            
            cur.execute(selectQuery)
            
            failcheck = cur.fetchall()        
            
            
            if len(failcheck) == 0:

                insertQuery = "INSERT INTO coupons(couponid, regclosetime, matchnumber, hometeam, awayteam) VALUES ('" + str(couponId) + "','" + regCloseTime + "', '" + str(matchNumber) + "', '" + jsonData[homeTeam] + "', '" + jsonData[awayTeam] + "')"

                cur.execute(insertQuery)
            
                conn.commit()

                print("Added into DB: " + str(matchNumber) + ": " + jsonData[homeTeam] + " - " + jsonData[awayTeam])
            else:
                print("Exists in DB: " + str(matchNumber) + ": " + jsonData[homeTeam] + " - " + jsonData[awayTeam])
            
            matchNumber += 1
            i += 1
        except Exception as error:
            print(error)
        
        



#if __name__ == '__main__':
#    time.sleep(10)

#    try:
#        coupon_creation()
#    except Exception as error:
#        print(error)

