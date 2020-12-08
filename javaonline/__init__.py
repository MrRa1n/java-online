from flask_login import LoginManager
from flask import Flask

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = 'login.index'