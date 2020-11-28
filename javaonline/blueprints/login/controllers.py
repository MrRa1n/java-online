from flask import Blueprint, render_template

login = Blueprint('login', __name__, template_folder='templates')

@login.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')
