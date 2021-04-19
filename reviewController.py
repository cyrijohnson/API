from app import app
from utils.DbConfig import mysql
from utils.searchImpl import getKeywords
from flask import jsonify
from flask import flash,request

# @app.route("/addReview", methods = ["POST"])
#
# @app.route("/getMyServiceReviews", methods = ["GET"])
#
# @app.route("/getMyReviews", methods = ["GET"])