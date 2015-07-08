from usergroups.db import Db

db = Db()
class Group:
    group_name = None

    def __init__(self, group_name = None):
        self.group_name = group_name
        #classname = self.__class__.__name__
        db.findOne('groups', {'group_name':group_name})

    @staticmethod
    def create(group_name):
        db.insert('groups', {'group_name': group_name.get('name', None)})
        return Group(group_name)

    def find(self, **kwargs):
        results = []
        if 'userid' in kwargs:
            for group,user in self.groups:
                if user == kwargs['userid']:
                    results.append(group)
            return results
        elif 'group_name' in kwargs:
            return self.groups.get(kwargs['group_name'], [])

        return self.groups.keys()

    def save(self, group_name = None):
        return "blah"
        #db.insert('groups', (group_name))

    def update(self, group_name, users):
        return True

    def pickle(self):
        return self.group_name