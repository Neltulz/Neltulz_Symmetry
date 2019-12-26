import bpy

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#    Reset all Settings
# -----------------------------------------------------------------------------    

class NTZSYM_OT_NtzResetAllSettings(Operator):
    """Tooltip"""
    bl_idname = "ntz_sym.resetallsettings"
    bl_label = "Neltulz - Symmetry - Reset all Settings"
    bl_description = 'Reset All Settings'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scn = context.scene
    
        scn.ntzSym.cutLocation        = "LOCAL"
        scn.ntzSym.cutRotation        = "LOCAL"
        scn.ntzSym.fillAfterCut       = "NO_FILL"
        scn.ntzSym.keepMirrorModifier = "NO"

        return {'FINISHED'}
    # END execute()

# END Operator()