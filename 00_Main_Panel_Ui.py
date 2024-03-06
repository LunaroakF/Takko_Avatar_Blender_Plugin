import bpy

class Avatar_Panel_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Avatar工具"
    bl_idname = "VIEW_3D_PT_Avatar_PANEL_UI"    
    bl_category = '獭可工具'   
    bl_options = {'DEFAULT_CLOSED'}

    bl_order = -1
        
    def draw(self, context):        
        layout = self.layout

    def draw_header_preset(self, context):   
        self.layout.operator("web_tool.open",icon = "QUESTION").url = "www.baidu.com"


class Other_Panel_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "其他工具"
    bl_idname = "VIEW_3D_PT_Other_PANEL_UI"    
    bl_category = '獭可工具'   
    bl_options = {'DEFAULT_CLOSED'}

    bl_order = -2
        
    def draw(self, context):        
        layout = self.layout
        
