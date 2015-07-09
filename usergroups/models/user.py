from usergroups.models.base import BaseModel
from usergroups.models.user_in_group import UserInGroup
from usergroups.models.group import Group

class User(BaseModel):
    userid = None
    first_name = None
    last_name = None
    groups = None

    _index = ['userid']
    _table = 'user'
    _pickle_schema = [
        'first_name',
        'last_name',
        'userid',
        'groups'
    ]
    _exclude_fields = ['groups']

    def __init__(self, data):
        super(User, self).__init__(data)
        if self.groups is None:
            self.groups = UserInGroup.list_groups({'userid': self.userid})

    def insert(self):
        # Overriding insert can ensure concurrency of user_in_group data on updates too
        # This is because insert is currently invoked by update
        if super(User, self).insert():
            # Create user-group mappings on successful insert
            uigs = []
            cached_group_lookups = {}
            if getattr(self, 'groups', None) is not None:
                for group_name in self.groups:
                    if group_name not in cached_group_lookups:
                        group = Group(group_name)
                        if not group.exists_in_db():
                            cached_group_lookups[group_name] = group.insert()
                    uig = {'userid': self.userid, 'group_name': group_name}
                    uigs.append(uig)
                UserInGroup.insert_many(uigs)
            return True
        return False

    def delete(self):
        userid_to_delete = self.userid
        if super(User, self).delete():
            # Remove all user-group mappings on successful delete
            UserInGroup.delete_many({'userid': userid_to_delete})
            return True
        return False


