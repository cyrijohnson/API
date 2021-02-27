import pymysql
import random as random
import string
import serviceRegistration
import dataProvider
import apiAuth as apiAuth
import security as auth
from random import randint
from app import app
from utils.DbConfig import mysql
from utils.searchImpl import getKeywords
from flask import jsonify
from flask import flash, request


def validateReviewId(conn, cur):
    try:
        autoGenId = randint(10000,99999)
        while True:
            cur.execute("select * from review where review_key = %s",(autoGenId))
            rows = cur.fetchall()
            if(len(rows) == 0):
                break
            else:
                autoGenId = randint(10000,99999)
        return autoGenId
    except Exception as e:
        return 0

@app.route('/addReview', methods=['POST'])
def reviewwriting():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        formdata = request.json
        print(formdata)
        userid = request.args.get('userid')
        token = request.args.get('tok')
        if apiAuth.apiAuth(userid,token) == True :
            serviceid = request.args.get('serviceid')
            reviewid = validateReviewId(conn, cur);
            cur.execute("insert into review(review_key,r_userid,r_serviceid,r_stars,r_header,r_content) values(%s,%s,%s,%s,%s,%s)",
                        (reviewid, userid, serviceid, formdata['star'], formdata['header'], formdata['content']))
            conn.commit()
            response = jsonify("Review added successfully")
            response.status_code = 200
            return response
        else:
            response = jsonify("unauthorised")
            response.status_code = 403
            return response
    except Exception as e:
        print(e)
        response = jsonify('Error occured')
        response.status_code = 500
        return response
    finally:
        conn.close()
        cur.close()


@app.route('/getUserReviews', methods=['GET'])
def userReviewDashboard():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        userid = request.args.get('userid')
        cur.execute('select * from review where r_userid = %s', userid)
        conn.commit()
        response = jsonify(cur.fetchall())
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        response = jsonify('Error occured')
        response.status_code = 500
        return response
    finally:
        conn.close()
        cur.close()


@app.route('/getServiceReviews', methods=['GET'])
def serviceReviewDashboard():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        serviceid = request.args.get('serviceid')
        cur.execute('select * from review where r_serviceid = %s', serviceid)
        conn.commit()
        response = jsonify(cur.fetchall())
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify('Error occured')
        response.status_code = 500
        return response
    finally:
        conn.close()
        cur.close()
