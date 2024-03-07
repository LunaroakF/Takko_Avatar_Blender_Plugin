import bpy
from .Core import Poll
from .Core import Log
from .Core import Armature
from .Core import Obj
from .Core import VertexGroup
from .Core import Mode
from .Core import Constraint
from .Core import Modifier

# global的防止乱码 https://devtalk.blender.org/t/enumproperty-and-string-encoding/7835
# 获取骨骼集合名称组成一个列表
enum_list = []
def Get_Bone_Collection_Items(self, context):
    global enum_list
    arm = context.scene.decoration_constraint_tool_main_armature
    if arm is None:return []
    bone_grps = Armature.Collections_All_Get(arm)
    enum_list = []
    for grp in bone_grps:
        enum_list.append((grp,grp,""))
    return enum_list

# 骨架物体
bpy.types.Scene.decoration_constraint_tool_main_armature = bpy.props.PointerProperty(
        name ="主骨架",
        type= bpy.types.Object,
        poll= Poll.ArmatureObj )

# 骨骼集合名称
bpy.types.Scene.decoration_constraint_tool_bone_collection_name =  bpy.props.EnumProperty(
        name='身体骨骼集合',
        items=Get_Bone_Collection_Items,
    )



class Decoration_Constraint_Tool_OT_Seperate(bpy.types.Operator):
    bl_idname = "decoration_constraint_tool.seperate"
    bl_label = "从主骨架中分离"
    bl_description = "从主骨架中分离出一个服装的骨架，并设置约束"
        
    def execute(self,context): 
        if (not Mode.Is_Object): return Log.Error_Cancelled(self,"需在物体模式下操作")

        #获取选中的装饰物体
        decoration_objs = []     
        for obj in Obj.Selection_All_Get():
            if Obj.Type_Get(obj) == "MESH":
                decoration_objs.append(obj)
        if len(decoration_objs) == 0: return Log.Error_Cancelled(self,"未选中任何网格物体")

        #获取主骨架，以及全部的骨骼
        main_armObj = context.scene.decoration_constraint_tool_main_armature
        if main_armObj is None: return Log.Error_Cancelled(self,"未指定主骨架")
        all_bones = Armature.Bone_Names_All_Get(main_armObj)

        #通过骨骼组获取身体骨骼
        collection_name = context.scene.decoration_constraint_tool_bone_collection_name
        if collection_name == "": return Log.Error_Cancelled(self,"请指定身体骨骼所在骨骼集合")
        if not Armature.Is_Collection_Exist(main_armObj,collection_name): return Log.Error_Cancelled(self,"主骨架中并不包含 {} 这个骨骼集合".format(collection_name))
        body_bones = Armature.Get_Bones_From_Collection(main_armObj,collection_name)
        if(len(body_bones) == 0): return Log.Error_Cancelled(self,"骨骼集合没有指定骨骼")

        print(body_bones)

        #通过装饰网格体获取全部的非空顶点组
        decoration_vtgs = set()
        for obj in decoration_objs:
            nonEmpty_grps = VertexGroup.Non_Empty_Group_All_Get(obj)
            #取并集
            decoration_vtgs = decoration_vtgs | set(nonEmpty_grps)
        
        #服装权重骨(跟服装权重有关的骨骼) 服装顶点组 和 全部骨骼 取交集
        decoration_weight_bones = decoration_vtgs & set(all_bones)

        #仅属服装骨（服装权重骨中只属于服装的） 骨骼中不属于身体的 与 服装权重骨 取交集 
            #比如 sp_belt_01
        decoration_only_bones = (set(all_bones) - set(body_bones)) & decoration_weight_bones
        
        #额外服装骨（服装骨的子级和父级，不包括身体骨）
            #例如 root_belt sp_belt_end
        decoration_extra_bones = set()
        
        #身体服装骨（同时属于身体和服装的骨骼，包括有权重的，以及父级，简单来说就是身体骨骼中要被拷贝的）
            #例如 hips
                #先取身体骨骼和服装骨骼的交集，之后再遍历加入 子级是身体骨的
        decoration_body_bones = set(body_bones) & decoration_weight_bones

        def Run_All_Child(armatureObj,bone):
            #获取该骨骼的全部子骨骼
            children = Armature.Bone_Children_Get(armatureObj,bone)
            if children is not None:
                #遍历子骨骼
                for child_bone in children:
                    #如果子骨骼已经在 服装骨，就跳过
                    if(child_bone in decoration_only_bones): continue
                    #加入 额外服装骨，并继续遍历其子级
                    decoration_extra_bones.add(child_bone)
                    Run_All_Child(armatureObj,child_bone)
        
        def Run_All_Parent(armatureObj,bone):
            #获取骨骼的父级
            parent_bone = Armature.Bone_Parent_Get(armatureObj,bone)
            #如果父级不是空并且不在服装骨中
            if parent_bone is not None and parent_bone not in decoration_only_bones:
                #如果父级是身体骨
                if parent_bone in body_bones:
                    #加入 身体服装骨
                    decoration_body_bones.add(parent_bone)
                #父级不是身体骨，那么它就是其他骨
                else:
                    #加入额外服装骨，继续遍历其父级
                    decoration_extra_bones.add(parent_bone)
                    Run_All_Parent(armatureObj,parent_bone)

        #仅属服装骨 的子级中获得 额外服装骨
        for bone in decoration_only_bones:
            Run_All_Child(main_armObj,bone)
        #仅属服装骨 的父级中获得 额外服装骨 和 其他的 身体服装骨
        for bone in decoration_only_bones:
            Run_All_Parent(main_armObj,bone)
        
        #输出一下
        print("="*40)
        print("仅属服装骨 {0} 个: {1}".format(len(decoration_only_bones), " ".join(decoration_only_bones)))
        print("额外服装骨 {0} 个: {1}".format(len(decoration_extra_bones), " ".join(decoration_extra_bones)))
        print("身体服装骨 {0} 个: {1}".format(len(decoration_body_bones), " ".join(decoration_body_bones)))
        print("="*40)

        #拷贝一个新的骨架并赋值，作为服装骨架，注意是拷贝
        decoration_armObj = Obj.Clone(main_armObj,False)
        collections = Obj.Collections_All_Get(decoration_objs[0])
        Obj.Collections_Set(decoration_armObj,collections[0])

        #删除原骨架的服装骨
        Obj.Selection_Clear()
        Obj.Acive_Set(main_armObj)
        Mode.Switch_Edit()

        for bone in decoration_only_bones:
            Armature.Edit_Bone_Remove(main_armObj,bone)
        for bone in decoration_extra_bones:
            Armature.Edit_Bone_Remove(main_armObj,bone)
        
        Mode.Switch_Object()

        #遍历，断掉 身体服装骨 的父级，并删除掉不属于三个骨的骨骼

        Obj.Selection_Clear()
        Obj.Acive_Set(decoration_armObj)
        Mode.Switch_Edit()
        
        for bone in Armature.Bone_Names_All_Get(decoration_armObj):
            if bone in decoration_body_bones:
                Armature.Edit_Bone_Parent_Set(decoration_armObj,bone,None)
            elif bone not in decoration_only_bones and bone not in decoration_extra_bones:
                Armature.Edit_Bone_Remove(decoration_armObj,bone)
        
        #将 身体服装骨 缩小(操作的时候关闭镜像，不然会操作叠加)
        blMirror = Armature.Use_Mirror_Get()
        Armature.Use_Mirror_Set(False)

        for bone in Armature.Bone_Names_All_Get(decoration_armObj):
            if bone in decoration_body_bones:
                head,tail,roll = Armature.Edit_Bone_Transform_Get(decoration_armObj,bone)
                center = ((head[0]+tail[0])/2,(head[1]+tail[1])/2,(head[2]+tail[2])/2)  
                Armature.Edit_Bone_Transform_Set(
                    decoration_armObj,bone,
                    tail = center)
        
        Armature.Use_Mirror_Set(blMirror)
        
        #设置约束
        Mode.Swtich_Pose()
        for bone in decoration_body_bones:
            con = Constraint.CHILD_OF.Add_To_Bone(decoration_armObj,bone)
            Constraint.CHILD_OF.Target_Set(con,main_armObj)
            Constraint.CHILD_OF.SubTarget_Set(con,bone)
        
        Mode.Switch_Object()
        
        #将装饰绑定到服装骨骼
        for obj in decoration_objs: 
            mos = Modifier.Get_All_By_Type(obj,"ARMATURE")
            for mo in mos:
                Modifier.Remove(obj,mo)
            Obj.Selection_Clear()
            Obj.Select_Set(obj,True)
            Obj.Acive_Set(decoration_armObj)
            Armature.Binding_Default()

        return {"FINISHED"}
    
