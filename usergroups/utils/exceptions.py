class PrimaryKeyException(Exception):
    def __init__(self, value):
        self.value = value
        self.msg = "Primary Key Collision: %s".format(value)
    def __str__(self):
        return self.msg

class PrimaryKeyNotFoundException(Exception):
    def __init__(self, value):
        self.value = value
        self.msg = "Primary Key Expected but not found: %s".format(value)
    def __str__(self):
        return self.msg