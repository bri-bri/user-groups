import logging
import os
from flask import Flask

from utils import LogHelper
from usergroups.db import Db
from usergroups.config import Config

def init_db():
    return Db()

env = os.getenv('USERGROUP_ENV')

config_map = {
    'PRODUCTION': 'ProductionConfig',
    'DEVELOPMENT': 'DevelopmentConfig',
    'TESTING': 'TestingConfig'
}

'''Initialize'''
app = Flask(__name__)
db = init_db()

config_class = config_map.get(env, 'Config')
app.config.from_object("usergroups.config." + config_class)
app.logger.setLevel(app.config['LOG_LEVEL'])
logger = LogHelper(app.logger)