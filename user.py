import pymysql
import random as random
import string
from utils import apiAuth as apiAuth
import security as auth
from app import app
from utils.DbConfig import mysql
from utils.searchImpl import getKeywords
from flask import jsonify
from flask import request


@app.route('/user', methods = ['GET'])
def user():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("select * from user")
        rows = cur.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        return response
    except Exception as e:
        return e
    finally:
        cur.close();
        conn.close();

@app.route('/newUser', methods = ['POST'])
def adduser():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        _req = request.json
        print(_req)
        _encrpass = auth.encrypt_password(_req['password'])
        cur.execute("insert into user(email, firstName,lastName,password,phone,init,role) values(%s, %s, %s, %s, %s, %s, %s)",
                    (_req['userid'],_req['fname'], _req['lname'],_encrpass,_req['phone'], _req['initial'], 'user'))
        conn.commit();
        resp = jsonify('User added successfully')
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify(e)
        resp.status_code = 500
        return resp
    finally:
        cur.close()
        conn.close()

@app.route('/validateId', methods = ['GET'])
def validateUserId():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        userid = request.args.get('userid')
        cur.execute("select * from user where userid = '" + userid + "';");
        rows = cur.fetchall()
        if len(rows) == 0:
            response = jsonify('true')
        else:
            response = jsonify('false')
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify('Error occured')
        response.status_code = 500
        return response
    finally:
        conn.close()
        cur.close()

@app.route('/authenticate',methods = ['POST'])
def userAuth():
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("select password,role from user where email = '" + request.json['userid'] + "';")
        rows = cur.fetchall()
        if len(rows) == 0:
            response = jsonify('InvalidUser')
        else:
            check = auth.check_encrypted_password(request.json['password'], rows[0]['password'])
            if check == True:
                response = {"key" : generateKey(request.json['userid']), "role" : rows[0]['role']}
                response = jsonify(response)
                print(response)
                if response == False:
                    response = jsonify('False')
            else:
                response = jsonify('AuthenticationFailed')
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify('Error occured')
        response.status_code = 500
        print(e)
        return response
    finally:
        conn.close()
        cur.close()

def generateKey(user):
    rand = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(12)])
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("update user set token = %s where email = '" + user + "';",rand)
        conn.commit();
        return rand
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()
        cur.close()


@app.route('/userInfo',methods=['GET'])
def getUserInfo():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    print(userid+" "+token)
    try:
        if apiAuth.apiAuth(token, userid) == True:
            conn = mysql.connect();
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("Select email, firstName, lastName, phone, init, role from user where email='"+userid+"';")
            rows = cur.fetchall()
            response = jsonify(rows)
            response.status_code = 200
            return response
        else:
            response = jsonify('Unauthorized Access')
            response.status_code = 200
            return response
    except Exception as e:
        print(e)
        response = jsonify('Server Error')
        response.status_code = 500
        return response

@app.route('/editUserInfo', methods = ['POST'])
def editProfile():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    try:
        if apiAuth.apiAuth(token, userid) == True:
            conn = mysql.connect();
            cur = conn.cursor(pymysql.cursors.DictCursor)
            _req = request.json
            cur.execute("update user set firstName = %s, lastName = %s, phone = %s where email = %s",(_req['fname'],_req['lname'],_req['phone'],userid))
            conn.commit()
            response = jsonify("success")
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

@app.route("/changePass", methods = ['POST'])
def changePassword():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    try:
        if apiAuth.apiAuth(token, userid) == True:
            conn = mysql.connect();
            cur = conn.cursor(pymysql.cursors.DictCursor)
            _req = request.json
            cur.execute("select password from user where email = %s;",(userid))
            rows = cur.fetchall()
            check = auth.check_encrypted_password(_req['curPass'], rows[0]['password'])
            if check == True:
                _encrpass = auth.encrypt_password(_req['newPass'])
                cur.execute("update user set password = %s where email = %s", (_encrpass,userid))
                conn.commit()
                response = jsonify("success")
            elif check == False:
                response = jsonify("invalid")
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

@app.route('/newAdminUser', methods = ['POST'])
def addadminuser():
    adKey = "v(i'7#5x>~}>n.j3H:F)*T),D-Er~1L6g|RPtRI$S)1VSvL/u/sanFP0PZ<9S0q"
    uKey = "17TZ27vRus"
    try:
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        _req = request.json
        if _req['role'] == "AD":
            if adKey == _req['key']:
                _encrpass = auth.encrypt_password(_req['password'])
                cur.execute("insert into user(email, firstName,lastName,password,phone,init,role) values(%s, %s, %s, %s, %s, %s, %s)",
                            (_req['userid'],_req['fname'], _req['lname'],_encrpass,_req['phone'], _req['initial'], _req['role']))
                conn.commit();
                resp = jsonify('User added successfully')
                resp.status_code = 200
            else:
                resp = jsonify('Incorrect Key')
                resp.status_code = 200
        elif _req['role'] == "DE" or _req['role'] == "AP":
            if uKey == _req['key']:
                _encrpass = auth.encrypt_password(_req['password'])
                cur.execute("insert into user(email, firstName,lastName,password,phone,init,role) values(%s, %s, %s, %s, %s, %s, %s)",
                            (_req['userid'],_req['fname'], _req['lname'],_encrpass,_req['phone'], _req['initial'], _req['role']))
                conn.commit();
                resp = jsonify('User added successfully')
                resp.status_code = 200
            else:
                resp = jsonify('Incorrect Key')
                resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify(e)
        resp.status_code = 500
        return resp
    finally:
        cur.close()
        conn.close()