class Decoration_Constraint_Tool_OT_Combine(bpy.types.Operator):
    bl_idname = "decoration_constraint_tool.combine"
    bl_label = "合并回主骨架"
    bl_description = "将选中的装饰及其骨架合并回主骨架"
        
    def execute(self,context): 
        #获取主骨架，以及全部的骨骼
        main_armObj = context.scene.decoration_constraint_tool_main_armature
        if main_armObj is None: return Log.Error_Cancelled(self,"未指定主骨架")
        main_bones = Armature.Bone_Names_All_Get(main_armObj)

        #获取选中的全部装饰,和全部骨架
        decoration_objs = []
        deco_arm_objs = []
        for obj in Obj.Selection_All_Get():
            if Obj.Type_Get(obj) == "MESH":
                decoration_objs.append(obj)
            elif Obj.Type_Get(obj) == "ARMATURE" and obj != main_armObj:
                deco_arm_objs.append(obj)
        
        if len(deco_arm_objs) == 0: return Log.Error_Cancelled(self,"未选择服装骨架")
        if len(decoration_objs) == 0: Log.ReportWarning(self,"未选择任何服装网格，仅将骨骼合并")
        
        #对比骨架中的名称，通过名称相同部分，获取全部要移除的身体骨，和要合并的装饰骨
        #列表序号与 deco_arm_objs 的序号相同
        #字典是装饰骨架中的与身体骨直接连接的骨骼和它们的父级
        ls_bone_to_remove = []
        ls_bone_to_combine = []
        dic_parent = {}
        for i in range(len(deco_arm_objs)):
            #获取要移除的和要合并的骨骼
            arm_obj = deco_arm_objs[i]
            bone_names = Armature.Bone_Names_All_Get(arm_obj)
            bone_to_remove = set()
            bone_to_combine = set()
            for bone_name in bone_names:
                if bone_name in main_bones:bone_to_remove.add(bone_name)
                else : bone_to_combine.add(bone_name)

            ls_bone_to_remove.append(bone_to_remove)
            ls_bone_to_combine.append(bone_to_combine)

            print(bone_to_remove)
            print(bone_to_combine)
            #记录父级
            for deco_bone in bone_to_combine:
                parent = Armature.Bone_Parent_Get(arm_obj,deco_bone)
                print(parent)
                if parent in bone_to_remove:
                    dic_parent[deco_bone] = parent           

        #确保 ls_bone_to_combine 中没有相同的骨骼名称
        same_names = set()
        for i in range(len(ls_bone_to_combine) - 1):
            same_names = same_names | (ls_bone_to_combine[i] & ls_bone_to_combine[i+1])
        if (len(same_names)) > 0:
            error_info = "装饰骨架间存在同名骨骼："
            for name in same_names:
                error_info += name + " "
            return Log.Error_Cancelled(self,error_info)

        
        #删除掉服装骨架中的全部的身体骨
        Mode.Switch_Object()
        for i in range(len(deco_arm_objs)):
            arm_obj = deco_arm_objs[i]
            Obj.Selection_Clear()
            Obj.Acive_Set(arm_obj)
            Mode.Switch_Edit()
            for bone in ls_bone_to_remove[i]:
                Armature.Edit_Bone_Remove(arm_obj,bone)
            Mode.Switch_Object()
        
        #将服装骨架合并到主骨架
        Obj.Selection_Clear()
        for obj in deco_arm_objs:
            Obj.Select_Set(obj,True)
        Obj.Acive_Set(main_armObj)
        Obj.Join()

        print(dic_parent)
        #设置骨骼父级关系
        Mode.Switch_Edit()
        for bone in dic_parent.keys():
            Armature.Edit_Bone_Parent_Set(main_armObj,bone,dic_parent[bone],False)

        #将装饰绑定回主骨骼
        Mode.Switch_Object()
        for obj in decoration_objs: 
            mos = Modifier.Get_All_By_Type(obj,"ARMATURE")
            for mo in mos:
                Modifier.Remove(obj,mo)
            Obj.Selection_Clear()
            Obj.Select_Set(obj,True)
            Obj.Acive_Set(main_armObj)
            Armature.Binding_Default()


        return {"FINISHED"}
        
