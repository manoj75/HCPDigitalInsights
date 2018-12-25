from project import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id          =   db.Column(db.Integer, primary_key=True)
    username    =   db.Column(db.String(15), unique=True)
    email       =   db.Column(db.String(50), unique=True)
    password    =   db.Column(db.String(80))
    first_name  =   db.Column(db.String(80))
    last_name  =   db.Column(db.String(80))
    customerid  =   db.Column(db.Integer)

    #customer    =   db.relationship("Customer")

    def __init__(self, username, email,password,customerid,firstname,lastname):
        self.username = username
        self.email = email
        self.password=password
        self.first_name=firstname
        self.last_name=lastname
        self.customerid=customerid

class Customer(db.Model):
    __tablename__ = 'Customers'

    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.Text)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name):
        self.name = name


class Profession(db.Model):
    __tablename__ = 'Profession'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    campaignId = db.Column(db.Integer)

    def __init__(self, name, campaignid):
        self.name = name
        self.campaignId = campaignid        

class SpecialtyGroup(db.Model):
    __tablename__ = 'SpecialtyGroup'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    campaignId = db.Column(db.Integer)

    def __init__(self, name, campaignid):
        self.name = name
        self.campaignId = campaignid                

class GeoRegions(db.Model):
    __tablename__ = 'GeoRegion'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    campaignId = db.Column(db.Integer)

    def __init__(self, name, campaignid):
        self.name = name
        self.campaignId = campaignid                        

class Segment(db.Model):
    __tablename__ = 'Segment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    campaignId = db.Column(db.Integer)

    def __init__(self, name, campaignid):
        self.name = name
        self.campaignId = campaignid                        


class Campaign(db.Model):
    __tablename__ = 'Campaigns'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.Text)
    customerId  = db.Column(db.Integer)
    def __init__(self, name, customerid):
        self.name       = name
        self.customerId = customerid