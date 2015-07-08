from flask import Flask

from usergroups.db import Db
from controllers.user_controller import UserController
from controllers.group_controller import GroupController

app = Flask(__name__)
app.db = Db