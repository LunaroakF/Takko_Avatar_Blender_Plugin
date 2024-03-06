import bpy

class Texture_Paint_Tool_Ui(bpy.types.Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "纹理绘制"
    bl_idname = "VIEW_3D_PT_Texture_Paint_Tool_UI"
    bl_category = '獭可工具'   
    bl_options = {'DEFAULT_CLOSED'}
    import os
    bl_order = int(os.path.basename(__file__)[:2])
    bl_parent_id = "VIEW_3D_PT_Avatar_PANEL_UI"
      
    def draw(self, context):

        layout = self.layout
        #放两个Button, 控制材质球槽的增减
        #一个列表,里面包含材质球槽, 并且可选择

        layout.template_list("Texture_Paint_Material_Uilist", "", context.scene, "texture_paint_tool_material_slot_list", context.scene, "texture_paint_tool_material_slot_list_index")

        layout.operator("texture_paint_tool.operate_material_slot",text = "", icon = "ADD").operation = 0
        layout.operator("texture_paint_tool.operate_material_slot",text = "", icon = "REMOVE").operation = 1

class Texture_Paint_Material_Uilist(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        layout.label(text="", icon_value=icon)