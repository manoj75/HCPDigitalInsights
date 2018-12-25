import json
import requests
import adal
import re
#from flask_sendgrid import SendGrid
import sendgrid
from sendgrid.helpers import mail

import os
from project import db,app
from flask import Blueprint,render_template, redirect,url_for,request,flash
from project.models import User ,Profession, Customer,Campaign 
from project.admin.forms import AddNewUserForm,NewCustomerForm,NewCampaignForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

admin_blueprint =   Blueprint(
    'admin',
    __name__,
    template_folder='templates'
)

#app.config['SENDGRID_API_KEY'] = str(os.environ['SendGridKey'])
#app.config['SENDGRID_DEFAULT_FROM'] = 'admin@hcpdigitalinsights.com'

SENDGRID_API_KEY = str(os.environ['SendGridKey'])
SENDGRID_SENDER = os.environ['SENDGRID_SENDER']

#mail = SendGrid(app)

 
def sendGridEmail():
    to = "manoj75@gmail.com"
    #if not to:
        #return ('Please provide an email address in the "to" query string '
        #        'parameter.'), 400
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    to_email = mail.Email(to)
    from_email = mail.Email(SENDGRID_SENDER)
    subject = 'This is a test email'
    content = mail.Content('text/plain', 'Example message.')
    message = mail.Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=message.get())
    print(response.status_code)
    print(response._body)
    #if response.status_code != 202:
        #return 'An error occurred: {}'.format(response.body), 500
    #return 'Email sent.'

 

@admin_blueprint.route("/")
@login_required
def Index():
    sendGridEmail()
    return render_template('admin/index.html')

@admin_blueprint.route("/newcustomer", methods=['GET', 'POST'])
@login_required
def AddNewCustomer():
    form = NewCustomerForm()
    print(form)
    print(request.method)
    if request.method=="GET":
        return render_template('admin/AddNewCustomer.html',newCustomerForm=form)
    if request.method=="POST":
        print(form.validate_on_submit())
    if form.validate_on_submit() :
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
    if request.method=="GET":
        return render_template('admin/AddNewUser.html',newUserForm=form)
    if request.method=="POST":
        print(form.validate_on_submit())
    if form.validate_on_submit() :
        # code to process form
        #print("Validated")
        #hashed_password = generate_password_hash(form.password.data, method='sha256')
        hashed_password = generate_password_hash("123", method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password,customerid=form.customer.data,firstname=form.firstname.data,lastname=form.lastname.data)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return render_template('admin/AddNewUser.html',newUserForm=form,success=True)
    else:
        print("1111="+form.customer.data)
        print(form.errors)
    return render_template('admin/AddNewUser.html',newUserForm=form)
        

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
    if request.method=="POST":
        print(form.validate_on_submit())
    if form.validate_on_submit() :
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
    return render_template('admin/resetPassword.html')
