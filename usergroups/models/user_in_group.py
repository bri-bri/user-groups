from usergroups.models.base import BaseModel

'''A graph edge-like data model defining the edge between users and groups

Intended to optimize for reads instead of writes'''


class UserInGroup(BaseModel):
    userid = None
    group_name = None

    _index = ['userid', 'group_name']
    _table = 'user_in_group'
    _groups_in_memory = {}

    @staticmethod
    def list_groups(query_params):
        uigs = UserInGroup().find_all(query_params)
        result = [UserInGroup(u).group_name for u in uigs if u is not None]
        return result

    @staticmethod
    def list_users(query_params):
        uigs = UserInGroup().find_all(query_params)
        result = [UserInGroup(u).userid for u in uigs if u is not None]
        return result

    @staticmethod
    def insert_many(docs):
        for doc in docs:
            uig = UserInGroup(doc)
            uig.insert()

    @staticmethod
    def delete_many(query_params):
        uigs = UserInGroup().find_all(query_params)
        for uig in uigs:
            if uig is not None:
                uig_object = UserInGroup(uig)
                uig_object.delete()