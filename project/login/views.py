import os
from flask import Blueprint,render_template, redirect,url_for,request,flash
from project.users.forms import UserForm
from project.models import *
from werkzeug.security import  generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from project.login.forms import LoginForm
from project import app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'



login_blueprint =   Blueprint(
    'login',
    __name__,
    template_folder='templates'
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))


@login_blueprint.route("/", methods=['GET', 'POST'])
def login():
    customerName=""
    form = LoginForm()
    print("sdasdasdasdasdadsadsads")
    print(form.username.data)
    print("sdasdasdasdasdadsadsads")
    print(request.method)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print("LOGIN")
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                print("CustomerID="+str(user.customerid))
                customerName=Customer.query.get(user.customerid).name
                print("CuatomerName="+customerName)
                print(current_user)
                return redirect(url_for('dashboard.Index'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    else:
        print(form.errors)

    return render_template('login/login-mdg.html', form=form)

#@users_blueprint.route('/login')
#def login():
#    return render_template('users/login.html')    

    
