import configparser
import logging

from logging.handlers import RotatingFileHandler
from flask import Flask, url_for
from flask_mongoengine import MongoEngine

app = Flask(__name__)
db = MongoEngine()
db.init_app(app)

@app.route('/')
def root():
    app.logger.info('Endpoint hit: ' + url_for('.root'))
    return 'Hello, World!'

@app.route('/config')
def config():
    app.logger.info('Endpoint hit: ' + url_for('.config'))
    s = []
    s.append('debug: ' + str(app.config['DEBUG']))
    s.append('ip: ' + app.config['ip'])
    s.append('port: ' + app.config['port'])
    s.append('url: ' + app.config['url'])
    return ', '.join(s)

def init(app):
    config = configparser.ConfigParser()
    try:
        config_location = 'etc/defaults.cfg'
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

def logs(app):
    log_path = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_path, maxBytes=1024*1024*10, backupCount=1024)
    file_handler.setLevel(app.config['log_level'])
    formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.setLevel(app.config['log_level'])
    app.logger.addHandler(file_handler)

init(app)
logs(app)

if __name__ == '__main__':
    init(app)
    logs(app)
    app.run(host=app.config['ip'], port=app.config['port'])
