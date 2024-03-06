import bpy

# 材质槽 Item
class Texture_Paint_Tool_Material_Slot_Item(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    color: bpy.props.FloatVectorProperty(size=3)

# 这个 Item看样子不会被自动注册, 还得手动
bpy.utils.register_class(Texture_Paint_Tool_Material_Slot_Item)

# 用 Item去创建质槽 List
bpy.types.Scene.texture_paint_tool_material_slot_list = bpy.props.CollectionProperty(type=Texture_Paint_Tool_Material_Slot_Item)

# 材质槽 List的 Index
bpy.types.Scene.texture_paint_tool_material_slot_list_index = bpy.props.IntProperty()


class Texture_Paint_Tool_OT_Operate_Material_Slot(bpy.types.Operator):
    bl_idname = "texture_paint_tool.operate_material_slot"
    bl_label = "操作材质球"

    # 0:+ 1:- 2:上 3:下
    operation : bpy.props.IntProperty(default=0)

    def execute(self, context):
        material_list = context.scene.texture_paint_tool_material_slot_list

        if(self.operation == 0):
            material_list.add()
        if(self.operation == 1):
            material_list.remove(0)
        print(material_list)
        return {"FINISHED"}     