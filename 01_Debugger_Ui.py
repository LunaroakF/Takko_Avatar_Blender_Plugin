import bpy

class Debbuger_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Debug"
    bl_idname = "VIEW_3D_PT_Debbuger_UI"    
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = '獭可工具'   
    import os
    bl_order = int(os.path.basename(__file__)[:2])
    bl_parent_id = "VIEW_3D_PT_Avatar_PANEL_UI"
    

    def draw(self, context):        
        layout = self.layout
        layout.operator("debugger.test", text = "测试")
        