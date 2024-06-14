bl_info = {
    "name": "Blank Addon Simple",
    "author": "sereda",
    "version": (0, 0, 1),
    "blender": (4, 1, 0),
    "location": "",
    "description": "",
    "warning": "Test",
    "doc_url": "",
    "category": "",
}

import bpy

class ADDONNAME_OT_MOD_my_operator(bpy.types.Operator):
    bl_idname = "addonname.my_operator"
    bl_label = "My Operator Name"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.active_object #and len(bpy.context.selected_objects)>1
        # return context.area.type == 'VIEW_3D' and context.active_object and len(bpy.context.selected_objects)>1
    
    def execute(self, context):
    
        def myfunction_example():
            return bpy.context.active_object.name
            
        def main():
            print (myfunction_example())
            
        main()
        self.report({'INFO'}, "message")
        return {'FINISHED'}


class OBJECT_OT_my_operator(bpy.types.Operator):
    bl_idname = "object.my_operator"
    bl_label = "My Operator"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Access the addon preferences.
        prefs = context.preferences.addons[__package__].preferences
    
        # Retrieve the properties
        my_string = prefs.my_string
        my_int = prefs.my_int
        my_float = prefs.my_float
        my_bool = prefs.my_bool
        my_enum = prefs.my_enum
        my_path = prefs.my_path
        my_dir = prefs.my_dir
        my_file = prefs.my_file

        # Use the properties (for demonstration, we'll just print them)
        self.report({'INFO'}, f"String: {my_string}")
        self.report({'INFO'}, f"Integer: {my_int}")
        self.report({'INFO'}, f"Float: {my_float}")
        self.report({'INFO'}, f"Boolean: {my_bool}")
        self.report({'INFO'}, f"Enum: {my_enum}")
        self.report({'INFO'}, f"Path: {my_path}")
        self.report({'INFO'}, f"Directory: {my_dir}")
        self.report({'INFO'}, f"File: {my_file}")
    
        return {'FINISHED'}


####################------ UI -----#####################
class ADDONNAME_PT_panel(bpy.types.Panel):
#It's just another regular panel.
#Do not use it if not necessary (too much of the panels).
    bl_label = "Template Addon Panel"
    bl_idname = "ADDONNAME_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Template Addon"
    
    def draw(self, context):
        layout = self.layout
        layout.operator(ADDONNAME_OT_MOD_my_operator.bl_idname, text="Run My Operator")
        layout.operator(OBJECT_OT_my_operator.bl_idname, text="Run My Other Operator")

# def menu(self, context): # A simple button without submenu. Use this if the addon has one button.
    # layout = self.layout
    # layout.separator()
    # layout.operator(module.ADDONNAME_OT_MOD_my_operator.bl_idname, )
    
def menu(self, context): #This is more advanced setup - it's a main menu which is attached to Blender's menus.
    layout = self.layout
    layout.menu("VIEW3D_MT_object_my_addon_menu", text='Custom', icon_value=31)

class MyAddonSubMenu(bpy.types.Menu): #This is a submenu which is attached to menu. Must be registered though.
    bl_idname = "VIEW3D_MT_object_my_addon_menu"
    bl_label = "My Addon"
    
    def draw(self, context):
        layout = self.layout
        layout.operator(ADDONNAME_OT_MOD_my_operator.bl_idname, )
        layout.separator()# You could use separators
        layout.operator(OBJECT_OT_my_operator.bl_idname, )
        # You can add more items to the submenu if needed
####################------ UI -----#####################

################------ Preferences -----################
class MyAddonPreferences(bpy.types.AddonPreferences):
    # It should be the default way to declare(?) the addon preferences.
    bl_idname = __package__
    
    # Examples of properties types:
    # String Property
    my_string: bpy.props.StringProperty(
        name="String Value",
        description="A string property for the addon",
        default="Default Value"
    )

    # Integer Property
    my_int: bpy.props.IntProperty(
        name="Integer Value",
        description="An integer property for the addon",
        default=10,
        min=1,
        max=100
    )

    # Float Property
    my_float: bpy.props.FloatProperty(
        name="Float Value",
        description="A float property for the addon",
        default=1.0,
        min=0.0,
        max=10.0
    )

    # Boolean Property
    my_bool: bpy.props.BoolProperty(
        name="Boolean Value",
        description="A boolean property for the addon",
        default=False
    )

    # Enum Property
    my_enum: bpy.props.EnumProperty(
        name="Enum Value",
        description="An enum property for the addon",
        items=[
            ('OPT_A', "Option A", "Description of Option A"),
            ('OPT_B', "Option B", "Description of Option B"),
            ('OPT_C', "Option C", "Description of Option C")
        ],
        default='OPT_A'
    )

    # Path Property
    my_path: bpy.props.StringProperty(
        name="Path Value",
        description="A path property for the addon",
        subtype='FILE_PATH',
        default=""
    )

    # Directory Property
    my_dir: bpy.props.StringProperty(
        name="Directory Value",
        description="A directory property for the addon",
        subtype='DIR_PATH',
        default=""
    )

    # File Property
    my_file: bpy.props.StringProperty(
        name="File Value",
        description="A file property for the addon",
        subtype='FILE_NAME',
        default=""
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "my_string")
        layout.prop(self, "my_int")
        layout.prop(self, "my_float")
        layout.prop(self, "my_bool")
        layout.prop(self, "my_enum")
        layout.prop(self, "my_path")
        layout.prop(self, "my_dir")
        layout.prop(self, "my_file")
################------ Preferences -----################

###############------ Registration -----################
_classes = (
    ADDONNAME_OT_MOD_my_operator,
    OBJECT_OT_my_operator,
    ADDONNAME_PT_panel,
    MyAddonPreferences,
    MyAddonSubMenu,
)


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu)


def unregister():
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu)