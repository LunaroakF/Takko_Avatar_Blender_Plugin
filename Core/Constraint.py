import bpy
# "CAMERA_SOLVER", "FOLLOW_TRACK", "OBJECT_SOLVER", "COPY_LOCATION", "COPY_ROTATION", 
# "COPY_SCALE", "COPY_TRANSFORMS", "LIMIT_DISTANCE", "LIMIT_LOCATION", "LIMIT_ROTATION", 
# "LIMIT_SCALE", "MAINTAIN_VOLUME", "TRANSFORM", "TRANSFORM_CACHE", "CLAMP_TO", 
# "DAMPED_TRACK", "IK", "LOCKED_TRACK", "SPLINE_IK", "STRETCH_TO", "TRACK_TO", 
# "ACTION", "ARMATURE", "CHILD_OF", "FLOOR", "FOLLOW_PATH", "PIVOT", "SHRINKWRAP"

def Get_From_Obj(obj,conName):
    return obj.constraints[conName]
    
def Get_From_Pose(armObj,boneName,conName):
    return armObj.pose.bones[boneName].constraints[conName]

#因为要面对两种方案（骨骼和物体的约束），所以返回的是实例而非名称

#基类
class Constraint:
    @classmethod
    def Add_To_Obj(cls,obj):
        con = obj.constraints.new(cls.__name__)
        return con
    @classmethod
    def Add_To_Bone(cls,armObj,boneName):
        con = armObj.pose.bones[boneName].constraints.new(cls.__name__)
        return con
    

#跟随路径
class FOLLOW_PATH(Constraint):
    #偏移系数设置
    def Offset_Factor_Set(con,value):
        con.offset_factor = value

    #是否固定位置
    def Use_Fixed_Location_Set(con,value_bool):
        con.use_fixed_location = value_bool
    
    #目标设置
    def Target_Set(con,curveObj):
        con.target = curveObj


class CHILD_OF(Constraint):
    #目标设置
    def Target_Set(con,targetObj):
        con.target = targetObj

    #子目标（比如骨骼）
    def SubTarget_Set(con,subTargetName):
        con.subtarget = subTargetName