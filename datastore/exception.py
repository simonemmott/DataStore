

class DataStoreException(Exception):
    pass

class InvalidDataStoreFormat(DataStoreException):
    pass

class NotAManagedType(DataStoreException):
    def __init__(self, **kw):
        if 'ref_type' in kw:
            super(NotAManagedType, self).__init__('{type} is not a managed type'.format(type=kw.get('ref_type')))
            return
        raise ValueError('Not enough values supplied to create exception')