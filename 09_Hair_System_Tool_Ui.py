import bpy
class Hair_System_Tool_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "毛发系统工具"
    bl_idname = "VIEW_3D_PT_HAIR_SYSTEM_TOOL_UI"    
    bl_category = '獭可工具'   
    bl_options = {'DEFAULT_CLOSED'}
    import os
    bl_order = int(os.path.basename(__file__)[:2])
    bl_parent_id = "VIEW_3D_PT_Other_PANEL_UI"
        
    def draw(self, context):        
        layout = self.layout
        row = layout.row()
        row.operator("hair_system_tool.toggle_proxy",text = "代理模式").value = True 
        row.operator("hair_system_tool.toggle_proxy",text = "毛发模式").value = False