import pymysql
import sys
from random import randint
import string
import security as auth
from app import app
from utils.DbConfig import mysql
from flask import jsonify
from flask import flash,request
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/addCompany', methods = ['POST'])
def addCompany():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    _req = request.json
    try:
        if apiAuth(token, userid) == True:
            if _req['company'] == "true":
                conn = mysql.connect()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                companyid = validateCompanyId(conn, cur);
                if companyid != 0:
                    cur.execute("insert into companydetails(idcompany, name,city,phone,mobile,firstName,lastName,emailKey) values(%s, %s, %s, %s, %s, %s, %s, %s)",
                                (companyid, _req['cname'],_req['ccity'], _req['cphone'],_req['cmobile'], _req['cfname'],_req['clname'], userid))
                    conn.commit();
                    data = {"companyId":companyid, "status":"Company added successfully"}
                    response = jsonify(data)
                    response.status_code = 200
                    return response
                else:
                    data = {"companyId":companyid, "status":"Creation unsuccessful"}
                    response = jsonify(data)
                    response.status_code = 200
                    return response
            else:
                response = jsonify("No Company")
                response.status_code = 200
                return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 200
        return response
   

@app.route('/addService', methods = ['POST'])
def addService():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    _req = request.json
    try:
        if apiAuth(token, userid) == True:
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            serviceid = validateServiceId(conn, cur);
            if _req['company'] == "true":
                companyid = _req["companyid"]
                if(serviceid!=0):
                    cur.execute("insert into services(idservices, name, building, street, landmark, area, pincode, state, country, companyid, serviceUserFK,verified) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (serviceid, _req['sname'], _req['sbuilding'], _req['sstreet'], _req['slandmark'], _req['sarea'], _req['spincode'], _req['sstate'], _req['scountry'],
                                 companyid, userid,0))
                    conn.commit()
                    data = {"serviceId":serviceid, "status":"Service added successfully"}
                    response = jsonify(data)
                    response.status_code = 200
                    return response
                else:
                    data = {"serviceId":serviceid, "status":"Creation unsuccessful"}
                    response = jsonify(data)
                    response.status_code = 200
                    return response
            else:
                cur.execute("insert into services(idservices, name, building, street, landmark, area, pincode, state, country, companyid, serviceUserFK) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)",
                                (serviceid, _req['sname'], _req['sbuilding'], _req['sstreet'], _req['slandmark'], _req['sarea'], _req['spincode'], _req['sstate'], _req['scountry'],
                                 0, userid))
                conn.commit()
                data = {"serviceId":serviceid, "status":"Service added successfully"}
                response = jsonify(data)
                response.status_code = 200
                return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        response = jsonify("Database Error")
        response.status_code = 200
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/addServiceContact', methods = ['POST'])
def addServiceContact():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    _req = request.json
    try:
        if apiAuth(token, userid) == True:
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            contactid = validateContactId(conn, cur);
            serviceid = _req["serviceid"]
            if(contactid!=0):
                cur.execute("insert into servicecontactinfo(idserviceContactInfo, name, phone, cell, fax, tollfree, email, website, facebook, twitter, instagram, youtube, servicecontackfk) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (contactid, _req['conPerson'], _req['conPhone'], _req['conMobile'], _req['conFax'], _req['conTollfree'], _req['conEmail'], _req['conWebsite'], _req['conFacebook'],
                             _req['conTwitter'],_req['conInstagram'],_req['conYoutube'], serviceid))
                conn.commit()
                cur.execute("update services set contactid = %s where idservices = %s",(contactid, serviceid))
                conn.commit()
                data = {"serviceId":serviceid, "status":"Contact added successfully"}
                response = jsonify(data)
                response.status_code = 200
                return response
            else:
                data = {"serviceId":serviceid, "status":"Creation unsuccessful"}
                response = jsonify(data)
                response.status_code = 200
                return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 200
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/addServiceSchedule', methods = ['POST'])
def addServiceSchedule():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    _req = request.json
    try:
        if apiAuth(token, userid) == True:
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            scheduleid = validateScheduleId(conn, cur)
            paymentid = validatePaymentId(conn,cur)
            serviceid = _req["serviceid"]
            if(scheduleid!=0 and paymentid!=0):
                cur.execute("insert into scheduletable(scheduleId, serviceId, monStart, monEnd, tueStart, tueEnd, wedStart, wedEnd, thurStart, thurEnd, friStart, friEnd, satStart, satEnd, sunStart, sunEnd) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            (scheduleid, serviceid, _req['monBeg'], _req['monEnd'], _req['tueBeg'], _req['tueEnd'], _req['wedBeg'], _req['wedEnd'], _req['thurBeg'], _req['thurEnd'],
                             _req['friBeg'],_req['friEnd'],_req['satBeg'], _req['satEnd'], _req['sunBeg'], _req['sunEnd']))
                conn.commit()
                cur.execute("update services set scheduleid = %s where idservices = %s",(scheduleid, serviceid))
                conn.commit()
                cur.execute("Insert into paymentoptions(idpaymentoptions,idservice,cash,card,onlinepayments) values(%s,%s,%s,%s,%s)",
                            (paymentid, serviceid, _req['cash'], _req['card'], _req['digi']))
                conn.commit()
                cur.execute("update services set paymentid = %s where idservices = %s",(paymentid, serviceid))
                conn.commit()
                data = {"serviceId":serviceid, "status":"Schedule and payment added successfully"}
                response = jsonify(data)
                response.status_code = 200
                return response
            else:
                data = {"serviceId":serviceid, "status":"Creation unsuccessful"}
                response = jsonify(data)
                response.status_code = 200
                return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 200
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/addServiceKeywords', methods = ['POST'])
def addServiceKeywords():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    _req = request.json
    try:
        if apiAuth(token, userid) == True:
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            keywordsid = validateKeywordsId(conn, cur)
            serviceid = _req["serviceid"]
            if(keywordsid!=0):
                cur.execute("insert into keywords(keywordsid,keywordstext,servicekeywordsfk) values(%s,%s,%s)", (keywordsid, _req['keywords'], serviceid))
                cur.execute("update services set keywordsid = %s where idservices = %s",(keywordsid, serviceid))
                conn.commit()
                data = {"serviceId":serviceid, "status":"Keywords added successfully"}
                response = jsonify(data)
                response.status_code = 200
                return response
            else:
                data = {"serviceId":serviceid, "status":"Keywords unsuccessful"}
                response = jsonify(data)
                response.status_code = 200
                return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 200
        return response
    finally:
        cur.close();
        conn.close();

