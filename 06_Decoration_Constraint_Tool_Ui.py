import bpy
class Decoration_Constraint_Tool_Ui(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "装扮约束工具"
    bl_idname = "VIEW_3D_PT_Decortaion_Constraint_Tool_Ui"    
    bl_category = '獭可工具'    
    bl_options = {'DEFAULT_CLOSED'}
    import os
    bl_order = int(os.path.basename(__file__)[:2])
    bl_parent_id = "VIEW_3D_PT_Avatar_PANEL_UI"
        
    def draw(self, context):        
        layout = self.layout
        box = layout.box()
        box.prop(context.scene,'decoration_constraint_tool_main_armature')
        box.prop(context.scene,'decoration_constraint_tool_bone_collection_name')
        box.operator("decoration_constraint_tool.seperate")
        box.operator("decoration_constraint_tool.combine")