from flaskext.mysql import MySQL
import sys
sys.path.insert(1, 'C:\\Users\\I517463\\Desktop\\NilgiriConnect\\API')
from app import app
mysql = MySQL()
#My SQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'nilgiriconnect'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)
