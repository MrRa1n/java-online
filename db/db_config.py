import configparser

from flask_mongoengine import MongoEngine


db = None
my_app = None

class DbInstance:
    __instance = None

    @staticmethod
    def getInstance():
        if DbInstance.__instance == None:
            DbInstance(my_app)
        return DbInstance.__instance

    def __init__(self, app):
        self.DB_URI = read_credentials()
        my_app = app
        if DbInstance.__instance != None:
            raise Exception("Instance already exists!")
        else:
            db = MongoEngine()
            db.init_app(my_app)

            DbInstance.__instance = self

def read_credentials():
    config = configparser.ConfigParser()
    try:
        config.read('etc/database.cfg')
        db_name = config['mongo_credentials']['db_name']
        db_pass = config['mongo_credentials']['db_pass']

        db_uri = 'mongodb+srv://tcook:{}@pythoncluster.88bdg.mongodb.net/{}?retryWrites=true&w=majority'.format(db_pass, db_name)

    except:
        print('Could not read database config!')

    return db_uri
