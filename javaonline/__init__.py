import configparser
import logging

from logging.handlers import RotatingFileHandler
from flask import Flask, url_for
from config.database import DbInstance

from javaonline.app import home
from javaonline.blueprints.login.controllers import login

app = Flask(__name__)
db = DbInstance()

app.register_blueprint(home, url_prefix='/') 
app.register_blueprint(login, url_prefix='/login')

def read_config(app):
    config = configparser.ConfigParser()
    try:
        config_location = './config/etc/defaults.cfg'
        config.read(config_location)
        # Config
        app.config['DEBUG'] = config['config']['debug']
        app.config['ip'] = config['config']['ip']
        app.config['port'] = config['config']['port']
        app.config['url'] = config['config']['url']
        # Logging
        app.config['log_file'] = config['logging']['name']
        app.config['log_location'] = config['logging']['location']
        app.config['log_level'] = config['logging']['level']
    except:
        print('Could not read config from: ', config_location)

def configure_logger(app):
    log_path = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_path, maxBytes=1024*1024*10, backupCount=1024)
    file_handler.setLevel(app.config['log_level'])
    formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.setLevel(app.config['log_level'])
    app.logger.addHandler(file_handler)
