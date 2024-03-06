from asyncio.windows_events import NULL
from unittest import result
import bpy
from enum import Enum

class Modes(Enum):
    OTHER = 0
    OBJECT = 1
    EDIT = 2
    POSE = 3

class ObjType(Enum):
    OTHER = 0
    MESH = 1
    ARMATURE = 2
    CURVE = 3 

class ConsType(Enum):
    OTHER = 0
    COPY_TRANSFORMS = 1
    COPY_ROTATION = 2

class ModType(Enum):
    OTHER = 0
    ARMATURE = 1

class ChannelType(Enum):
    location = 0
    rotation_euler = 1
    rotation_quaternion = 2
    scale = 3

class RotationMode(Enum):
    OTHER = 0 
    QUATERNION = 1
    XYZ = 2




    

class Mode:
    def Get():
        mode = bpy.context.mode
        result = Modes.OTHER
        if mode in ['EDIT_MESH','EDIT_CURVE','EDIT_ARMATURE']:
            result = Modes.EDIT
        elif mode == 'POSE':
            result = Modes.POSE
        elif mode == 'OBJECT':
            result = Modes.OBJECT

        return result

    def Set(modeEnum):
        if Mode.Get() != modeEnum:
            bpy.ops.object.mode_set(mode = modeEnum.name)
    
    def EditObject(obj):
        if (Mode.Get() == Modes.EDIT):
            if Obj.EditObject == obj:
                return
            else : Mode.Set(Modes.OBJECT)
        Obj.Active.Set(obj)
        Mode.Set(Modes.EDIT)
    
    
class Obj:
    
    def All(): #获取所有物体
        return bpy.context.scene.objects

    def EditObject():
        return bpy.context.edit_object
    
    def Clone(obj): #克隆物体，返回克隆体
        newObj = bpy.data.objects.new(obj.name,obj.data)
        newObj.parent = obj.parent

        collections = obj.users_collection
        for collection in collections:
            collection.objects.link(newObj)
                
        return newObj

    
    class Active:
        
        def Get(): #获取Active的物体
            return bpy.context.active_object
            
        def Set(obj): #设置一个新物体为Active
            bpy.context.view_layer.objects.active = obj
            return

        def IsActive(obj): #判断一个物体是不是Active

            return bpy.context.active_object == obj

    class Select:

        def GetAll(): #获取全部选中物体
            return bpy.context.selected_objects

        def SetAll(isSelect): #选中/取消选中全部物体
            return

        def Set(obj): #设置物体的选中状态
            return
    
    def GetType(obj): #获取物体的类型
        t = obj.type
        result = ObjType.OTHER
        if t == "MESH": result = ObjType.MESH
        elif t == "ARMATURE": result = ObjType.ARMATURE
        elif t == "CURVE": result = ObjType.CURVE
        return result    
    
    class Transform:
        def SetRotationMode(obj,rotationMode):
            obj.rotation_mode = rotationMode.name
        def GetRotationMode(obj,rotationMode):
            r = RotationMode.OTHER
            if obj.rotation_mode in RotationMode.__members__:
                r = RotationMode._member_map_[obj.rotation_mode]
            return r

    




class Mesh:
    class Vertice:
        
        def Count(obj): #获得顶点数量
            return len(obj.data.vertices)
        
        def Selected(obj): #获得选中的点（index列表）
            result = []
            for ver in obj.data.vertices:
                if ver.select:
                    result.append(ver.index)
            return result
    
    class VertexGroup:

        def GetAllVtgNames(obj): #获取全部顶点组名称
            r = []
            for vtg in obj.vertex_groups:
                r.append(vtg.name)
            return r
        
        def RenameVtg(obj,oldName,newName): #重命名顶点组
            obj.vertex_groups[oldName].name = newName

        def Count(obj): #获取顶点组数量
            return len(obj.vertex_groups)

        def ActiveIndex(obj): #获取活动的顶点组的index
            return obj.vertex_groups.active_index

        def GetWeight(obj,vtgIndex,vIndex): #获取特定点的顶点组权重,
            return obj.vertex_groups[vtgIndex].weight(vIndex)

        def SetWeight(obj,vtgIndex,vIndexs,weight): #设置顶点组权重
            obj.vertex_groups[vtgIndex].add(vIndexs,weight,"REPLACE")
            return
        
        def RemoveVertice(obj,vtgIndex,vIndexs): #从顶点组中删除顶点
            obj.vertex_groups[vtgIndex].remove(vIndexs)
            return

class Constraint:
    
    class Bone:

        def Add(armObj,boneName,type): #新建约束,返回名称
            poseBone = armObj.pose.bones[boneName]
            con = poseBone.constraints.new(type.name)
            return con.name
        
        def SetValue(armObj,boneName,conName,conInfo): #设置数值
            poseBone = armObj.pose.bones[boneName]
            con = poseBone.constraints[conName]
            Constraint._valueWrite(con,conInfo)

        def Clear(armObj,boneName): #清除约束
            poseBone = armObj.pose.bones[boneName]
            cons = poseBone.constraints
            for con in cons:
                poseBone.constraints.remove(con)

    def _valueWrite(constraint,conInfo): #把conInfo写入constraint
        constraint.target = Obj.All()[conInfo.target]
        constraint.subtarget = conInfo.subTarget

    class ConInfoStruct: #结构体，约束信息
        def __init__(self):
            self.target = ""
            self.subTarget = ""
    
#驱动器
class Driver:
    def NewDriver(obj,channel,channelIndex): #在物体的某一个通道上新建驱动器（默认是脚本表达式）
        animData = obj.animation_data
        if animData is None: animData = obj.animation_data_create()
        FCurves = animData.drivers
        path = channel.name
        newFCurve = FCurves.find(path,index = channelIndex)
        if newFCurve is None:
            newFCurve = FCurves.new(path,index = channelIndex)
        driver = newFCurve.driver
        vars = driver.variables
        for var in vars: vars.remove(var)
        driver.type = "SCRIPTED"
    
    def SetScript(obj,channel,channelIndex,script): #给驱动器设置表达式
        driver = obj.animation_data.drivers.find(channel.name,index =channelIndex).driver
        driver.expression = script
        return

    def AddVar(obj,channel,channelIndex,varStruct): #给某一个驱动器输入变量
        driver = obj.animation_data.drivers.find(channel.name,index = channelIndex).driver
        vars = driver.variables
        var = vars.new()

        var.name = varStruct.name
        var.type = varStruct.type
        
        tar = var.targets[0]
        tar.id = varStruct.obj.id_data
        tar.bone_target = varStruct.bone_target
        tar.rotation_mode = varStruct.rotation_mode
        tar.transform_space = varStruct.transform_space
        tar.transform_type = varStruct.transform_type

        return
    
    class VarStruct:
        def __init__(self):
            self.name = "untitled"
            self.type = 'TRANSFORMS'

            self.obj = None
            self.bone_target = ""
            self.rotation_mode = "AUTO"
            self.transform_space = "LOCAL_SPACE" #[WORLD_SPACE,LOCAL_SPACE,TRANSFORM_SPACE]
            self.transform_type = "LOC_X" #[LOC_X, LOC_Y, LOC_Z, ROT_X, ROT_Y, ROT_Z, ROT_W, SCALE_X, SCALE_Y, SCALE_Z, SCALE_AVG]
            

            
            


#修改器
class Modifier:
    def GetByType(obj,modType): #根据类型获取修改器
        r = ""
        for mod in obj.modifiers:
            if mod.type == modType.name:
                r = mod.name
                break
        return r

    def GetAllByType(obj,modType): #根据类型获取全部修改器
        r = []
        for mod in obj.modifiers:
            if mod.type == modType.name:
                r.append(mod.name)
        return r

    def Clear(obj):
        obj.modifiers.clear()
    
    class Armature: #骨架修改器
        
        def GetArmObj(obj,modName): #获取骨架修改器的骨架物体
            return obj.modifiers[modName].object

