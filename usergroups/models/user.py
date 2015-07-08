from usergroups.db import Db

db = Db()
class User:
    first_name = None
    id = None
    def __init__(self, body):
        classname = self.__class__.__name__
        db.find(classname, body['userid'])
        first_name = body.get('first_name', None)

    def create(self, **kwargs):
        print "Creating"
        doc = {}
        for key,value in kwargs:
            doc[key] = value
        Db.insert('users', doc)
        return self.__init__({'userid':kwargs['userid']})

    def save(self):
        print "Saving"