@app.route("/getCompaniesForApproval", methods=['GET'])
def getApCompanies():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    try:
        if apiAuth.apiAuth(token, userid) == True:
            if request.args.get('role') == "AP":
                conn = mysql.connect();
                cur = conn.cursor(pymysql.cursors.DictCursor)
                _req = request.json
                cur.execute("select idservices, name, building, street, landmark, area, pincode, state, country, companyid, serviceUserFK from services where verified=0;")
                conn.commit()
                response = jsonify(cur.fetchall())
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

@app.route("/getServiceInfo", methods=["GET"])
def getServiceInfo():
    userid = request.args.get('userid')
    token = request.args.get('tok')
    sid = request.args.get('sid')
    response = {}
    try:
        if apiAuth.apiAuth(token, userid) == True:
            if request.args.get('role') == "AP":
                conn = mysql.connect();
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute("select idservices, services.name, building, street, landmark, area, pincode, state, country, contactid, serviceUserFK, scheduleid, paymentid, keywordsid, companyId from services where idservices=%s;",(sid))
                rows = cur.fetchall()
                if rows[0]["companyId"]!=0:
                    cur.execute("select * from companydetails where idcompany=%s",(rows[0]["companyid"]))
                    rowsDat = cur.fetchall()
                    response = {"company": rowsDat}
                cur.execute("select * from servicecontactinfo where idserviceContactInfo=%s",(rows[0]["contactid"]))
                rowsDat = cur.fetchall()
                response["contactInfo"] = rowsDat
                cur.execute("select * from scheduletable where scheduleId=%s",(rows[0]["scheduleid"]))
                rowsDat = cur.fetchall()
                response["schedule"] = rowsDat
                cur.execute("select * from paymentoptions where idpaymentoptions=%s", (rows[0]["paymentid"]))
                rowsDat = cur.fetchall()
                response["payment"] = rowsDat
                cur.execute("select * from keywords where keywordsid=%s", (rows[0]["keywordsid"]))
                rowsDat = cur.fetchall()
                response["keywords"] = rowsDat
                cur.execute("select firstName,lastName,phone from user where email=%s", (rows[0]["serviceUserFK"]))
                rowsDat = cur.fetchall()
                response["user"] = rowsDat
                response["service"] =  rows
                response = jsonify(response)
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
        print("hellooo")
        response = jsonify('Server Error')
        response.status_code = 500
        return response

@app.route("/find", methods=["POST"])
def findService():
    try:
        _req = request.json
        text = _req["searchText"]
        print(text)
        tokens = getKeywords(text)
        resultServices = []
        serviceData = []
        print(tokens)
        conn = mysql.connect();
        cur = conn.cursor(pymysql.cursors.DictCursor)
        for i in tokens:
            cur.execute("select servicekeywordsfk from keywords where keywordstext like '%" + i + "%'")
            temp = cur.fetchall()
            for i in temp:
                print(i["servicekeywordsfk"])
                resultServices.append(i["servicekeywordsfk"])
        resultServices = list(set(resultServices))
        for i in resultServices:
            cur.execute("SELECT idservices, services.name, building, street, landmark, area, pincode, state, country, companyid, serviceUserFK FROM services join servicecontactinfo on services.idservices = servicecontactinfo.servicecontackfk join scheduletable on scheduletable.serviceId = services.idservices  where services.idservices = %s",(i))
            serviceData.append(cur.fetchall()[0])
        print(serviceData)
        response = jsonify(serviceData)
        return response
    except Exception as e:
        print(e)

@app.route("/forgotPass", methods = ['POST'])
def forgotPassword():
    userid = request.args.get('userid')
    try:
        conn = mysql.connect();
        cur = conn.cursor(pymysql.cursors.DictCursor)
        _req = request.json
        _encrpass = auth.encrypt_password(_req['newPass'])
        print(_encrpass)
        cur.execute("update user set password = %s where email = %s", (_encrpass,userid))
        conn.commit()
        response = jsonify("success")
        return response
    except Exception as e:
        print(e)
        response = jsonify('Server Er7ror')
        response.status_code = 500
        return response

@app.route('/getPh',methods = ['GET'])
def getphone():
    userid = request.args.get('userid')
    try:
        conn = mysql.connect();
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("select phone from user where email = %s;",(userid))
        rows = cur.fetchall()
        conn.commit()
        response = jsonify(rows)
        return response
    except Exception as e:
        print(e)
        response = jsonify('Server Er7ror')
        response.status_code = 500
        return response

if __name__ == "__main__" :
    app.run(debug=True)

