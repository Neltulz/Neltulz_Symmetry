import bpy
import bmesh
import mathutils
import math

from .             import misc_ot
from .             import miscLay
from .             import miscFunc

from bpy.props     import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types     import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#    Main Addon Operator
# -----------------------------------------------------------------------------    

class NTZSYM_OT_ntzperformsym(Operator):
    """Tooltip"""
    bl_idname = "ntz_sym.performsym"
    bl_label = "Neltulz - Symmetry"
    bl_description = 'Perform symmetry on mesh object'
    bl_options = {'REGISTER', 'UNDO'}

    tooltip : StringProperty(options={'HIDDEN'})

    

    pivotPointTransformAtInvoke = None

    operatorShowOptions : BoolProperty (
        name    = "Show Options",
        default = False
    )

    cursorLocationAtInvoke : FloatVectorProperty (
        name    = "Pivot Location at Invoke",
        default = (0,0,0),
    )

    symType_List = [
        ("SLICE",  "Slice",          "", "", 0),
        ("CUT",    "Cut",            "", "", 1),
        ("MIRROR", "Mirror",         "", "", 2),
    ]

    symType : EnumProperty (
        items       = symType_List,
        name        = "Symmetry Type",
        description = "Which type of Symmetry to perform (Cut or Symmetry)",
        default     = "CUT"
    )

    cutLocation_List = [
        ("DEFAULT",  "Default",         "",                        "FAKE_USER_ON",          0),
        None,
        ("GLOBAL",   "Global",          "",                        "ORIENTATION_GLOBAL",    1),
        ("OBJECT",   "Object",          "",                        "OBJECT_ORIGIN",         2),
        ("BOUNDING", "Bounding Box",    "",                        "PIVOT_BOUNDBOX",        3),
        ("MEDIAN",   "Median",          "",                        "PIVOT_MEDIAN",          4),
        ("CURSOR",   "Cursor",          "",                        "ORIENTATION_CURSOR",    5),
    ]

    cutLocation : EnumProperty (
        items       = cutLocation_List,
        name        = "Cut Location",
        description = "Where the cut should begin",
        default     = "OBJECT",
    )

    cutRotation_List = [
        ("DEFAULT",  "Default",   "",                        "FAKE_USER_ON",          0),
        None,
        ("GLOBAL",   "Global",    "",                        "ORIENTATION_GLOBAL",    1),
        ("LOCAL",    "Local",     "",                        "ORIENTATION_LOCAL",     2),
        ("NORMAL",   "Normal",    "",                        "ORIENTATION_NORMAL",    3),
        ("VIEW",     "View",      "",                        "ORIENTATION_VIEW",      4),
        ("CURSOR",   "Cursor",    "",                        "ORIENTATION_CURSOR",    5),
        ("CUSTOM",   "Custom",    "",                        "",                      6),
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
        ("BACKWARD", "", "", "BACK",    0),
        ("FORWARD",  "", "", "FORWARD", 1),
    ]

    axisDir : EnumProperty (
        items       = axisDir_List,
        name        = "Axis Direction",
        description = "Which direction to perform the cut or symmetry",
        default     = "FORWARD"
    )

    use_fill : BoolProperty (
        name        = "Use Fill",
        description = "Fill the hole with an NGON after performing a cut",
        default     = False
    )

    flip_fill_normal : BoolProperty (
        name = "Flip Fill Normal",
        description = 'Flips the newly created face when using "Fill"',
        default = True,
    )


    reset_mergeThreshold : BoolProperty (
        name = "Reset Merge Threshold",
        default = False,
    )

    useMerge : BoolProperty (
        name = "Use Merge",
        default = True,
    )

    mergeThreshold : FloatProperty (
        name        = "Limit",
        description = "Merge Threshold when mirroring",
        min         = 0,
        soft_min    = 0,
        soft_max    = 0.01,
        default     = 0.000001,
        precision   = 6,
    )

    useBisectPlane : BoolProperty (
        name        = "Use Bisect Plane",
        description = 'Uses a bisect plane to reduce vertice overlap artifacts when mirroring objects.  Side effect: Sometimes causes ngons to appear interior of geometry.  Tip: Remember to check interior for ngons, and cleanup non-manifold geometry',
        default     = False,
    )


    reset_tweakBisect : BoolProperty (
        name = "Reset Offset Bisect",
        default = False,
    )

    tweakBisect : FloatProperty (
        name        = "Tweak",
        description = "Tweak bisect plane by offsetting it slightly",
        soft_min    = -0.005,
        soft_max    = 0.005,
        default     = 0,
        precision   = 6,
    )

    keepModifiers : BoolProperty (
        name        = "Keep Modifiers",
        description = "Preserves the mirror and bisect modifiers when complete",
        default     = False
    )
    #END Operator  Properties
    

    @classmethod
    def description(cls, context, properties):
        return properties.tooltip
    #END description()

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        scn = context.scene
        lay = self.layout.column(align=True)

        scale_y = 1
        labelScale = 4
        propScale = 15
        labelAlign = "RIGHT"
        propAlignment = "EXPAND"
        propAlign = True
        labelJustify = "RIGHT"




        if self.operatorShowOptions:

            box = lay.box().column(align=True)
            
                
                

            if self.symType in ['SLICE', 'CUT', 'MIRROR']:  

                #miscLay.createProp( self, context, scn,  bEnabled,             bActive,                bUseCol,    labelText,           data,    checkboxProp,       propItem,                  scale_y, labelScale, propScale, labelAlign,    propAlignment,   propAlign,   propText,    bExpandProp, propColCount,  bUseSlider, resetProp,                 layout )
                miscLay.createProp(  self, context, None, True,                 True,                   False,      "Location",          self,    None,               "cutLocation",             scale_y, labelScale, propScale, labelAlign,    propAlignment,   propAlign,   "",          False,       1,             False,      None,                      box    )
                
                box.separator()
                
                miscLay.createProp(  self, context, None, True,                 True,                   False,      "Rotation",          self,    None,               "cutRotation",             scale_y, labelScale, propScale, labelAlign,    propAlignment,   propAlign,   "",          False,       1,             False,      None,                      box    )
                
            

            fillEnabled = False #declare
            if self.symType == "CUT":

                box.separator()

                fillEnabled = True
                row = box.row(align=True)
                
                useFillRow = row.row(align=True)
                useFillRow.alignment = "RIGHT"
                useFillRow.ui_units_x = 3
                useFillBool = useFillRow.prop(self, "use_fill")

                flipNormalRow = row.row(align=True)

                flipNormalRow.active = self.use_fill

                flipNormalRow.alignment = "RIGHT"
                flipNormalRow.ui_units_x = 2
                flipNormalBool = flipNormalRow.prop(self, "flip_fill_normal", text="Flip Normal")

            if self.symType == "MIRROR":
                
                box.separator()

                #miscLay.createProp( self, context, scn,  bEnabled,             bActive,                bUseCol,    labelText,           data,    checkboxProp,       propItem,                  scale_y, labelScale, propScale, labelAlign,    propAlignment,   propAlign,   propText,    bExpandProp, propColCount,  bUseSlider, resetProp,                 layout )
                miscLay.createProp(  self, context, None, True,                 self.useBisectPlane,    False,      "Bisect",            self,    "useBisectPlane",   "tweakBisect",            scale_y, labelScale, propScale, labelAlign,    propAlignment,   propAlign,   None,        True,        1,             True,       "reset_tweakBisect",      box    )
                
                box.separator()
                
                miscLay.createProp(  self, context, None, True,                 self.useMerge,          False,      "Merge",             self,    "useMerge",         "mergeThreshold",          scale_y, labelScale, propScale, labelAlign,    propAlignment,   propAlign,   None,        True,        1,             True,       "reset_mergeThreshold",    box    )
                
                box.separator()

                miscLay.createProp(  self, context, None, True,                 True,                   False,      "",                  self,    None,               "keepModifiers",           scale_y, labelScale, propScale, labelAlign,    propAlignment,   propAlign,   None,        True,        1,             False,      None,                      box    )
           

            lay.separator()

            

        row = lay.row(align=True)
        row.scale_y = 1.25
        row.prop(self, "symType", expand=True)
        row.separator()

        if self.operatorShowOptions:
            icon = "TRIA_UP"
        else:
            icon = "TRIA_RIGHT"

        row.prop(self, "operatorShowOptions", toggle=True, text="", icon=icon, emboss=True)

        lay.separator()
        #miscLay.createProp( self, context, scn,  bEnabled,          bActive, bUseCol,    labelText,           data,    checkboxprop,       propItem,                  scale_y, labelScale, propScale, labelAlign,    propAlignment,   propAlign,   propText,    bExpandProp, propColCount,  bUseSlider, resetProp, layout )
        
        axisAndDirRow = lay.row(align=True)

        row = axisAndDirRow.row(align=True)
        row.prop(self, "axis", expand=True)

        axisAndDirRow.separator()

        row = axisAndDirRow.grid_flow(columns=2, align=True)
        if self.symType == "SLICE":
            row.active = False
        row.scale_x = 4
        row.prop(self, "axisDir", expand=True, text="")

        #miscLay.createProp(  self, context, None, True,              True,    False,      "",                  self,    None,               "axis",                    scale_y, 0,          propScale, labelAlign,    propAlignment,   propAlign,   None,        True,        1,             False,      None,      lay    )
        #miscLay.createProp(  self, context, None, True,              True,    False,      "",                  self,    None,               "axisDir",                 scale_y, 0,          propScale, labelAlign,    propAlignment,   propAlign,   None,        True,        2,             False,      None,      lay    )

    #END draw()

    def execute(self, context):

        propsToReset = [
            ['reset_mergeThreshold', ['useMerge',       'mergeThreshold'] ],
            ['reset_tweakBisect',   ['useBisectPlane', 'tweakBisect']   ],
        ]

        miscFunc.resetOperatorProps(self, context, propsToReset)

        scn = context.scene

        #update operatorShowOptions in the scene properties
        scn.ntzSym.operatorShowOptions = self.operatorShowOptions
        
            
        modeAtBegin = "OBJECT" #declare
        try:    modeAtBegin = bpy.context.object.mode
        except: pass

        activeObj = context.view_layer.objects.active

        selObjs = context.selected_objects

        obj = None #declare
        if len(selObjs) > 0:
            obj = selObjs[0]
            if activeObj is None:
                context.view_layer.objects.active = obj
        else:
            if modeAtBegin == "EDIT":
                if activeObj is not None:
                    selObjs.append(activeObj)
                    activeObj.select_set(True)
            else:
                obj = None
                self.report({'WARNING'}, 'Please select an object' )

        

        if obj is not None:

            ###############################################################################################################################################################################
            # Determine Rotation
            ###############################################################################################################################################################################
            
            rotResult = mathutils.Euler((0, 0, 0)).to_quaternion() #declare

            transformOrientation = scn.transform_orientation_slots[0]
            
            if self.cutLocation == "DEFAULT":
                pass #use last known transform pivot point location

            elif self.cutLocation == "MEDIAN":
                scn.tool_settings.transform_pivot_point = "MEDIAN_POINT"

            elif self.cutLocation == "BOUNDING":
                scn.tool_settings.transform_pivot_point = "BOUNDING_BOX_CENTER"
            
            bpy.ops.view3d.snap_cursor_to_selected()

            if self.cutRotation == "DEFAULT":
                
                if transformOrientation.type == 'GLOBAL':
                    rotResult = miscFunc.getRot(self, context, scn, orient='GLOBAL', toQuat=True)

                elif transformOrientation.type == 'VIEW':
                    rotResult = miscFunc.getRot(self, context, scn, orient='VIEW', toQuat=True)
                
                elif transformOrientation.type == "NORMAL":
                    rotResult = miscFunc.getRot(self, context, scn, orient='NORMAL', toQuat=True)
                
                elif transformOrientation.type == "CURSOR":
                    rotResult = miscFunc.getRot(self, context, scn, orient='CURSOR', obj=obj, toQuat=True, modeAtBegin=modeAtBegin, activeObj=activeObj)
                
                else:
                    if transformOrientation.custom_orientation is not None:
                        if transformOrientation.type == transformOrientation.custom_orientation.name:
                            rotResult = miscFunc.getRot(self, context, scn, orient='CUSTOM', toQuat=True)
                        else:
                            rotResult = miscFunc.getRot(self, context, scn, orient='LOCAL', toQuat=True, obj=obj)
                    else:
                        rotResult = miscFunc.getRot(self, context, scn, orient='LOCAL', toQuat=True, obj=obj)


            elif self.cutRotation == "GLOBAL":
                rotResult = miscFunc.getRot(self, context, scn, orient='GLOBAL', toQuat=True)

            elif self.cutRotation == "LOCAL":
                rotResult = miscFunc.getRot(self, context, scn, orient='LOCAL', toQuat=True, obj=obj)

            elif self.cutRotation == "NORMAL":
                rotResult = miscFunc.getRot(self, context, scn, orient='NORMAL', toQuat=True)

            elif self.cutRotation == "VIEW":
                rotResult = miscFunc.getRot(self, context, scn, orient='VIEW', toQuat=True)

            elif self.cutRotation == "CURSOR":
                rotResult = miscFunc.getRot(self, context, scn, orient='CURSOR', obj=obj, toQuat=True, modeAtBegin=modeAtBegin, activeObj=activeObj)

            elif self.cutRotation == "CUSTOM":
                if transformOrientation.custom_orientation is not None:
                    if transformOrientation.type == transformOrientation.custom_orientation.name:
                        rotResult = miscFunc.getRot(self, context, scn, orient='CUSTOM', toQuat=True)
                    else:
                        rotResult = miscFunc.getRot(self, context, scn, orient='LOCAL', toQuat=True, obj=obj)
                else:
                    rotResult = miscFunc.getRot(self, context, scn, orient='LOCAL', toQuat=True, obj=obj)


            ###############################################################################################################################################################################
            # Determine Location
            ###############################################################################################################################################################################

            locationResult = (0,0,0) #declare
            
            if self.cutLocation == "DEFAULT":
                    
                if self.pivotPointTransformAtInvoke == "CURSOR":
                    locationResult = miscFunc.getLocation(self, context, scn, location='CURSOR')
                
                else:
                    locationResult = miscFunc.getLocation(self, context, scn, location='MEDIAN_OR_BOUNDING')


            elif self.cutLocation == "GLOBAL":
                locationResult = miscFunc.getLocation(self, context, scn, location='GLOBAL')
            
            elif self.cutLocation == "OBJECT":
                locationResult = miscFunc.getLocation(self, context, scn, location='OBJECT', obj=obj)

            elif self.cutLocation == "BOUNDING":
                locationResult = miscFunc.getLocation(self, context, scn, location='MEDIAN_OR_BOUNDING')

            elif self.cutLocation == "MEDIAN":
                locationResult = miscFunc.getLocation(self, context, scn, location='MEDIAN_OR_BOUNDING')

            elif self.cutLocation == "CURSOR":
                locationResult = miscFunc.getLocation(self, context, scn, location='CURSOR')

            ###############################################################################################################################################################################
            # Slice or Cut
            ###############################################################################################################################################################################

            if self.symType in ["SLICE", "CUT"]:

                if self.axis == "X":
                    vec = mathutils.Vector((1, 0, 0))

                elif self.axis == "Y":
                    vec = mathutils.Vector((0, 1, 0))

                elif self.axis == "Z":
                    vec = mathutils.Vector((0, 0, 1))

                vec.rotate(rotResult)
                planeNormal = vec

                
                    
                clear_inner=False #declare
                clear_outer=False #declare

                if self.symType in ["CUT"]:

                    if self.axisDir == "FORWARD":
                        clear_inner=False
                        clear_outer=True

                    elif self.axisDir == "BACKWARD":
                        clear_inner=True
                        clear_outer=False

                elif self.symType == "SLICE":
                    clear_inner=False
                    clear_outer=False

                # Perform destructive bisect operation
                #-------------------------------------
                bpy.ops.object.mode_set(mode='EDIT') #Switch to edit mode
                bpy.ops.mesh.select_all(action='SELECT')

                bpy.ops.mesh.bisect(plane_co=locationResult, plane_no=planeNormal, xstart=0, xend=0, ystart=0, yend=0, use_fill=self.use_fill, clear_inner=clear_inner, clear_outer=clear_outer)

                # Flip normals if cutting
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if self.symType == "CUT":
                    if self.use_fill and self.flip_fill_normal:
                        bpy.ops.mesh.flip_normals()
                
                if modeAtBegin == "OBJECT":
                    bpy.ops.object.mode_set(mode='OBJECT') #Switch back to edit mode



            ###############################################################################################################################################################################
            # Mirror
            ###############################################################################################################################################################################

            elif self.symType == "MIRROR":
                

                bpy.ops.object.mode_set(mode='OBJECT') #Switch to object mode
                

                # Add Empty Object (When Mirroring)
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

                #determine dimension of object so that the empty object is larger than the object
                objMaxDim = miscFunc.dimensionsFromObj(self, context, obj, "MAX")

                bpy.ops.object.empty_add(type='ARROWS', radius=objMaxDim, align='WORLD', rotation=rotResult, location=locationResult)
                mirrorEmpty = context.view_layer.objects.active
                mirrorEmpty.name = "Neltulz - Mirror Empty"



                # Add Bisect Plane and add Bisect Modifier (When Mirroring)
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if self.useBisectPlane:
                    
                    # Determine whether bisect plane should be Differenced or Intersected, and determine bisect plane rotation
                    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

                    if self.axis == "X":
                        if self.axisDir == "FORWARD":
                            bisectOperation = "INTERSECT"
                            planeRot = (0,math.radians(90),0)

                        elif self.axisDir == "BACKWARD":
                            bisectOperation = "DIFFERENCE"
                            planeRot = (0,math.radians(-90),0)

                    elif self.axis == "Y":
                        if self.axisDir == "FORWARD":
                            bisectOperation = "DIFFERENCE"
                            planeRot = (0,math.radians(90),math.radians(90))

                        elif self.axisDir == "BACKWARD":
                            bisectOperation = "DIFFERENCE"
                            planeRot = (0,math.radians(90),math.radians(-90))

                    elif self.axis == "Z":
                        if self.axisDir == "FORWARD":
                            bisectOperation = "DIFFERENCE"
                            planeRot = (0,0,0)

                        elif self.axisDir == "BACKWARD":
                            bisectOperation = "DIFFERENCE"
                            planeRot = (0,0,0)

                    # Add Bisect Plane
                    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------        
                    bpy.ops.mesh.primitive_plane_add(size=(objMaxDim * 10), enter_editmode=False, align='WORLD', rotation=planeRot)

                    bisectMesh = context.view_layer.objects.active
                    bisectMesh.name = 'Neltulz - Mirror Bisect'


                    # Offset Bisect Plane
                    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

                    if self.axisDir == "FORWARD":
                        offsetValue = self.tweakBisect
                    elif self.axisDir == "BACKWARD":
                        offsetValue = self.tweakBisect * -1

                    if self.axis == "X":
                        finalOffsetValue = (offsetValue, 0, 0)

                    if self.axis == "Y":
                        finalOffsetValue = (0, offsetValue,0)

                    if self.axis == "Z":
                        finalOffsetValue = (0, 0, offsetValue)

                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                    bpy.ops.transform.translate(value=finalOffsetValue, orient_type='LOCAL')
                

                

                #Store a pointer to the object on the empty so that the user can apply the mirror modifier from the empty later
                mirrorEmpty.mirrorParent = obj
                if self.useBisectPlane:
                    bisectMesh.mirrorParent = obj

                # Make Empty the active object
                context.view_layer.objects.active = mirrorEmpty

                # Parent the bisect plane to the empty, then hide the bisect plane.
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------
                if self.useBisectPlane:
                    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
                
                    context.view_layer.objects.active = bisectMesh
                    bpy.context.object.hide_set(True)

                    bisectMesh.rotation_euler = rotResult
                    bisectMesh.display_type = 'WIRE'

                    bisectModifier = obj.modifiers.new("Neltulz - Bisect", 'BOOLEAN')
                    bisectModifier.operation = bisectOperation
                    bisectModifier.object = bisectMesh



                # Make empty the active object and select it
                context.view_layer.objects.active = mirrorEmpty
                mirrorEmpty.select_set(True)

                # Add Mirror Modifier
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

                mirrorModifier = obj.modifiers.new("Neltulz - Mirror", 'MIRROR')
                mirrorModifier.mirror_object = mirrorEmpty
                
                mirrorModifier.show_on_cage = True

                # Determine which bisect axis to use for the mirror modifier
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if self.axis == "X":
                    mirrorModifier.use_bisect_axis[0] = True
                    mirrorModifier.use_bisect_axis[1] = False
                    mirrorModifier.use_bisect_axis[2] = False

                    mirrorModifier.use_axis[0] = True
                    mirrorModifier.use_axis[1] = False
                    mirrorModifier.use_axis[2] = False

                elif self.axis == "Y":
                    mirrorModifier.use_bisect_axis[0] = False
                    mirrorModifier.use_bisect_axis[1] = True
                    mirrorModifier.use_bisect_axis[2] = False

                    mirrorModifier.use_axis[0] = False
                    mirrorModifier.use_axis[1] = True
                    mirrorModifier.use_axis[2] = False

                elif self.axis == "Z":
                    mirrorModifier.use_bisect_axis[0] = False
                    mirrorModifier.use_bisect_axis[1] = False
                    mirrorModifier.use_bisect_axis[2] = True

                    mirrorModifier.use_axis[0] = False
                    mirrorModifier.use_axis[1] = False
                    mirrorModifier.use_axis[2] = True

                # Set Merge and Merge Threshold of mirror modifier
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

                mirrorModifier.use_mirror_merge = self.useMerge
                mirrorModifier.merge_threshold = self.mergeThreshold

                # Determine which flip axis to use for the mirror modifier
                #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

                if self.axisDir == "FORWARD":
                    if self.axis == "X":
                        mirrorModifier.use_bisect_flip_axis[0] = True

                    if self.axis == "Y":
                        mirrorModifier.use_bisect_flip_axis[1] = True

                    if self.axis == "Z":
                        mirrorModifier.use_bisect_flip_axis[2] = True

                else:
                    if self.axis == "X":
                        mirrorModifier.use_bisect_flip_axis[0] = False

                    if self.axis == "Y":
                        mirrorModifier.use_bisect_flip_axis[1] = False

                    if self.axis == "Z":
                        mirrorModifier.use_bisect_flip_axis[2] = False

                ###############################################################################################################################################################################
                # Remove Modifiers
                ###############################################################################################################################################################################
                
                bpy.ops.object.mode_set(mode='OBJECT') #Switch back to object mode

                if not self.keepModifiers:
                    bpy.context.view_layer.objects.active = obj
                    obj.select_set(True)

                    if self.useBisectPlane:
                        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Neltulz - Bisect")

                    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Neltulz - Mirror")

                    if self.useBisectPlane:
                        bpy.data.objects.remove(bisectMesh)
                        
                    bpy.data.objects.remove(mirrorEmpty)

                    #only switch to edit mode if removing modifiers
                    if modeAtBegin == "EDIT":
                        bpy.ops.object.mode_set(mode='EDIT') #Switch back to edit mode


        #final steps:
        scn.cursor.location                     = self.cursorLocationAtInvoke
        scn.tool_settings.transform_pivot_point = self.pivotPointTransformAtInvoke

        #final final step:
        self.wasInvoked = False

        return {'FINISHED'}
    # END execute()

    def invoke(self, context, event):
        
        scn = context.scene

        if event.ctrl:
            self.keepModifiers = True #override the "keepModifiers" scene property setting and force "keepModifiers" to True because user CTRL clicked one of the mirror buttons
        else:
            pass #determined automatically from the "keepModifiers" scene property setting


        #determine operatorShowOptions from the scene properties (the arrow button that unhides the operator options)
        if scn.ntzSym.defaultOperatorShowOptions == "UNSET":
            self.operatorShowOptions = scn.ntzSym.operatorShowOptions
        
        elif scn.ntzSym.defaultOperatorShowOptions == "HIDE":
            self.operatorShowOptions = False

        elif scn.ntzSym.defaultOperatorShowOptions == "EXPAND":
            self.operatorShowOptions = True

        self.cursorLocationAtInvoke = scn.cursor.location

        self.pivotPointTransformAtInvoke = scn.tool_settings.transform_pivot_point
    
        return self.execute(context)
    # END invoke()

# END Operator()