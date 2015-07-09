class Db(object):
    db = None

    def __init__(self):
        super(Db, self).__init__()
        self.create_all()

    '''Initialization and teardown methods'''
    def create_all(self):
        self.db = {
            'group': [],
            'user': [],
            'user_in_group': []
        }

    def remove_all(self):
        self.db = None

    # Returns a cursor to iterate over results
    def find(self, table_name, query):
        target = self.db.get(table_name, None)
        if target is not None:
            for doc in target:
                doc_in_set = True
                if bool(query):
                    try:
                        for index, expected in query.iteritems():
                            if doc[index] != expected:
                                doc_in_set = False
                                break
                    except:
                        break
                if doc_in_set:
                    yield doc
        yield None

    # Inserts a document.
    # TODO: Implement primary keys and enforce uniqueness here
    def insert(self, table_name, doc):
        target = self.db.get(table_name, None)
        target.append(doc)
        return True

    def delete(self, table_name, doc):
        target = self.db.get(table_name, None)
        if doc in target:
            target.remove(doc)
            return True
        else:
            return False