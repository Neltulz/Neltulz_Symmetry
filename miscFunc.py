import bpy
import bmesh
import mathutils

from operator      import itemgetter

import numpy
from itertools import chain
from itertools import permutations


def load_handler():
    bpy.app.handlers.undo_pre.append(prop_store)
    bpy.app.handlers.undo_post.append(prop_restore)
    bpy.app.handlers.redo_pre.append(prop_store)
    bpy.app.handlers.redo_post.append(prop_restore)

def unload_handler():
    bpy.app.handlers.undo_pre.remove(prop_store)
    bpy.app.handlers.undo_post.remove(prop_restore)
    bpy.app.handlers.redo_pre.remove(prop_store)
    bpy.app.handlers.redo_post.remove(prop_restore)

@bpy.app.handlers.persistent
def prop_store(scn):

    scn = bpy.context.scene

    vars(prop_store)["orientation"] = scn.transform_orientation_slots[0].type
    vars(prop_store)["transformpivot"] = scn.tool_settings.transform_pivot_point


@bpy.app.handlers.persistent
def prop_restore(scn):
    scn = bpy.context.scene

    orientation = vars(prop_store).get("orientation")
    if orientation is not None:
        transformpivot = vars(prop_store).get("transformpivot")
        scn.transform_orientation_slots[0].type = orientation
        scn.tool_settings.transform_pivot_point    = transformpivot

def average(lst): 
    return sum(lst) / len(lst) 

def remap(inputValue, minA, maxA, minB, maxB, useInt):
    OldRange = (maxA - minA)
    NewRange = (maxB - minB)

    result = (((inputValue - minA) * NewRange) / OldRange) + minB

    if useInt:
        result = int(result)

    return result

#Reset Operators to their default values:
def resetOperatorProps(self, context, propsToReset):

    # EXAMPLE OF propsToReset - ADD THIS TO THE TOP OF THE execute() IN YOUR OPERATOR AND CUSTOMIZE
    #
    # propsToReset = [
    #     ["reset_allVisibilityModes", ["render", "realtime", "editmode", "cage"] ],
    #     ["reset_affect", ["affect"] ],
    # ]

    for item in propsToReset:

        resetBoolPropName = item[0]
        resetBool = getattr(self, resetBoolPropName)

        if resetBool == True:

            for propName in item[1]:
                defaultVal = self.__annotations__[propName][1]['default']

                setattr(self, propName, defaultVal)
                setattr(self, resetBoolPropName, False)

def dimensionsFromObj(self, context, obj, returnType):

    x = obj.dimensions.x
    y = obj.dimensions.y
    z = obj.dimensions.z

    if returnType == "X":
        return x

    elif returnType == "Y":
        return y

    elif returnType == "Z":
        return z

    elif returnType == "XYZ":
        return [x,y,z]

    elif returnType == "MAX":
        return max([x,y,z])

    elif returnType == "MIN":
        return min([x,y,z])

    elif returnType == "AVG":
        return average([x,y,z])

def bboxFromSelection():

    #returns the bounding box of a selection.  Special thanks and Source: iceythe
    all_vcos = []
    # Get all vert cos from objects in edit mode
    for o in bpy.context.objects_in_mode_unique_data:
        bm = bmesh.from_edit_mesh(o.data)
        mat = o.matrix_world
        all_vcos.extend([mat @ v.co for v in bm.verts if v.select])

    (x1, y1, z1,
     x2, y2, z2) = [func(all_vcos, key=itemgetter(i))[i]
                    for func in (min, max) for i in range(3)]

    bbox = (
        (x1, y1, z1), (x1, y1, z2),
        (x2, y1, z2), (x2, y1, z1),

        # mirror other size
        (x1, y2, z1), (x1, y2, z2),
        (x2, y2, z2), (x2, y2, z1))

    bbox_vecs = [Vector(i) for i in bbox]

    return bbox_vecs

def dimensionsFromSelection(self, context, minMaxAvg):

    #Get dimension from selection - Special thanks & source: iceythe

    all_vcos = []
    # Get all vert cos from objects in edit mode
    for o in bpy.context.objects_in_mode_unique_data:
        bm = bmesh.from_edit_mesh(o.data)
        mat = o.matrix_world
        all_vcos.extend([(mat @ v.co)[:] for v in bm.verts if v.select])

    it = numpy.fromiter(chain.from_iterable(all_vcos), dtype=float)
    it.shape = (len(all_vcos), 3)
    _min, _max = Vector(it.min(0).tolist()), Vector(it.max(0).tolist())

    if minMaxAvg == "MIN":
        result = min((_max - _min))
    elif minMaxAvg == "MAX": 
        result = max((_max - _min))
    elif minMaxAvg == "AVG":
        result = average((_max - _min))

    return result

