import datetime
import os
from distutils.log import error

import psycopg2
from flask import Flask, jsonify, request
from psycopg2 import Error
from psycopg2.extras import RealDictCursor




#conn = psycopg2.connect(
#    user="gunnar", password="gunnar", host="localhost", port="5432", database="50-lappen"
#)

try:
        
    conn = psycopg2.connect(
        host = os.getenv('COUPON_HOST'),
        dbname = os.getenv('COUPON_DB_NAME'),
        user = os.getenv('COUPON_DB_USER'),
        password = os.getenv('COUPON_DB_PASSWORD'),
        port = os.getenv('COUPON_DB_PORT')
        
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)

except Exception as error:
    print(error)

app = Flask(__name__)

# gunnarasdf asdf asdf


# asdfd fa asdf


@app.route("/coupon", methods=["GET"])
def handle_items():
    try:

        cursor.execute("select * from coupons")
        result = cursor.fetchall()

        # [a["regclosetime"] for a in result]

        # result = [datetime(result.regclosetime).isoformat() for result.regclosetime in result]'

        for res in result:
            res["regclosetime"] = res["regclosetime"].isoformat()

        print(result)

        return jsonify(result)

    except Exception as error:
        return error


handle_items()


if __name__ == "__main__":
    app.run(debug=True)