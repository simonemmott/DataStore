import os.path
import os
from datastore.model import MetaType
from datastore.exception import NotAManagedType, InvalidDataStoreFormat
from json_model import get_ref, DuplicateReference, matches
import json

class References(object):
    def __init__(self, datastore, ref_type):
        self.datastore = datastore
        self.ref_type = ref_type
        self._ref_data = {}
        if not os.path.exists(os.path.join(self.datastore.path, self.ref_type, '__meta__.json')):
            raise InvalidDataStoreFormat('The reference type {type} does not define its meta data')
        self.meta = MetaType(file=os.path.join(self.datastore.path, self.ref_type, '__meta__.json'))
        self._scan()
        
    def _scan(self):
        for name in os.listdir(os.path.join(self.datastore.path, self.ref_type)):
            if name[0] != '_' and name[-5:] == '.json':
                ref = name[:-5]
                data = self.meta.type(file=os.path.join(self.datastore.path, self.ref_type, name))
                self._ref_data[ref] = data
                
    def _filename(self, ref):
        return os.path.join(self.datastore.path, self.ref_type, str(ref)+'.json')
    
    def _write(self, ref, obj):
        if hasattr(obj, 'to_dict') and callable(obj.to_dict):
            data = obj.to_dict()
        elif isinstance(obj, dict):
            data = obj
        else:
            raise TypeError('Unable to extract dict data from object of type: {cls}'.format(cls=obj.__class__.__name__))
        with open(self._filename(ref), 'w') as fp:
            json.dump(data, fp)
            
        
    def get(self, ref=None, **kw):
        if ref:
            if ref not in self._ref_data:
                raise self.meta.type.DoesNotExist(ref=ref)
            return self._ref_data[ref]
        else:
            for key, value in self._ref_data.items():
                if matches(value, **kw):
                    return value
            raise self.meta.type.DoesNotExist(criteria=kw)            
    
    def add(self, obj, **kw):
        ref = get_ref(obj, **kw)
        if ref in self._ref_data:
            raise self.meta.type.DuplicateReference(type=obj.__class__.__name__, ref=ref)
        self._write(ref, obj)
        self._ref_data[ref] = obj     
    
    def update(self, obj, **kw):
        ref = get_ref(obj, **kw)
        if ref not in self._ref_data:
            raise self.meta.type.DoesNotExist(ref=ref)
        self._write(ref, obj)
        self._ref_data[ref] = obj
    
    def delete(self, obj, **kw):
        ref = get_ref(obj, **kw)
        if ref not in self._ref_data:
            raise self.meta.type.DoesNotExist(ref=ref)
        os.remove(self._filename(ref))
        del self._ref_data[ref]
    
    def filter(self, **kw):
        result = []
        for key, value in self._ref_data.items():
            if matches(value, **kw):
                result.append(value)
        return result
    

class DataStore(object):
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            raise FileNotFoundError("The root of the data store: '{path}' does not exist".format(path=path))
        if not os.path.isdir(path):
            raise FileNotFoundError("The root of the data store: '{path}' is not a directory".format(path=path))
        self.meta_types = {}
        self.ref_data = {}
        self._scan()
    
    def _scan(self):
        for name in os.listdir(self.path):
            if name[0] != '_':
                if os.path.isdir(os.path.join(self.path, name)):
                    if os.path.exists(os.path.join(self.path, name, '__meta__.json')):
                        mt = MetaType(file=os.path.join(self.path, name, '__meta__.json'))
                        self.meta_types[mt.ref_type] = mt
                        self.ref_data[mt.ref_type] = References(self, mt.ref_type)
    
    def types(self):
        return self.meta_types.keys()
    
    def get_type(self, ref_type):
        if ref_type in self.meta_types:
            return self.meta_types[ref_type]
        raise NotAManagedType(ref_type=ref_type)
    
    def type(self, ref_type):
        if ref_type not in self.ref_data:
            raise NotAManagedType(ref_type=ref_type)
        return self.ref_data[ref_type]
        
    
    