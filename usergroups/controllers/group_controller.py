import urllib
from flask import request
from flask.ext.restful import Resource, abort, reqparse

from usergroups.models import Group, User, UserInGroup
from usergroups.utils.exceptions import PrimaryKeyException

class GroupController(Resource):

    '''API Routes'''
    def get(self, group_name=None):
        group = self.require_group(group_name)
        return getattr(group, 'users', [])

    def post(self):
        # TODO: create generic parser
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Unique group name')

        args = parser.parse_args()
        arg_dict = {k : v for k,v in args.iteritems()}

        group = Group(arg_dict)
        try:
            if group.insert():
                return "{0} inserted".format(group.group_name)
            else:
                abort(400)
        except PrimaryKeyException as e:
            abort(403)
        except:
            abort(400)

    def put(self, group_name=None):
        # TODO: create generic parser
        users = request.json
        if users is None:
            abort(400)
        group = self.require_group(group_name)
        filtered_users = [userid for userid in users if User(userid).exists_in_db()]
        group.update(filtered_users)
        return "{0} updated".format(group_name)


    def delete(self, group_name=None):
        group = self.require_group(group_name)
        if group.delete():
            delete_query = {'group_name': group_name}
            UserInGroup.delete_many(delete_query)
            return "{0} deleted".format(group_name)
        abort(400)

    '''Helper functions'''
    def require_group(self, group_name):
        # Initialize group, return 404 if it doesn't exist in db
        unescaped_group_name = urllib.unquote_plus(group_name)
        group = Group(unescaped_group_name)
        if not group.exists_in_db():
            abort(404)
        return group