class Armature:

    def GetBindingMeshObjs(armObj): #获取全部与其绑定的网格物体
        r = []
        objs = Obj.All()
        for obj in objs:
            if Obj.GetType(obj) == ObjType.MESH:
                modName = Modifier.GetByType(obj,ModType.ARMATURE)
                if modName != "":
                    if Modifier.Armature.GetArmObj(obj,modName) == armObj:
                        r.append(obj)
        return r

    def SetPosePosition(armObj,boolValue): #设置姿态位置（true）或静置位置（false）
            if boolValue == True:
                armObj.data.pose_position = 'POSE'
            else: armObj.data.pose_position = 'REST'

    class Bone:

        def SetName(armObj,oldName,newName): #设置骨骼名称
            armObj.data.bones[oldName].name = newName

        def GetAllNames(armObj): #获取全部骨骼的名称
            r = []
            for bone in armObj.data.bones:
                r.append(bone.name)
            return r

        def GetLayers(armObj,BoneName): #获取某个骨骼的全部层
            r = []
            layers = armObj.data.bones[BoneName].layers
            for i in range(len(layers)):
                if layers[i] == True:
                    r.append(i+1)
            return r 
        
        def GetBoneNamesInLayer(armObj,layer): #获取某个层中的全部骨骼名称
            r = []
            allBones = Armature.Bone.GetAllNames(armObj)
            for bone in allBones:
                if layer in Armature.Bone.GetLayers(armObj,bone):
                    r.append(bone)
            return r

        def GetUseConnect(armObj,boneName): #获取骨骼是否是相连项
            return armObj.data.bones[boneName].use_connect

        def Edit_SetLayers(armObj,BoneName,layerArray): #给某个骨骼设置骨骼层(需要Edit)      
            layers = [False] * 32          
            if isinstance(layerArray,int): layerArray = [layerArray]
            for i in layerArray:
                layers[i - 1] = True
            armObj.data.edit_bones[BoneName].layers = layers
      
        def Edit_SetUseDeform(armObj,boneName,boolValue): #设置骨骼是否UseDefrom
            editBone = armObj.data.edit_bones[boneName]
            editBone.use_deform = boolValue

        def Edit_GetBoneTransform(armObj,boneName): #根据名称获取骨骼的位置信息(需要处于Edit模式，)            
            r = Armature.BoneTransformStruct()

            editBone = armObj.data.edit_bones[boneName]

            r.headLocal = editBone.head
            r.tailLocal = editBone.tail
            r.roll = editBone.roll

            return(r)

        def Edit_SetBoneTransform(armObj,boneName,boneInfo): #设置骨骼的位置信息     

            editBone = armObj.data.edit_bones[boneName]

            editBone.head = boneInfo.headLocal
            editBone.tail = boneInfo.tailLocal
            editBone.roll = boneInfo.roll
        
        def Edit_New(armObj,name): #创建新的骨骼
            editBones = armObj.data.edit_bones
            editBones.new(name)
        
        def GetParent(armObj,boneName): #获取骨骼的父级名称
            parent = armObj.data.bones[boneName].parent
            if parent is None: return ""
            else: return parent.name

        def Edit_SetParent(armObj,boneName,parentName): #设置父级
            editBones = armObj.data.edit_bones
            editBones[boneName].parent =  editBones[parentName]

    class BoneTransformStruct: #结构体，骨骼的位置信息
        def __init__(self):
            self.headLocal = []
            self.tailLocal = []
            self.roll = 0



class Poll:
    def ArmatureObj(self,object):
        return object.type == 'ARMATURE'


class Report:
    def Info(operator,info):
        operator.report({"INFO"},info)

    def Error(operator,info):
        operator.report({"ERROR"},info)
    
    def Warning(operator,info):
        operator.report({"WARNING"},info)

class Editor:
    def ShowWeight(boolValue):
        bpy.context.space_data.overlay.show_weight = boolValue