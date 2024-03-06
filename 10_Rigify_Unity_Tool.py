import bpy
from .Core import Takko as T

bpy.types.Scene.rigify_meta_rig = bpy.props.PointerProperty(
    type=bpy.types.Object,
    poll=T.Poll.ArmatureObj)

#Rigify的MetaRig
bpy.types.Scene.rigify_rig = bpy.props.PointerProperty(
    type=bpy.types.Object,
    poll=T.Poll.ArmatureObj)

class Rigify_Unity_OT_Create_Export_Bones(bpy.types.Operator):
    bl_idname = "rigify_unity.create_export_bones"
    bl_label = "创建导出用的骨骼"

    def execute(self,context): 
        
        rig =  context.scene.rigify_rig
        if rig == None: 
            T.Report.Error(self,"没有选择Rig骨骼")
            return {"CANCELLED"} 

        #确定28层没有骨骼，否则不执行
        if len(T.Armature.Bone.GetBoneNamesInLayer(rig,28)) != 0:
            T.Report.Error(self,"Rig骨架的28层已经有骨骼")
            return {"CANCELLED"} 
        
        
        #获取30层的骨骼信息,并加入到字典
        DEFBoneNames = T.Armature.Bone.GetBoneNamesInLayer(rig,30)
        
        defBoneNames = [] #创建一个小写名称的列表
        for i in range(len(DEFBoneNames)):
            defBoneNames.append(DEFBoneNames[i].replace("DEF","def"))


        modeChache = T.Mode.Get()
        T.Mode.EditObject(rig) #切换到编辑模式进行操作

        nameToTransform = {} #创建字典，并录入信息
        for boneName in DEFBoneNames:
            boneInfo = T.Armature.Bone.Edit_GetBoneTransform(rig,boneName)
            nameToTransform[boneName] = boneInfo

        
        #改名，移动骨骼层，取消形变
        for i in range(len(DEFBoneNames)): #改名
            T.Armature.Bone.SetName(rig,DEFBoneNames[i],defBoneNames[i]) 
        
        for boneName in defBoneNames: #从30层复制到28层，取消形变
            T.Armature.Bone.Edit_SetLayers(rig,boneName,[28])
            T.Armature.Bone.Edit_SetUseDeform(rig,boneName,False)

        #按照记录的位置生成新的骨骼，放置在30层
        for boneName in DEFBoneNames:
            T.Armature.Bone.Edit_New(rig,boneName)
            T.Armature.Bone.Edit_SetLayers(rig,boneName,30)
            T.Armature.Bone.Edit_SetBoneTransform(rig,boneName,nameToTransform[boneName])

        #进入Pose模式,静置位置，设置约束
        T.Mode.Set(T.Modes.POSE)
        T.Armature.SetPosePosition(rig,False)

        for i in range(len(DEFBoneNames)):    

            conName = T.Constraint.Bone.Add(rig,DEFBoneNames[i],T.ConsType.COPY_TRANSFORMS)     

            conInfo = T.Constraint.ConInfoStruct()
            conInfo.target = rig.name
            conInfo.subTarget = defBoneNames[i]

            T.Constraint.Bone.SetValue(rig,DEFBoneNames[i],conName,conInfo)

        T.Armature.SetPosePosition(rig,True)
        T.Mode.Set(modeChache)

        #获取全部与rig绑定的网格体,重命名其顶点组
        bindingMeshs = T.Armature.GetBindingMeshObjs(rig)
        
        for obj in bindingMeshs:
            for vtgName in T.Mesh.VertexGroup.GetAllVtgNames(obj):
                oldName = vtgName
                newName = vtgName.replace("def","DEF")
                T.Mesh.VertexGroup.RenameVtg(obj,oldName,newName)

        return {"FINISHED"}  
    
class Rigify_Unity_OT_Relink_Export_Bones(bpy.types.Operator):
    bl_idname = "rigify_unity.relink_export_bones"
    bl_label = "重新连接导出用的骨骼"

    def execute(self,context): 
        
        metaRig = context.scene.rigify_meta_rig
        if metaRig == None: 
            T.Report.Error(self,"需要选择MetaRig骨架")
            return {"CANCELLED"} 
        
        rig = context.scene.rigify_rig
        if rig == None: 
            T.Report.Error(self,"需要选择Rig骨架")
            return {"CANCELLED"} 

        #从MetaRig中获取骨骼父子级关系，创建字典
        modeChace = T.Mode.Get() 
        T.Mode.EditObject(metaRig) 

        metaBones = T.Armature.Bone.GetAllNames(metaRig)
        
        boneNameToParent = {} #骨骼的父级

        for bone in metaBones :
            boneName = bone
            parentName = T.Armature.Bone.GetParent(metaRig,bone)
            boneName = "DEF-" + boneName
            if parentName != "":     
                parentName = "DEF-" + parentName
            boneNameToParent[boneName] = parentName
   
        T.Mode.EditObject(rig) #编辑Rig
        
        defBones = T.Armature.Bone.GetBoneNamesInLayer(rig,30) 

    
        for boneName in defBones: #根据字典设置rig里的DEF骨的父级
            parentName = boneNameToParent[boneName]
            if parentName != "":
                T.Armature.Bone.Edit_SetParent(rig,boneName,parentName)
        
        #进入Pose模式，将有父级并且是相连项的骨骼的约束设置为复制旋转
        T.Mode.Set(T.Modes.POSE)
        T.Armature.SetPosePosition(rig,False)
        for boneName in defBones: 
            parentName = boneNameToParent[boneName]
            if parentName != "":
                T.Constraint.Bone.Clear(rig,boneName)
                conName = T.Constraint.Bone.Add(rig,boneName,T.ConsType.COPY_ROTATION)  
                info = T.Constraint.ConInfoStruct()
                info.type = T.ConsType.COPY_ROTATION
                info.target = rig.name
                info.subTarget = boneName.replace("DEF","def")
                T.Constraint.Bone.SetValue(rig,boneName,conName,info)      
        T.Armature.SetPosePosition(rig,True)

        T.Mode.Set(modeChace)

        return {"FINISHED"} 

