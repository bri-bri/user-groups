from flask.ext.restful import Resource, abort, reqparse

from usergroups.models.user import User


class UserController(Resource):

    def get(self, userid):
        return "TODO"

    def post(self):
        # __TODO: create user parser util
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str, required=True, help='Unique user ID')
        parser.add_argument('first_name', type=str, required=True, help='User\'s first name')

        user = User.create()
        user.save()

    def put(self, userid):
        return "TODO"

    def delete(self, userid):
        return "TODO"
