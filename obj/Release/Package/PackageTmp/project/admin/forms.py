from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField,SelectField
from wtforms.validators import InputRequired, Email, Length

class AddNewUserForm(FlaskForm):
    username        =   StringField('username',validators=[InputRequired(), Length(max=80)],render_kw={ "class":"form-control", "id":"inputUsername", "placeholder":"User Name"})
    email           =   StringField('email',validators=[InputRequired()],render_kw={"type":"email", "class":"form-control", "id":"inputEmail", "placeholder":"Email Address"})
    customer        =   SelectField('customer',coerce =int, render_kw={ "class":"form-control", "id":"inputCustomer"})
    firstname       =   StringField('fname',validators=[InputRequired()],render_kw={"class":"form-control", "id":"inputFname", "placeholder":"First Name"})
    lastname        =   StringField('lname',validators=[InputRequired()],render_kw={"class":"form-control", "id":"inputLname", "placeholder":"Last Name"})
    isAdmin         =   BooleanField('Admin User')
    salesForceID    =   StringField('salesforceid',validators=[InputRequired()],render_kw={"class":"form-control", "id":"inputsalesforceid", "placeholder":"Salesforce ID"})
    
class NewCampaignForm(FlaskForm):
    name        =   StringField('campaignname',validators=[InputRequired(), Length(max=80)],render_kw={ "class":"form-control", "id":"inputCampaignName", "placeholder":"Campaign Name"})
    customer    =   SelectField('customer',coerce =int, render_kw={ "class":"form-control", "id":"inputCustomer"})

class NewCustomerForm(FlaskForm):
    customername=   StringField('customername',validators=[InputRequired()],render_kw={"class":"form-control", "id":"inputCustomername", "placeholder":"Customer Name"})
    salesForceID=   StringField('salesforceid',validators=[InputRequired()],render_kw={"class":"form-control", "id":"inputsalesforceid", "placeholder":"Salesforce ID"})

class PasswordResetForm(FlaskForm):
    customer    =   SelectField('customer',coerce =int, render_kw={ "class":"form-control", "id":"inputCustomer"})
    user        =   SelectField('campaignname',coerce =int,render_kw={ "class":"form-control", "id":"inputuserName"})
    