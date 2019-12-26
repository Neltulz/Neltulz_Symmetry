import bpy
import mathutils
from . import misc_ot

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#    Main Addon Operator
# -----------------------------------------------------------------------------    

class NTZSYM_OT_ntzperformsym(Operator):
    """Tooltip"""
    bl_idname = "ntz_sym.performsym"
    bl_label = "Neltulz - Symmetry"
    bl_description = 'Perform symmetry on mesh object'
    bl_options = {'REGISTER', 'UNDO'}

    #BEGIN Operator Properties
    symType_List = [
        ("CUT",    "Cut",            "", "", 0),
        ("SLICE",  "Slice",          "", "", 1),
        ("MIRROR", "Cut & Mirror",   "", "", 2),
    ]

    symType : EnumProperty (
        items       = symType_List,
        name        = "Symmetry Type",
        description = "Which type of Symmetry to perform (Cut or Symmetry)",
        default     = "CUT"
    )

    cutLocation_List = [
        ("UNSET",    "Unset",      "Use Last Known Settings", "",                   0),
        ("LOCAL",    "Local",      "",                        "ORIENTATION_LOCAL",  1),
        ("GLOBAL",   "Global",     "",                        "ORIENTATION_GLOBAL", 2),
    ]

    cutLocation : EnumProperty (
        items       = cutLocation_List,
        name        = "Cut Location",
        description = "Where the cut should begin",
        default     = "LOCAL"
    )

    cutRotation_List = [
        ("UNSET",    "Unset",      "Use Last Known Settings", "",                   0),
        ("LOCAL",    "Local",      "",                        "ORIENTATION_LOCAL",  1),
        ("GLOBAL",   "Global",     "",                        "ORIENTATION_GLOBAL", 2),
    ]

    cutRotation : EnumProperty (
        items       = cutRotation_List,
        name        = "Cut Rotation",
        description = "The rotation of the cut should",
        default     = "LOCAL"
    )

    axis_List = [
        ("X", "X", "", "", 0),
        ("Y", "Y", "", "", 1),
        ("Z", "Z", "", "", 2),
    ]

    axis : EnumProperty (
        items       = axis_List,
        name        = "Axis",
        description = "Which axis to perform the cut or symmetry",
        default     = "X"
    )
    
    axisDir_List = [
        ("PLUS",  "Forwards",  "", "", 0),
        ("MINUS", "Backwards", "", "", 1),
    ]

    axisDir : EnumProperty (
        items       = axisDir_List,
        name        = "Axis Direction",
        description = "Which direction to perform the cut or symmetry",
        default     = "PLUS"
    )

    use_fill : BoolProperty (
        name        = "Use Fill",
        description = "Fill the hole with an NGON after performing a cut",
        default     = False
    )

    keepMirrorModifier : BoolProperty (
        name        = "Keep Mirror Modifier",
        description = "Preserves the mirror modifier when complete",
        default     = False
    )
    #END Operator  Properties
    



    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scn = context.scene
        

        activeObj = bpy.context.view_layer.objects.active

        selObjs = bpy.context.selected_objects

        if len(selObjs) > 0:
            obj = selObjs[0]
        else:
            obj = None
            
        modeAtBegin = bpy.context.object.mode

        if obj is None:
            self.report({'WARNING'}, 'Please select an object' )
        
        elif obj is not None:

            if modeAtBegin == "OBJECT":
                bpy.ops.object.mode_set(mode='EDIT') #Switch to edit mode

            
            bpy.ops.mesh.select_all(action='SELECT')

            plane_no = (1, 0, 0) #declare
            plane_co = (0, 0, 0) #declare

            if self.cutRotation == "GLOBAL":
                if self.axis == "X":
                    plane_no = (1, 0, 0)

                elif self.axis == "Y":
                    plane_no = (0, 1, 0)

                elif self.axis == "Z":
                    plane_no = (0, 0, 1)

            elif self.cutRotation == "LOCAL":
                
                if self.axis == "X":
                    vec = mathutils.Vector((1, 0, 0))

                elif self.axis == "Y":
                    vec = mathutils.Vector((0, 1, 0))

                elif self.axis == "Z":
                    vec = mathutils.Vector((0, 0, 1))

                vec.rotate(obj.rotation_euler)
                plane_no = vec

                

            if self.cutLocation == "GLOBAL":
                plane_co = (0, 0, 0)
            
            elif self.cutLocation == "LOCAL":
                plane_co = (obj.location[0], obj.location[1], obj.location[2])
                
            clear_inner=True #declare

            if self.symType in ["CUT", "MIRROR"]:

                if self.axisDir == "PLUS":
                    clear_inner=False
                    clear_outer=True

                elif self.axisDir == "MINUS":
                    clear_inner=True
                    clear_outer=False

            elif self.symType == "SLICE":
                clear_inner=False
                clear_outer=False

            bpy.ops.mesh.bisect(plane_co=plane_co, plane_no=plane_no, xstart=0, xend=0, ystart=0, yend=0, use_fill=self.use_fill, clear_inner=clear_inner, clear_outer=clear_outer)

            if self.symType == "MIRROR":
                mirrorModifier = obj.modifiers.new("Neltulz - Mirror", 'MIRROR')

                if self.axis == "X":
                    pass
                if self.axis == "Y":
                    mirrorModifier.use_axis[0] = False
                    mirrorModifier.use_axis[1] = True
                if self.axis == "Z":
                    mirrorModifier.use_axis[0] = False
                    mirrorModifier.use_axis[2] = True

            
            bpy.ops.object.mode_set(mode='OBJECT') #Switch back to object mode

            if not self.keepMirrorModifier:
                bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Neltulz - Mirror")

            if modeAtBegin == "EDIT":
                bpy.ops.object.mode_set(mode='EDIT') #Switch back to edit mode

        return {'FINISHED'}
    # END execute()

# END Operator()