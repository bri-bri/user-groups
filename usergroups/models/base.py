from usergroups import db
from usergroups.utils.exceptions import PrimaryKeyException, PrimaryKeyNotFoundException
from usergroups import logger

class BaseModel(dict):

    _mapping = {}
    _index = []
    _table = None
    _pickle_schema = []

    def __init__(self, data=None):
        data = self.sanitize(data)

        # Load from db if possible
        doc = self.find_one(data)
        data = doc if doc else data
        if data and type(data) is dict:
            for key, value in data.iteritems():
                # Map json keys to data model properties
                # Only set properties defined in data model
                if hasattr(self, key):
                    setattr(self, key, value)

    ''' CRUD methods'''
    def find_one(self, props):
        # Returns the first item in result iterator
        query = self.create_query(props)
        cursor = db.find(self._table, query)
        return next(cursor)

    def find_all(self, props):
        # Returns list of all items in result set
        query = self.create_query(props)
        cursor = db.find(self._table, query)
        results = []
        for item in cursor:
            results.append(item)
        return results

    def insert(self):
        # Ensure uniqueness by checking primary key
        if not self.exists_in_db():
            row = self.prepare_object()
            logger.logger.debug("INSERTING {0}".format(row))
            return db.insert(self._table, row)
        else:
            raise PrimaryKeyException(self.primary_key())

    def update(self, data):
        # Current update paradigm involves wholesale data model refresh; delete the whole thing and re-add it!
        if self.delete():
            self.__init__(data)
            return self.insert()
        else:
            query = self.primary_key_query()
            raise PrimaryKeyNotFoundException(query)

    def delete(self):
        query = self.prepare_object()
        logger.logger.debug("DELETING {0}".format(query))
        return db.delete(self._table, query)

    '''Query building methods'''
    def primary_key(self):
        # Get set of values composing unique primary key
        key_values = {key : getattr(self, key, None) for key in self._index if hasattr(self, key)}
        if None in key_values.values():
            return None
        return key_values

    def primary_key_query(self):
        # Create query on primary keys
        key_values = self.primary_key()
        query = self.create_query(key_values)
        return query

    def map_props(self, props):
        # Map property keys that might have different names in client request
        if type(props) is dict:
            props = {self._mapping.get(k, k) : v for k, v in props.iteritems()}
        return props

    def create_query(self, props):
        # Format query
        query_props = self.map_props(props)
        return query_props

    '''Helper methods'''
    def exists_in_db(self):
        # Checks for primary key in database
        query = self.primary_key_query()
        # If primary keys aren't properly set
        if not query:
            return None
        doc = self.find_one(query)
        return doc is not None

    def prepare_object(self):
        pickled = self.pickle()
        if hasattr(self, '_exclude_fields'):
            for key in self._exclude_fields:
                if key in pickled:
                    del pickled[key]
        return pickled

    def pickle(self):
        # Serialize the document
        result = {}
        pickle_fields = self._pickle_schema if bool(self._pickle_schema) else self._index
        for key in pickle_fields:
            result[key] = getattr(self, key, None)
        return result

    def sanitize(self, input):
        # Sanitize constructor params
        if (self._index and
            len(self._index) == 1 and
            type(input) is not dict):
                props = {self._index[0]: input.encode('utf-8')}
                return self.map_props(props)
        else:
            return self.map_props(input)




