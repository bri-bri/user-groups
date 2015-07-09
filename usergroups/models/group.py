from usergroups.models.base import BaseModel
from usergroups.models.user_in_group import UserInGroup

class Group(BaseModel):
    group_name = None

    _index = ['group_name']
    _mapping = {'name': 'group_name'}
    _table = 'group'
    _exclude_fields = ['users']

    def __init__(self, data):
        super(Group, self).__init__(data)
        self.users = UserInGroup.list_users({'group_name': self.group_name})

    def delete(self):
        group_name_to_delete = self.group_name
        if super(Group, self).delete():
            UserInGroup.delete_many({'group_name' : group_name_to_delete})
            return True
        return False

    def update(self, users):
        UserInGroup.delete_many({'group_name' : self.group_name})

        user_in_group_data = []
        unique_users = set(users)
        for userid in unique_users:

            doc = {
                'userid': userid,
                'group_name': self.group_name
            }
            user_in_group_data.append(doc)
        UserInGroup.insert_many(user_in_group_data)
        return True