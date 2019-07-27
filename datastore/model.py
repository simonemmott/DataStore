from json_model import JsonModel
import importlib


def import_class(name):
    mod_path = '.'.join(name.split('.')[:-1])
    cls_name = name.split('.')[-1]
    mod = importlib.import_module(mod_path)
    if hasattr(mod, cls_name):
        attr = getattr(mod, cls_name)
        if isinstance(attr, type):
            return attr
        raise ValueError('{name} is not a class'.format(name=name))
    raise ValueError('The module {mod} does not define {name}'.format(mod=mod_path, name=cls_name))


class MetaType(JsonModel):
    name = JsonModel.field(str)
    ref_type = JsonModel.field(str)
    
    class Meta():
        required_fields = ['name']
    
    def __init__(self, *args, **kw):
        super(MetaType, self).__init__(*args, **kw)
        if not self.ref_type:
            self.ref_type = self.name.split('.')[-1]
        self.type = import_class(self.name)
    
            
    @staticmethod
    def from_class(cls):
        return MetaType(name=cls.__name__)
    
        