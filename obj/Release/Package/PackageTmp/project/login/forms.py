from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=80)],render_kw={"type":"email", "class":"form-control", "id":"inputEmail", "placeholder":"Email Address"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=2, max=80)],render_kw={"type":"password", "class":"form-control", "id":"inputPassword","placeholder":"Password"})
    remember = BooleanField('remember me')
