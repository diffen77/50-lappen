from ast import While
from cgitb import text
import urllib.request
import json, sqlite3
from flatten_json import flatten

conn = sqlite3.connect('coupon.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS coupons
    (couponId int, regCloseTime DateTime, matchNumber int, homeTeam string, awayTeam string)''')

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
        insertQuery = "INSERT INTO coupons VALUES ('" + str(couponId) + "', '" + str(regCloseTime) + "', '" + str(matchNumber) + "', '" + jsonData[homeTeam] + "', '" + jsonData[awayTeam] + "')"

        cur.execute(str(insertQuery))
    
        conn.commit()

        print("Added into DB: " + str(matchNumber) + ": " + jsonData[homeTeam] + " - " + jsonData[awayTeam])
    else:
        print("Exists in DB: " + str(matchNumber) + ": " + jsonData[homeTeam] + " - " + jsonData[awayTeam])
    
    matchNumber += 1
    i += 1