@app.route("/approveService", methods=["POST"])
def approveService():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    sid = request.args.get('sid')
    _req = request.json
    try:
        if apiAuth(token, userid) == True:
            if request.args.get('role') == "AP":
                conn = mysql.connect();
                cur = conn.cursor(pymysql.cursors.DictCursor)
                appId = validateAppId(conn, cur)
                if (appId != 0):
                    cur.execute("insert into approvallog(logid,approverid,approvalText, approvalDate, approvalStatus) values(%s,%s,%s,%s,%s)",
                                (appId, _req["appid"], _req["apptext"], _req["appdate"], _req["appstatus"]))
                    cur.execute("update services set verified = %s, vstatus=%s where idservices = %s", (appId, _req["appstatus"], sid))
                    conn.commit()
                    response = jsonify("success")
                    response.status_code = 200
                    return response
                else:
                    response = jsonify("failedkey")
                    response.status_code = 200
                    return response
            else:
                response = jsonify("false")
                response.status_code = 200
                return response
        else:
            response = jsonify('Unauthorized Access')
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify('Server Error')
        response.status_code = 500
        return response

@app.route('/saveServiceImage', methods = ['POST'])
def imageFunction():
    _req = request.files['myFile']
    print(_req)
    response = jsonify("success")
    response.status_code = 200;
    return response

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def validateKeywordsId(conn, cur):
    try:
        autoGenId = randint(10000,99999)
        while True:
            cur.execute("select * from keywords where keywordsid = %s",(autoGenId))
            rows = cur.fetchall()
            if(len(rows) == 0):
                break
            else:
                autoGenId = randint(10000,99999)
        return autoGenId
    except Exception as e:
        return 0
    
def validatePaymentId(conn, cur):
    try:
        autoGenId = randint(10000,99999)
        while True:
            cur.execute("select * from paymentoptions where idpaymentoptions = %s",(autoGenId))
            rows = cur.fetchall()
            if(len(rows) == 0):
                break
            else:
                autoGenId = randint(10000,99999)
        return autoGenId
    except Exception as e:
        return 0

def validateScheduleId(conn, cur):
    try:
        autoGenId = randint(10000,99999)
        while True:
            cur.execute("select * from scheduletable where scheduleId = %s",(autoGenId))
            rows = cur.fetchall()
            if(len(rows) == 0):
                break
            else:
                autoGenId = randint(10000,99999)
        return autoGenId
    except Exception as e:
        return 0

def validateCompanyId(conn, cur):
    try:
        autoGenId = randint(10000,99999)
        while True:
            cur.execute("select * from companydetails where idcompany = %s",(autoGenId))
            rows = cur.fetchall()
            if(len(rows) == 0):
                break
            else:
                autoGenId = randint(10000,99999)
        return autoGenId
    except Exception as e:
        return 0

def validateContactId(conn, cur):
    try:
        autoGenId = randint(10000,99999)
        while True:
            cur.execute("select * from servicecontactinfo where idserviceContactInfo = %s",(autoGenId))
            rows = cur.fetchall()
            if(len(rows) == 0):
                break
            else:
                autoGenId = randint(10000,99999)
        return autoGenId
    except Exception as e:
        return 0

def validateServiceId(conn, cur):
    try:
        autoGenId = randint(10000,99999)
        while True:
            cur.execute("select * from services where idservices = %s",(autoGenId))
            rows = cur.fetchall()
            if(len(rows) == 0):
                break
            else:
                autoGenId = randint(10000,99999)
        return autoGenId
    except Exception as e:
        return 0

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
        return False
    finally:
        conn.close()
        cur.close()
    
def validateAppId(conn, cur):
    try:
        autoGenId = randint(10000,99999)
        while True:
            cur.execute("select * from approvallog where logid = %s",(autoGenId))
            rows = cur.fetchall()
            if(len(rows) == 0):
                break
            else:
                autoGenId = randint(10000,99999)
        return autoGenId
    except Exception as e:
        return 0

