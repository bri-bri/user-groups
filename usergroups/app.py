from flask import Flask
#from flask.ext.restful import Api

from controllers.user_controller import UserController
from controllers.group_controller import GroupController

app = Flask(__name__)
#api = Api(app)

#api.add_resource(UserController, '/users/', '/users/<string:userid>')
#api.add_resource(GroupController, '/groups/', '/groups/<string:group_name>')

#if __name__ == '__main__':
#    app.run()