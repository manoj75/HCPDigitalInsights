from flask_wtf import FlaskForm
from wtforms import StringField, validators
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import InputRequired, Email, Length, EqualTo

class UserForm(FlaskForm):
    first_name=StringField('First Name',[validators.DataRequired])
    last_name= StringField('First Name',[validators.DataRequired])



class ChangePasswordForm(FlaskForm):
    username            =   StringField('username'          ,render_kw={"class":"form-control", "id":"inputcurrentpassword","readonly": True})
    currentpassword     =   StringField('currentpassword'   ,validators=[InputRequired()],render_kw={"class":"form-control", "id":"inputcurrentpassword", "placeholder":"Current Password"})
    newpassword         =   StringField('newpassword'       ,validators=[InputRequired(), Length(min=4, max=80)],render_kw={"class":"form-control", "id":"inputNewPassword", "placeholder":"New Password"})
    confirmpassword     =   StringField('confirmpassword'   ,validators=[InputRequired(),EqualTo('newpassword')],render_kw={"class":"form-control", "id":"inputConfirmPassword", "placeholder":"Confirm Password"})

    