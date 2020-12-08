from flask import Blueprint, render_template, request, redirect, url_for, flash
from javaonline.models.login_form import LoginForm
from javaonline.models.user import User
from javaonline.db.base import Session

from flask_login import login_user, logout_user, current_user

session = Session()

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('challenges.index'))

    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif form.validate_on_submit():

        user = session.query(User).filter(User.username == form.username.data).first()

        if user == None or not user.check_password(form.password.data):
            form.submit.errors.append('Username or password is incorrect')
            # return redirect(url_for('login.index'))
            return render_template('login.html', form=form)

        login_user(user)
        return redirect(url_for('challenges.index'))

        # flash('Welcome back, {}'.format(form.username.data))

@login_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login.index'))
