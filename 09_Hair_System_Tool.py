import bpy
from .Core import Mode
from .Core import Log
from .Core import Obj
from .Core import GeometryNode
from .Core import Modifier


class Hair_System_Tool_OT_Toggle_Proxy(bpy.types.Operator):
    bl_idname = "hair_system_tool.toggle_proxy"
    bl_label = "切换毛发状态"
    value : bpy.props.BoolProperty()

    def execute(self,context): 
        _prop_name = "Socket_10"
        _nodeTree_name = "Fur"

        #if not Mode.Is_Object(): return Log.Error_Cancelled(self, "请在物体模式下操作")
        
        # 获取全部曲线物体
        objs = Obj.Scene_All_Get()
        hair_objs = set()

        for obj in objs:
            if Obj.Type_Get(obj) == "CURVES":
                hair_objs.add(obj)

        # 遍历曲线物体, 获得几何节点
        success_objs = set()
        for obj in hair_objs:
            node_modifiers = Modifier.Get_All_By_Type(obj,"NODES")
            for node_modifier in node_modifiers:
                # 确定 修改器里指定的树的名称是对应的
                mo = Modifier.Get_By_Name(obj,node_modifier)    
                if mo.node_group.name != _nodeTree_name: continue
                

                # 设定值
                mo[_prop_name] = self.value
                success_objs.add(obj)
        # 设置完值,刷新一下
        Obj.Update()

        # Report
        fail_objs = hair_objs - success_objs
        report = "成功设置了 {}个毛发".format(len(success_objs))
        if len(fail_objs) != 0:
            report += ", {}个毛发的几何节点没有 {}属性".format(len(fail_objs), _prop_name)
        Log.ReportInfo(self, report)

        return{"FINISHED"}
