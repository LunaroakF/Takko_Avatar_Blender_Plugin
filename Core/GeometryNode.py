import bpy
from . import Modifier

def Has_Property(obj, modifier_name, prop_name):
    mo = Modifier.Get_By_Name(obj, modifier_name)
    for k in mo.items():
        print(k)
    #return prop_name in mo.node_group.inputs.keys()

def Set_Property(obj, modifier_name, prop_name, value):
    mo = Modifier.Get_By_Name(obj, modifier_name)
    index = mo.node_group.inputs.find(prop_name)
    id = mo.node_group.inputs[index].identifier
    mo[id] = value
    
    # 务必要登记刷新一下
    obj.update_tag()

