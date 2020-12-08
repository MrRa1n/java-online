from flask import Blueprint, render_template, request, redirect, url_for, flash
from javaonline.models.register_form import RegisterForm
from javaonline.models.user import User
from javaonline.models.role import Role
from javaonline.db.base import Session

from datetime import datetime

from flask_login import login_user, logout_user, current_user

session = Session()

register_bp = Blueprint('register', __name__, template_folder='templates')

@register_bp.route('/register', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('challenges.index'))

    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    elif form.validate_on_submit():
        role = Role('user')

        user = User(username=form.username.data, email=form.email.data, password=form.password.data, role=role)

        user.set_experience_points(0)
        user.set_created_on(datetime.now())
        user.set_last_login(None)

        session.add(user)
        session.commit()
        session.close()

        return redirect(url_for('login.index'))

        # flash('Welcome back, {}'.format(form.username.data))
    return render_template('register.html', form=form)
