import pymysql
import sys
import string
from utils.DbConfig import mysql
from flask import jsonify
from flask import flash,request

def apiAuth(token, user):
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("select * from user where email = '" + user + "' and token = '"+token+"';")
        rows = cur.fetchall()
        if len(rows) == 0:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()
        cur.close()
