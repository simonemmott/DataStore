from json_model import JsonModel, RefItem

class Type1(JsonModel, RefItem):
    ref = JsonModel.field(str)
    name = JsonModel.field(str)
    description = JsonModel.field(str)
    
    class Meta():
        required_fields = ['ref', 'name']
        reference_field = 'ref'
   
    
class Type2(JsonModel, RefItem):
    ref = JsonModel.field(str)
    name = JsonModel.field(str)
    description = JsonModel.field(str)
    
    class Meta():
        required_fields = ['ref', 'name']
        reference_field = 'ref'
    
    