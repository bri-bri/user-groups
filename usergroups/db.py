class Db:
    db = {'groups': [],
    'users': [],
    'users_in_groups': [],

    'groups_indexes': {'group_name': 0}, # primary key
    'users_indexes': {'userid': 0}, # primary key
    'users_in_groups_indexes': {'user_and_group': 0, 'group_name': 1, 'userid': 2 } # primary key and two foreign keys
    }
    def __init__(self):
        self.db

    # Find returns a cursor to iterate over results
    def find(self, table_name, query):
        target = self.db.get(table_name, None)
        indexes = self.db.get(table_name + "_indexes", None)
        if target is not None and indexes is not None:
            query_fields = {}
            for key,val in query:
                if indexes.get(key, None) is not None:
                    query_fields[indexes['key']] = val
            for doc in target:
                if bool(query_fields):
                    try:
                        for index,expected in query_fields:
                            if doc[index] != expected:
                                pass
                    except:
                        pass
                yield doc
        yield None

    def findOne(self, table_name, query):
        cursor = self.find(table_name, query)
        return next(cursor)

    def findAll(self, table_name, query):
        cursor = self.find(table_name, query)
        results = []
        for doc in cursor:
            results.append(doc)
        return results

    def insert(self, table_name, row):
        print "INSERTING", row
        target = self.db.get(table_name, None)
        indexes = self.db.get(table_name + "_indexes", None)
        if target is not None and indexes is not None:
            unique_query = {}
            for key in indexes:
                unique_query[key] = row.get(key, None)
            for doc in target:
                if self.match(doc, unique_query):
                    print "COLLISION"
                    return False
            target.append(row)
        print target

    def delete(self, table, **kwargs):
        return "HI"

    def match(self, doc, query):
        for key, value in query:
            if doc.get(key, None) != value:
                return False
        return True