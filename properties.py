import bpy

from .         import miscFunc

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)



class NTZSYM_ignitproperties(PropertyGroup):

    operatorShowOptions : BoolProperty (
        name    = "Show Options",
        default = False,
    )

    defaultOperatorShowOptions_List = [
        ("UNSET",   "Unset",   "Use Last Known Settings", "",            0),
        ("HIDE",    "Hide",    "",                        "TRIA_RIGHT",  1),
        ("EXPAND",  "Expand",  "",                        "TRIA_UP",     2),
    ]

    defaultOperatorShowOptions : EnumProperty (
        items       = defaultOperatorShowOptions_List,
        name        = "Default Operator Show Options",
        description = "Hide/Expand Operator Options",
        default     = "UNSET"
    )

    bShowOptions : BoolProperty (
        name="Show Options",
        description="Reveals options.",
        default = False,
    )

    optionsPopoverEnum_List = [
        ("OPTIONS", "Options", "", "SETTINGS", 0),
    ]

    optionsPopoverEnum : EnumProperty (
        items       = optionsPopoverEnum_List,
        name        = "Options Popover Enum",
        description = "Options Popover Enum",
        default     = "OPTIONS"
    )

    cutLocation_List = [
        ("UNSET",    "Unset",           "Use Last Known Settings", "",                      0),
        None,
        ("DEFAULT",  "Default",         "",                        "FAKE_USER_ON",          1),
        None,
        ("GLOBAL",   "Global",          "",                        "ORIENTATION_GLOBAL",    2),
        ("OBJECT",   "Object",          "",                        "OBJECT_ORIGIN",         3),
        ("BOUNDING", "Bounding Box",    "",                        "PIVOT_BOUNDBOX",        4),
        ("MEDIAN",   "Median",          "",                        "PIVOT_MEDIAN",          5),
        ("CURSOR",   "Cursor",          "",                        "ORIENTATION_CURSOR",    6),
    ]

    cutLocation : EnumProperty (
        items       = cutLocation_List,
        name        = "Cut Location",
        description = "Where the cut should begin",
        default     = "DEFAULT"
    )

    cutRotation_List = [
        ("UNSET",    "Unset",     "Use Last Known Settings", "",                      0),
        None,
        ("DEFAULT",  "Default",   "",                        "FAKE_USER_ON",          1),
        None,
        ("GLOBAL",   "Global",    "",                        "ORIENTATION_GLOBAL",    2),
        ("LOCAL",    "Local",     "",                        "ORIENTATION_LOCAL",     3),
        ("NORMAL",   "Normal",    "",                        "ORIENTATION_NORMAL",    4),
        ("VIEW",     "View",      "",                        "ORIENTATION_VIEW",      5),
        ("CURSOR",   "Cursor",    "",                        "ORIENTATION_CURSOR",    6),
        ("CUSTOM",   "Custom",    "",                        "",                      7),
    ]

    cutRotation : EnumProperty (
        items       = cutRotation_List,
        name        = "Cut Rotation",
        description = "The rotation of the cut should",
        default     = "DEFAULT"
    )

    fillAfterCut_List = [
        ("UNSET",   "Unset", "Use Last Known Settings", "",            0),
        None,
        ("NO_FILL", "No",    "",                        "X",           1),
        ("FILL",    "Yes",   "",                        "CHECKMARK",   2),
    ]

    fillAfterCut : EnumProperty (
        items       = fillAfterCut_List,
        name        = "Fill",
        description = "Fill the empty hole with an NGON after performing a cut",
        default     = "NO_FILL"
    )

    keepModifiers_List = [
        ("UNSET", "Unset", "Use Last Known Settings", "",          0),
        None,
        ("NO",    "No",    "",                        "X",         1),
        ("YES",   "Yes",   "",                        "CHECKMARK", 2),
    ]

    keepModifiers : EnumProperty (
        items       = keepModifiers_List,
        name        = "Keep Modifiers",
        description = "Preserves the mirror and bisect modifiers when complete",
        default     = "NO"
    )

    removeEmpties_List = [
        ("UNSET", "Unset", "Use Last Known Settings", "",          0),
        None,
        ("NO",    "No",    "",                        "X",         1),
        ("YES",   "Yes",   "",                        "CHECKMARK", 2),
    ]

    removeEmpties : EnumProperty (
        items       = removeEmpties_List,
        name        = "Remove Empties",
        description = "Removes Empties when applying or removing modifiers",
        default     = "YES"
    )
    
    removeBisectPlanes_List = [
        ("UNSET", "Unset", "Use Last Known Settings", "",          0),
        None,
        ("NO",    "No",    "",                        "X",         1),
        ("YES",   "Yes",   "",                        "CHECKMARK", 2),
    ]

    removeBisectPlanes : EnumProperty (
        items       = removeBisectPlanes_List,
        name        = "Remove Bisect Planes",
        description = "Removes Bisect Planes when applying or removing modifiers",
        default     = "YES"
    )

#END NTZSYM_ignitproperties()