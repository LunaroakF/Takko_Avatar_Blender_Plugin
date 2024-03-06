import bpy

#获取激活的物体
def Acive_Get():
    return bpy.context.active_object

def Acive_Set(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

#获取全部选中的物体
def Selection_All_Get():
    return bpy.context.selected_objects.copy()

def Name_Get(obj):
    return obj.name
#设置物体的选中状态

def Select_Set(obj,select):
    obj.select_set(select)

#取消选中任何物体
def Selection_Clear():
    bpy.ops.object.select_all(action='DESELECT')

# 获取 Scene中的全部物体
def Scene_All_Get():
    return set(bpy.context.scene.objects)

#物体类型
def Type_Get(obj):
    return obj.type
    #enum in ["MESH", "CURVE", "SURFACE", "META", "FONT", 
    # "CURVES", "POINTCLOUD", "VOLUME", "GPENCIL", "ARMATURE", 
    # "LATTICE", "EMPTY", "LIGHT", "LIGHT_PROBE", "CAMERA", "SPEAKER"]
    # default "EMPTY",

#克隆物体（是否Link）
def Clone(obj,blLink):
    data = None
    if (blLink): data = obj.data
    else: data = obj.data.copy()

    newObj = bpy.data.objects.new(obj.name,data)
    newObj.parent = obj.parent

    collections = obj.users_collection
    for collection in collections:
        collection.objects.link(newObj)
    return newObj

#获取物体所在的全部合集
def Collections_All_Get(obj):
    collections = obj.users_collection
    result = []
    for co in collections:
        result.append(co.name)
    return result 

#将物体移入合集
def Collections_Set(obj,collections):
    if collections is not list:
        collections = [collections]
    old_collections = obj.users_collection
    for co in old_collections:
        co.objects.unlink(obj)
    for co_name in collections:
        co = bpy.context.blend_data.collections[co_name]
        co.objects.link(obj)



#创建空物体
def Create_Empty():
    Empty_Obj = bpy.data.objects.new(name="Empty", object_data = None)
    bpy.context.view_layer.active_layer_collection.collection.objects.link(Empty_Obj)
    return Empty_Obj

#删除物体
def Delete(obj):
    bpy.data.objects.remove(obj)

#进行过更改的东西有些需要Update，比如约束值修改后，位置需要刷新再获取
def Update():
    # 更新数据
    bpy.context.view_layer.update()
    # 更新画面
    for area in bpy.context.screen.areas:
        area.tag_redraw()

#获取位置(包括约束)
def Position_World_Get(obj):
    postion = [0,0,0]
    matrix = obj.matrix_world
    postion[0] = matrix[0][3]
    postion[1] = matrix[1][3]
    postion[2] = matrix[2][3]
    return postion

def Convert_Selection_To_Mesh():
    bpy.ops.object.convert(target='MESH')

def Parent_Set(obj,parentObj):
    obj.parent = parentObj

#清空父级
def Parent_Clear_Keep_Transform():
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')

#物体合并
def Join():
    bpy.ops.object.join()


