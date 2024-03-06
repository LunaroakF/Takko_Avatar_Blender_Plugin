from typing import List
import bpy
#创建骨架
def Create_Empty_Armature(arm_name = "Armature"):
    arm_data = bpy.data.armatures.new(name= arm_name)
    arm_obj = bpy.data.objects.new(name= arm_name, object_data = arm_data)
    bpy.context.view_layer.active_layer_collection.collection.objects.link(arm_obj)
    return arm_obj

def Binding_Default():
    bpy.ops.object.parent_set(type='ARMATURE')
    
#绑定(自动权重)
def Binding_With_Auto_Weight():
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')

#合并
def Join():
    bpy.ops.object.join()

#创建Edit骨骼(Edit模式)
def Create_Edit_Bone(armObj,bone_name = "newBone"):
    bone = armObj.data.edit_bones.new(bone_name)
    return bone.name

#删除骨骼(Edit)
def Edit_Bone_Remove(armObj,boneName):
    armObj.data.edit_bones.remove(armObj.data.edit_bones[boneName])

#Edit骨骼位置设置(Edit模式),注意，遍历设置的时候，这个会受到镜像的叠加
def Edit_Bone_Transform_Set(armObj,boneName,head = None,tail = None ,roll = None):
    bone = armObj.data.edit_bones[boneName]
    if head is not None: bone.head = head
    if tail is not None: bone.tail = tail
    if roll is not None: bone.roll = roll

def Edit_Bone_Transform_Get(armObj,boneName):
    bone = armObj.data.edit_bones[boneName]
    return (tuple(bone.head),tuple(bone.tail),bone.roll)

#设置父级(Edit模式)
def Edit_Bone_Parent_Set(armObj,childName,parentName,connect = False):
    if parentName is None:
        armObj.data.edit_bones[childName].parent = None
    else:
        armObj.data.edit_bones[childName].parent = armObj.data.edit_bones[parentName]
        armObj.data.edit_bones[childName].use_connect = connect

def Use_Mirror_Set(blMirror):
    bpy.context.object.data.use_mirror_x = blMirror

def Use_Mirror_Get():
    return bpy.context.object.data.use_mirror_x

#获取父级
def Bone_Parent_Get(armObj,boneName):
    parent = armObj.data.bones[boneName].parent
    if parent is None: return None
    return parent.name

#获取子级
def Bone_Children_Get(armObj,boneName):
    children = armObj.data.bones[boneName].children
    if len(children) == 0: return None
    children_names = []
    for child in children:
        children_names.append(child.name)
    return children_names

#设置骨骼层级，输入的是层级或列表 （5或[3,5,11]）
def Edit_Bone_Layers_Set(armObj,boneName,layers):
    lsLayer = [False] * 32
    if type(layers) is int:
        lsLayer[layers] = True
    elif type(layers) is list:
        for i in layers:
            lsLayer[i] = True
    armObj.data.edit_bones[boneName].layers = lsLayer

#获取全部骨骼名称
def Bone_Names_All_Get(armObj):
    names = []
    for bone in armObj.data.bones:
        names.append(bone.name)
    return names

#修改骨骼名称
def Bone_Name_Change(armObj,originName,newName):
    armObj.data.bones[originName].name = newName

#确定骨骼组是否存在(过时)
def Bone_Group_Exist(armObj,groupName):
    if armObj.pose.bone_groups.find(groupName) == -1: return False
    return True

#获取全部骨骼的骨骼组(过时)
def Bone_Group_All_Get(armObj):
    bone_grps_names = []
    for grp in armObj.pose.bone_groups:
        bone_grps_names.append(grp.name)
    return bone_grps_names

#通过骨骼组获取骨骼(过时)
def Bones_From_Group(armObj,groupName):
    bones = []
    for bone in armObj.pose.bones:
        if bone.bone_group is not None and bone.bone_group.name == groupName:
            bones.append(bone.name)
    return bones

#确定骨骼集合是否存在
def Bone_Collection_Exist(armObj,collectionName):
    if armObj.data.collections.find(collectionName) == -1: return False
    return True

#根据骨架物体获得全部骨骼集合
def Bone_Collection_All_Get(armObj):
    bone_collection_names = []
    for collection in armObj.data.collections:
        bone_collection_names.append(collection.name)
    return bone_collection_names

#获取骨骼集合中的全部骨骼
def Get_Bones_From_Collection(armObj,collectionName):
    bones = []
    for bone in armObj.data.bones:
        if bone.collections is not None:
            for collection in bone.collections:
                if collection.name ==  collectionName:
                    bones.append(bone.name)
                    break
    return bones



#约束



#制作骨骼树收效甚微，因为Blender不像Unity能有个根节点来按层获取