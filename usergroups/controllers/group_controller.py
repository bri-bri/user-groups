from flask.ext.restful import Resource, abort, reqparse

from usergroups.models.group import Group

class GroupController(Resource):

    def get(self, group_name=None):
        group = Group(group_name)
        if not group:
            abort(404)
        return group.pickle()

    def post(self):
        # __TODO: create user parser util
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Unique group name')

        args = parser.parse_args()
        group = Group.create(args)
        group.save()

    def put(self, group_name=None):
        # __TODO: create user parser util

        parser = reqparse.RequestParser()
        parser.add_argument('users', type=list, required=True, help='Unique user ID')

        args = parser.parse_args()
        group = Group(group_name)
        return "TODO"

    def delete(self, group_name=None):
        return "TODO"
