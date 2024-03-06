import bpy
import webbrowser

class Web_Tool_OT_Open(bpy.types.Operator):
    bl_idname = "web_tool.open"
    bl_label = ""

    url : bpy.props.StringProperty(default="")

    def execute(self, context):
        webbrowser.open(self.url) 
        return {'FINISHED'}