def getRotFromNormal(self, context, scn):

    transformOrientation = scn.transform_orientation_slots[0]

    originalOrientation = transformOrientation.type

    transformOrientation.type = "NORMAL"

    #create custom orientation
    bpy.ops.transform.create_orientation(name="NTZSYM_NORMAL", use_view=False, use=True, overwrite=True)

    custom_orientation = transformOrientation.custom_orientation
    rotation_of_custom_orientation = custom_orientation.matrix.to_euler()
    
    #delete custom orientation
    bpy.ops.transform.delete_orientation()

    #restore original orientation
    try:
        transformOrientation.type = originalOrientation
    except:
        pass

    return rotation_of_custom_orientation

def getRotFromView(self, context, scn):

    transformOrientation = scn.transform_orientation_slots[0]

    originalOrientation = transformOrientation.type

    transformOrientation.type = "NORMAL"

    #create custom orientation
    bpy.ops.transform.create_orientation(name="NTZSYM_VIEW", use_view=True, use=True, overwrite=True)

    custom_orientation = transformOrientation.custom_orientation
    rotation_of_custom_orientation = custom_orientation.matrix.to_euler()
    
    #delete custom orientation
    bpy.ops.transform.delete_orientation()

    #restore original orientation
    try:
        transformOrientation.type = originalOrientation
    except:
        pass

    return rotation_of_custom_orientation

def getRotFromCustomOrientation(self, context, scn):

    transformOrientation = scn.transform_orientation_slots[0]

    custom_orientation = transformOrientation.custom_orientation
    rotation_of_custom_orientation = custom_orientation.matrix.to_euler()
    
    return rotation_of_custom_orientation

def getRot(self, context, scn, orient='GLOBAL', obj=None, toQuat=False, modeAtBegin='OBJECT', activeObj=None):

    if orient == "GLOBAL":
        result = mathutils.Euler((0,0,0))
        
    elif orient == "LOCAL":
        result = obj.rotation_euler

    elif orient == "CURSOR":

        if modeAtBegin == "EDIT":
            bpy.ops.object.mode_set(mode='OBJECT') #Switch to object mode

        bpy.ops.object.empty_add(type='PLAIN_AXES', align='CURSOR', location=self.cursorLocationAtInvoke)
        cursorEmpty = context.view_layer.objects.active

        result = cursorEmpty.rotation_euler

        bpy.data.objects.remove(cursorEmpty)

        #if active object is specified, it can be made the active object again, and reselected
        if activeObj is not None:
            context.view_layer.objects.active = activeObj
            activeObj.select_set(True)

        if modeAtBegin == "EDIT":
            bpy.ops.object.mode_set(mode='EDIT') #Switch to Edit mode

    elif orient == "NORMAL":
        result = getRotFromNormal(self, context, scn)

    elif orient == "VIEW":
        result = getRotFromView(self, context, scn)

    elif orient == "CUSTOM":
        result = getRotFromCustomOrientation(self, context, scn)

    if toQuat:
        result.to_quaternion()


    return result

def getLocation(self, context, scn, location='GLOBAL', obj=None):

    if location == "GLOBAL":
        result = (0,0,0)

    elif location == "OBJECT":
        result = obj.location

    elif location == "MEDIAN_OR_BOUNDING":
        #Note - This always gets the location of the transform pivot (technically cursor location) since the cursor is being snapped to selection at the beginning of the operator
        result = scn.cursor.location
    
    elif location == "CURSOR":
        result = self.cursorLocationAtInvoke


    return result


def findCustomPropByName(obj=None, customPropName=None):

    keyResult = None
    for key in obj.keys():
        if key not in '_RNA_UI':
            if key == customPropName:
                keyResult = obj[key]
                break

    return keyResult


def findModifier(obj=None, modifierType=None, modifierName=None):

    modifierResult = None

    for modifier in obj.modifiers:

        if modifierResult is None:

            if modifierType is not None:

                if modifier.type == modifierType:

                    if modifierName is not None:
                        if modifier.name == modifierName:
                            modifierResult = modifier
                            break

                    else:
                        modifierResult = modifier
                        break
        
        if modifierResult is None:

            if modifierName is not None:

                for modifier in obj.modifiers:

                    if modifier.name == modifierName:
                        modifierResult = modifier
                        break


    return modifierResult