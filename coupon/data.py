from ast import While
from cgitb import text
import datetime
from distutils.log import error
from logging import exception
import urllib.request
import json, psycopg2
from xmlrpc.client import DateTime
from database_schema import database_schema_setup
from flatten_json import flatten
from configparser import ConfigParser

coupon_config = ConfigParser()
coupon_config.read("coupon/config.ini")

#Create database schema in PostGress
database_schema_setup()



conn = psycopg2.connect(
    dbname = coupon_config['POSTGRES']['dbname'],
    user = coupon_config['POSTGRES']['user'],
    password = coupon_config['POSTGRES']['password'],
    host = coupon_config["POSTGRES"]["host"],
    port = coupon_config['POSTGRES']['port']
)


cur = conn.cursor()


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

    #if __name__ == '__main__':
    #    app.run()