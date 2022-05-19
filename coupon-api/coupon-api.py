import datetime
import os
import time
from distutils.log import error

import psycopg2
from flask import Flask, jsonify, request
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

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





@app.route("/coupon", methods=["GET"])
def handle_items():
    with app.app_context():
        try:

            cursor.execute("select * from coupons where regclosetime = (SELECT MAX(regclosetime) FROM coupons)")
            result = cursor.fetchall()

            # [a["regclosetime"] for a in result]

            # result = [datetime(result.regclosetime).isoformat() for result.regclosetime in result]'

            for res in result:
                res["regclosetime"] = res["regclosetime"].isoformat()

            print(result)

            return jsonify(result)

        except Exception as error:
            print(error)



if __name__ == "__main__":
    time.sleep(10)
    handle_items()
    app.run(debug=True, host="0.0.0.0", port=8081)