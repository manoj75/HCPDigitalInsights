import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_migrate import Migrate
#import pyodbc
import urllib.parse 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
modus = Modus(app)
logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)
logHandler.setLevel(logging.INFO)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(logHandler)  

DBServer   = os.environ['DBServer']
DataBase    = os.environ['DataBase']
DBUserID    = os.environ['DBUserID']
DBPassword  = os.environ['DBPassword']
print(DBServer)
print(DataBase)
print(DBUserID)
print(DBPassword)

#DBServer="hcpdigitalinsights.database.windows.net"
#DataBase="HCPDigitalInsights"
#DBUserID="hcpdigital"
#DBPassword="Hcp123digital"

params = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER="+DBServer+";DATABASE="+DataBase+";UID="+DBUserID+";PWD="+DBPassword)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "THIS SHOULD BE HIDDEN!"
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['TESTING'] = False
db = SQLAlchemy(app)
print(db)
migrate = Migrate(app, db)

# import a blueprint that we will create
from project.users.views import users_blueprint
from project.dashboard.views import dashboard_blueprint
from project.login.views import login_blueprint
from project.admin.views import admin_blueprint

from project.models import Profession,SpecialtyGroup,GeoRegions,Segment,Customer,User

# register our blueprints with the application
app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
app.register_blueprint(login_blueprint, url_prefix='/login')
app.register_blueprint(admin_blueprint,url_prefix='/admin')

@app.context_processor
def filters():
#    professions=Profession.query.all()
#    specialtyGroups=SpecialtyGroup.query.all()
#    geoRegions=GeoRegions.query.all()
#    Segments=Segment.query.all()
    print("--------------------------")
    print(current_user.is_authenticated)
    if(current_user.is_authenticated):
        customerName=Customer.query.get(current_user.customerid).name
    else:
        customerName=""
    print("Customer Name="+customerName)
    print("--------------------------")
    return dict(customer_name=customerName)

@app.route('/')
def root():
    #return "HELLO BLUEPRINTS!"
    return redirect(url_for('login.login'))