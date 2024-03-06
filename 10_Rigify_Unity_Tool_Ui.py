import bpy

class Rigify_Unity_Tool_UI(bpy.types.Panel):

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Rigify到Unity"
    bl_idname = "VIEW_3D_PT_Rigify_Unity_Tool_UI"
    bl_category = '獭可工具'   
    bl_options = {'DEFAULT_CLOSED'}
    import os
    bl_order = int(os.path.basename(__file__)[:2])
    bl_parent_id = "VIEW_3D_PT_Other_PANEL_UI"
      
    def draw(self, context):

        layout = self.layout

        box = layout.box()
        box.prop_search(context.scene, "rigify_meta_rig", bpy.data, "objects", text='MetaRig',icon = 'OUTLINER_OB_ARMATURE')
        box.prop_search(context.scene, "rigify_rig", bpy.data, "objects", text='Rig',icon = 'OUTLINER_OB_ARMATURE')
        
        layout.operator("rigify_unity.create_export_bones",text = "创建散装DEF骨", icon ='BONE_DATA')
        layout.operator("rigify_unity.relink_export_bones",text = "重新连接DEF骨", icon ='BONE_DATA')