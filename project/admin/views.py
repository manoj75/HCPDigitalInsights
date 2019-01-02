import json
import requests
import adal
import re
import os
import string
import sendgrid
from random import *
from project import db,app
from sendgrid.helpers import mail
from flask import Blueprint,render_template, redirect,url_for,request,flash
from project.models import User ,Profession, Customer,Campaign 
from project.admin.forms import PasswordResetForm,AddNewUserForm,NewCustomerForm,NewCampaignForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

admin_blueprint =   Blueprint(
    'admin',
    __name__,
    template_folder='templates'
)

SENDGRID_API_KEY = str(os.environ['SendGridKey'])
SENDGRID_SENDER = os.environ['SENDGRID_SENDER']
 
def sendGridEmail(to,emailType,userid,password):
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    to_email = mail.Email(to)
    from_email = mail.Email(SENDGRID_SENDER)
    content=""
    if emailType=="newuser":
        subject = 'Your HCPDigital Insights account'
        content = 'userId:'     +   userid+'\n'  
        content = content+'Password:'   +   password+'\n'
        content = content+'url:https://hcpdigitalinsights.azurewebsites.net'              
         
        body = mail.Content('text/plain',content)
    else:
        subject = 'Password reset'
        content = content+'userId:'     +   userid+'\n'  
        content = content+'Password:'   +   password+'\n'
        content = content+'url:https://hcpdigitalinsights.azurewebsites.net'              
        
    message = mail.Mail(from_email, subject, to_email, body)
    response = sg.client.mail.send.post(request_body=message.get())
    print(response.status_code)
    print(response._body)
 

@admin_blueprint.route("/")
@login_required
def Index():
    return render_template('admin/index.html')

@admin_blueprint.route("/newcustomer", methods=['GET', 'POST'])
@login_required
def AddNewCustomer():
    form = NewCustomerForm()
    print(form)
    print(request.method)
    error=None
    if request.method=="GET":
        return render_template('admin/AddNewCustomer.html',newCustomerForm=form)
    else:
        if form.validate_on_submit() :
            exists = db.session.query(Customer.id).filter_by(name=form.customername.data).first() is not None
            print("exists="+str(exists))
            if(exists):
                flash("Customer already exists!")
                return render_template('admin/AddNewCustomer.html',newCustomerForm=form,success=False,error=True)
            else:    
                new_customer = Customer(name=form.customername.data)
                print(new_customer)
                db.session.add(new_customer)
                db.session.commit()
                return render_template('admin/AddNewCustomer.html',newCustomerForm=form,success=True)
        else:
            print(form.errors)
        return render_template('admin/AddNewCustomer.html')

@admin_blueprint.route("/newuser", methods=['GET', 'POST'])
@login_required
def AddNewUser():
    form = AddNewUserForm()
    form.customer.choices=[(customer.id, customer.name) for customer in Customer.query.all()]
    print(form)
    print(request.method)
    blnError=None
    blnSuccess=None
    if request.method=="GET":
        return render_template('admin/AddNewUser.html',newUserForm=form)
    if form.validate_on_submit() :
        username        =   form.username.data
        email           =   form.email.data
        password        =   generateRandomPwd()
        customerid      =   form.customer.data
        firstname       =   form.firstname.data
        lastname        =   form.lastname.data
        isadmin         =   form.isAdmin.data    
        print(isadmin)
        exists = db.session.query(User.id).filter_by(username=username).first() is not None
        print("exists="+str(exists))
        if(exists):
            blnError=True
            blnSuccess=False
            flash("User already exists!")
            #return render_template('admin/AddNewCampaign.html',newCampaignForm=form,success=False,error=True)
        else:
            hashed_password =   generate_password_hash(password, method='sha256')
            new_user = User(username=username, email=email, password=hashed_password,customerid=customerid,firstname=firstname,lastname=lastname,isAdmin=isadmin)
            print(new_user)
            db.session.add(new_user)
            db.session.commit()
            sendGridEmail(email,"newuser",username,password)
            blnSuccess=True
            blnError=False
        return render_template('admin/AddNewUser.html',newUserForm=form,success=blnSuccess,error=blnError)
    else:
        print(form.errors)
    return render_template('admin/AddNewUser.html',newUserForm=form)
        



def generateRandomPwd():
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.punctuation + string.digits
    password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    print ("This is your password : ",password)
    return password

@admin_blueprint.route("/newcampaign", methods=['GET', 'POST'])
@login_required
def AddNewCampaign():
    print(Campaign.query.all())
    form = NewCampaignForm()
    form.customer.choices=[(customer.id, customer.name) for customer in Customer.query.all()]
    print(form)
    print(request.method)
    if request.method=="GET":
        return render_template('admin/AddNewCampaign.html',newCampaignForm=form)
    if form.validate_on_submit() :
        exists = db.session.query(Campaign.id).filter_by(name=form.name.data,customerId=form.customer.data).first() is not None
        print("exists="+str(exists))
        if(exists):
            flash("Campaign already exists!")
            return render_template('admin/AddNewCampaign.html',newCampaignForm=form,success=False,error=True)
        else:
            new_campaign = Campaign(name=form.name.data, customerid=form.customer.data)
            print(new_campaign)
            db.session.add(new_campaign)
            db.session.commit()
            return render_template('admin/AddNewCampaign.html',newCampaignForm=form,success=True)
    else:
        print(form.errors)
        return render_template('admin/AddNewCampaign.html',newCampaignForm=form)


@admin_blueprint.route("/resetpassword")
@login_required
def ResetPassword():
    passwordresetform= PasswordResetForm()
    passwordresetform.customer.choices=[(customer.id, customer.name) for customer in Customer.query.all()]
    passwordresetform.user.choices=[(user.id, user.username) for user in User.query.all()]
    return render_template('admin/resetPassword.html',form=passwordresetform)
