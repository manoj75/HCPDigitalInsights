from flask import Blueprint,render_template, redirect,url_for,request,flash
from project.users.forms import UserForm
from project.models import *

users_blueprint =   Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

@users_blueprint.route("/")
def hello():
    return "HCPDigitalInsights!"

#@users_blueprint.route('/login')
#def login():
#    return render_template('users/login.html')    