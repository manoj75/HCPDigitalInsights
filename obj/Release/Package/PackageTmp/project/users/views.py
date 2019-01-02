from project.models import *
from flask import Blueprint,render_template, redirect,url_for,request,flash
from project.users.forms import UserForm,ChangePasswordForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

users_blueprint =   Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

@users_blueprint.route("/")
def hello():
    return "HCPDigitalInsights!"


@users_blueprint.route('/changePassword/<userid>', methods=['GET', 'POST'])
@login_required
def changePassword(userid):
    form = ChangePasswordForm()
    print(form.errors)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        user = current_user
        print("------------------------------")
        print("current password")
        print(form.currentpassword.data)
        print(user.password)
        #print(user.verify_password(form.currentpassword.data))
        print("------------------------------")
        if check_password_hash(user.password, form.currentpassword.data):
            user.password = generate_password_hash(form.newpassword.data, method='sha256')
            db.session.add(user)
            db.session.commit()
            flash('Your password was successfully changed.')
            #return redirect(index_url_for_blueprint(current_user))
        else:
            print("invalid current Password")
            form.currentpassword.errors.append('Invalid password.')
    else:
        print(form.errors)
    return render_template('users/change-password.html', form=form)

#@users_blueprint.route('/login')
#def login():
#    return render_template('users/login.html')    