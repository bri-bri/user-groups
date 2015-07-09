import urllib
from flask.ext.restful import Resource, abort, reqparse

from usergroups import logger
from usergroups.models import User
from usergroups.utils.exceptions import PrimaryKeyException

class UserController(Resource):

    '''API Routes'''
    def get(self, userid):
        logger.logger.debug("GETTING")
        user = self.require_user(userid)
        return user.pickle()

    def post(self):
        logger.logger.debug("POSTING")
        args = self.parse_args()
        user = User(args)
        try:
            if user.insert():
                return "{0} inserted".format(user.userid)
        except PrimaryKeyException as e:
            abort(403)
        finally:
            abort(400)


    def put(self, userid):
        args = self.parse_args(False)

        user = self.require_user(userid)
        args['userid'] = userid         # args is a full user object; make sure it has userid
        user.update(args)
        return "{0} updated".format(user.userid)

    def delete(self, userid):
        user = self.require_user(userid)
        result = user.delete()
        if not result:
            abort(400)
        return "{0} deleted".format(user.userid)

    def parse_args(self, require_schema=True):
        # TODO: create generic configurable parser util
        parser = reqparse.RequestParser()
        parser.add_argument('userid', type=str, required=require_schema, help='Unique user ID')
        parser.add_argument('first_name', type=str, required=require_schema, help='User\'s first name')
        parser.add_argument('last_name', type=str, help='User\'s last name')
        parser.add_argument('groups', type=list, location='json', help='List of groups')

        args = parser.parse_args()
        arg_dict = {k : v for k,v in args.iteritems()}

        return arg_dict

    '''Helper functions'''
    def require_user(self, userid):
        # Initialize user, return 404 if it doesn't exist in db
        unescaped_userid = urllib.unquote_plus(userid)
        user = User(unescaped_userid)
        if not user.exists_in_db():
            abort(404)
        return user