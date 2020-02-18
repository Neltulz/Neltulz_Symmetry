import bpy

from .         import miscFunc

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
    
        scn.ntzSym.cutLocation                 = "DEFAULT"
        scn.ntzSym.cutRotation                 = "DEFAULT"
        scn.ntzSym.fillAfterCut                = "NO_FILL"
        scn.ntzSym.keepModifiers               = "NO"
        scn.ntzSym.defaultOperatorShowOptions  = "UNSET"
        scn.ntzSym.removeEmpties               = "YES"
        scn.ntzSym.removeBisectPlanes          = "YES"

        return {'FINISHED'}
    # END execute()

# END Operator()

# -----------------------------------------------------------------------------
#    Write Icon to File
# -----------------------------------------------------------------------------    

class NTZSYM_OT_writeicontofile(Operator):
    """Tooltip"""
    bl_idname = "ntz_sym.writeicontofile"
    bl_label = "Neltulz - Symmetry - Write Icon to File"
    bl_description = 'Write Icon to File'
    bl_options = {'REGISTER', 'UNDO'}

    scale : FloatProperty(
        default = 0.3
    )

    color : FloatVectorProperty (
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        default = (1.0, 1.0, 1.0, 1.0),
    )

    name : StringProperty(
        default = "Icon",
    )

    normalize : BoolProperty (
        default = True,
    )

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scn = context.scene

        miscFunc.createIconInfoFromGeo(self, context, self.name, self.color, self.scale, normalize=self.normalize)

        return {'FINISHED'}
    # END execute()

# END Operator()



# -----------------------------------------------------------------------------
#    Apply or Remove Mirror Modifier
# -----------------------------------------------------------------------------    

class NTZSYM_OT_applyorremovemodifier(Operator):
    """Tooltip"""
    bl_idname = "ntz_sym.applyorremovemodifier"
    bl_label = "Neltulz - Symmetry - Remove or Apply Mirror Modifier"
    bl_description = 'Remove Mirror Modifier'
    bl_options = {'REGISTER', 'UNDO'}

    tooltip : StringProperty(options={'HIDDEN'})

    method_List = [
        ("APPLY",  "Apply",  "", "", 0),
        ("REMOVE", "Remove", "", "", 1),
    ]

    method : EnumProperty (
        items       = method_List,
        name        = "Method",
        description = "Apply or Remove modifier",
        default     = "APPLY"
    )

    removeEmpty : BoolProperty (
        name    = "Remove Empty",
        default = True,
    )

    removeBisectPlane : BoolProperty (
        name    = "Remove Bisect Plane",
        default = True,
    )
    #END Operator  Properties

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip
    #END description()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scn = context.scene

        modeAtBegin = "OBJECT" #declare
        try:    modeAtBegin = bpy.context.object.mode
        except: pass

        activeObj = context.view_layer.objects.active
        selObjs = set(context.selected_objects)

        if modeAtBegin == "EDIT":
            editModeObjs = set(bpy.context.objects_in_mode)

            #combine selObjs and editModeObjs (useful for applying/removing modifiers in edit mode)
            selObjs = selObjs.union(editModeObjs)



        objsToRemove = set()

        for obj in selObjs:
            
            
            #check if mirrorParent exists on empty or bisectPlane
            mirrorParent = getattr(obj, "mirrorParent", None)

            if mirrorParent is not None:

                mirrorModifier = miscFunc.findModifier(obj=mirrorParent, modifierType='MIRROR')
                bisectModifier = miscFunc.findModifier(obj=mirrorParent, modifierType='BOOLEAN', modifierName='Neltulz - Bisect')

                mirrorBisectPlane = None #declare
                if bisectModifier is not None:
                    mirrorBisectPlane = bisectModifier.object

                    if self.method == "REMOVE":
                        mirrorParent.modifiers.remove(bisectModifier)

                    elif self.method == "APPLY":
                        context.view_layer.objects.active = mirrorParent

                        bpy.ops.object.mode_set(mode='OBJECT') #Switch to object mode
                        
                        bpy.ops.object.modifier_apply(modifier=bisectModifier.name)

                        if modeAtBegin == "EDIT":
                            bpy.ops.object.mode_set(mode='EDIT') #Switch to edit mode


                mirrorEmpty = None #declare
                if mirrorModifier is not None:
                    mirrorEmpty = mirrorModifier.mirror_object

                    if self.method == "REMOVE":
                        mirrorParent.modifiers.remove(mirrorModifier)

                    elif self.method == "APPLY":
                        context.view_layer.objects.active = mirrorParent

                        bpy.ops.object.mode_set(mode='OBJECT') #Switch to object mode

                        bpy.ops.object.modifier_apply(modifier=mirrorModifier.name)

                        if modeAtBegin == "EDIT":
                            bpy.ops.object.mode_set(mode='EDIT') #Switch to edit mode


                if mirrorEmpty is not None:
                    if self.removeEmpty:
                        objsToRemove.add(mirrorEmpty)

                if mirrorBisectPlane is not None:
                    if self.removeBisectPlane:
                        objsToRemove.add(mirrorBisectPlane)
            
            #check if object has a bisect(boolean) modifier
            bisectModifier = miscFunc.findModifier(obj=obj, modifierType='BOOLEAN', modifierName='Neltulz - Bisect')
            if bisectModifier is not None:

                mirrorBisectPlane = None #declare
                if bisectModifier is not None:
                    mirrorBisectPlane = bisectModifier.object

                    if self.method == "REMOVE":
                        obj.modifiers.remove(bisectModifier)

                    if self.method == "APPLY":
                        context.view_layer.objects.active = obj

                        bpy.ops.object.mode_set(mode='OBJECT') #Switch to object mode

                        bpy.ops.object.modifier_apply(modifier=bisectModifier.name)

                        if modeAtBegin == "EDIT":
                            bpy.ops.object.mode_set(mode='EDIT') #Switch to edit mode

                if mirrorBisectPlane is not None:
                    if self.removeBisectPlane:
                        objsToRemove.add(mirrorBisectPlane)

            #check if object has a mirror modifier
            mirrorModifier = miscFunc.findModifier(obj=obj, modifierType='MIRROR')
            
            if mirrorModifier is not None:

                mirrorEmpty = None #declare
                if mirrorModifier is not None:
                    mirrorEmpty = mirrorModifier.mirror_object

                    if self.method == "REMOVE":
                        obj.modifiers.remove(mirrorModifier)

                    elif self.method == "APPLY":
                        context.view_layer.objects.active = obj

                        bpy.ops.object.mode_set(mode='OBJECT') #Switch to object mode

                        bpy.ops.object.modifier_apply(modifier=mirrorModifier.name)

                        if modeAtBegin == "EDIT":
                            bpy.ops.object.mode_set(mode='EDIT') #Switch to edit mode

                if mirrorEmpty is not None:
                    if self.removeEmpty:
                        objsToRemove.add(mirrorEmpty)

        
        for obj in objsToRemove:
            bpy.data.objects.remove(obj, do_unlink=True)


        return {'FINISHED'}
    # END execute()


    def invoke(self, context, event):
        scn = context.scene

        if event.ctrl:
            self.removeEmpty = False
            self.removeBisectPlane = False
        else:
            if scn.ntzSym.removeEmpties in ["UNSET", "YES"]:
                self.removeEmpty = True
            else:
                self.removeEmpty = False

            if scn.ntzSym.removeBisectPlanes in ["UNSET", "YES"]:
                self.removeBisectPlane = True
            else:
                self.removeBisectPlane = False


        return self.execute(context)
    # END invoke()

# END Operator()