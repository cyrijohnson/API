import pymysql
import sys
from random import randint
import string
import security as auth
import apiAuth as apiAuth
from app import app
from utils.DbConfig import mysql
from flask import jsonify
from flask import flash,request

@app.route('/getMyCompaniesServices', methods = ['GET'])
def getCompanyServices():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    try:
        if apiAuth.apiAuth(token, userid) == True:
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("select * from companydetails where emailKey=%s",(userid))
            companies = cur.fetchall()
            response = {"companyCount":len(companies), "companiesList" :companies}
            cur.execute("select * from services where serviceUserFK=%s",(userid))
            services = cur.fetchall()
            response["serviceCount"] = len(services)
            response["serviceList"] = services
            response = jsonify(response)
            response.status_code = 200
            return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 500
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/getMyServiceMoreInfo', methods=['GET'])
def getMyMoreInfo():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    serviceid = request.args.get('serviceId')
    try:
        if apiAuth.apiAuth(token, userid):
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("select * from servicecontactinfo where servicecontackfk=%s",(serviceid))
            response = {"contact":cur.fetchall()}
            cur.execute("select * from scheduletable where serviceId=%s",(serviceid))
            response["schedule"] = cur.fetchall()
            cur.execute("select * from keywords where servicekeywordsfk=%s",(serviceid))
            response["keywords"] = cur.fetchall()
            response = jsonify(response)
            response.status_code = 200
            return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 500
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/updateCompany', methods = ["POST"])
def updateCompany():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    try:
        if apiAuth.apiAuth(token, userid):
            _req = request.json
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("update companydetails set name = %s, city = %s, phone = %s, mobile = %s, firstName = %s, lastName = %s where idcompany = %s",(
                _req['compName'], _req['compCity'], _req['compPhone'], _req['compMob'], _req['compFName'], _req['compLName'], _req['compId']
            ))
            conn.commit()
            response = jsonify("success")
            response.status_code = 200
            return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 500
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/updateCompanyGroup', methods = ["POST"])
def updateCompanyGrouping():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    try:
        if apiAuth.apiAuth(token, userid):
            _req = request.json
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("update services set companyId = %s where idservices=%s",(
                _req['compId'], _req['servId']
            ))
            conn.commit()
            response = jsonify("success")
            response.status_code = 200
            return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 500
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/updateServiceInfo', methods = ["POST"])
def updateServiceInfo():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    try:
        if apiAuth.apiAuth(token, userid):
            _req = request.json
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("update services set name = %s, building=%s, street=%s, landmark=%s, area=%s, pincode=%s, state=%s, country=%s where idservices=%s",(
                _req['sname'],_req['sbuilding'],_req['sstreet'],_req['slandmark'],_req['sarea'],_req['spincode'],_req['sstate'],_req['scountry'], _req['servId']
            ))
            conn.commit()
            response = jsonify("success")
            response.status_code = 200
            return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 500
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/getContactInfo', methods = ["GET"])
def getContactInfo():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    contactId = request.args.get('conId')
    try:
        if apiAuth.apiAuth(token, userid):
            _req = request.json
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("select * from servicecontactinfo where idserviceContactInfo=%s", contactId)
            response = jsonify(cur.fetchall())
            response.status_code = 200
            return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 500
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/updateServiceContact', methods = ['POST'])
def updateServiceContact():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    _req = request.json
    try:
        if apiAuth.apiAuth(token, userid) == True:
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("update servicecontactinfo set name=%s, phone=%s, cell=%s, fax=%s, tollfree=%s, email=%s, website=%s, facebook=%s, twitter=%s, instagram=%s, youtube=%s where idserviceContactInfo=%s",
                        (_req['conPerson'], _req['conPhone'], _req['conMobile'], _req['conFax'], _req['conTollfree'], _req['conEmail'], _req['conWebsite'], _req['conFacebook'],
                         _req['conTwitter'],_req['conInstagram'],_req['conYoutube'], _req['conId']))
            conn.commit()
            response = jsonify("success")
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

@app.route('/getScheduleInfo', methods = ["GET"])
def getScheduleInfo():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    schId = request.args.get('schId')
    pId = request.args.get('pId')
    try:
        if apiAuth.apiAuth(token, userid):
            _req = request.json
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("select * from scheduletable where scheduleId=%s", schId)
            response = {"schedule":cur.fetchall()}
            cur.execute("select * from paymentoptions where idpaymentoptions=%s", int(pId))
            response["payment"] = cur.fetchall()
            response = jsonify(response)
            response.status_code = 200
            return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 500
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/updateServiceSchedule', methods = ['POST'])
def updateServiceSchedule():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    _req = request.json
    try:
        if apiAuth.apiAuth(token, userid) == True:
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            scheduleid = _req['schid']
            paymentid = _req['pid']
            cur.execute("update scheduletable set monStart=%s, monEnd=%s, tueStart=%s, tueEnd=%s, wedStart=%s, wedEnd=%s, thurStart=%s, thurEnd=%s, friStart=%s, friEnd=%s, satStart=%s, satEnd=%s, sunStart=%s, sunEnd=%s where scheduleId=%s",
                        (_req['monBeg'], _req['monEnd'], _req['tueBeg'], _req['tueEnd'], _req['wedBeg'], _req['wedEnd'], _req['thurBeg'], _req['thurEnd'],
                         _req['friBeg'],_req['friEnd'],_req['satBeg'], _req['satEnd'], _req['sunBeg'], _req['sunEnd'], scheduleid))
            conn.commit()
            cur.execute("update paymentoptions set cash=%s,card=%s,onlinepayments=%s where idpaymentoptions=%s",
                        (_req['cash'], _req['card'], _req['digi'], paymentid))
            conn.commit()
            response = jsonify("success")
            response.status_code = 200
            return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error"+e)
        response.status_code = 500
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/getKeywords', methods = ["GET"])
def getKeywords():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    kId = request.args.get('kId')
    try:
        if apiAuth.apiAuth(token, userid):
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("select * from keywords where keywordsid=%s", kId)
            response = cur.fetchall()
            response = jsonify(response)
            response.status_code = 200
            return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 500
        return response
    finally:
        cur.close();
        conn.close();

@app.route('/updateKeywords', methods = ["POST"])
def updateKeywords():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    try:
        if apiAuth.apiAuth(token, userid):
            _req = request.json
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("update keywords set keywordstext=%s where keywordsid=%s", ( _req['keywords'], _req['keywordid'],))
            conn.commit()
            response = jsonify("success")
            response.status_code = 200
            return response
        else:
            response = jsonify("Not Authorized")
            response.status_code = 401
            return response
    except Exception as e:
        print(e)
        response = jsonify("Database Error")
        response.status_code = 500
        return response
    finally:
        cur.close();
        conn.close();


        
    





            
