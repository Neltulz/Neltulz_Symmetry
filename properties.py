import bpy

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

class NTZSYM_ignitproperties(PropertyGroup):

    bShowOptions : BoolProperty (
        name="Show Options",
        description="Reveals options.",
        default = False,
    )

    optionsPopoverEnum_List = [
        ("OPTIONS", "Options", "", "", 0),
    ]

    optionsPopoverEnum : EnumProperty (
        items       = optionsPopoverEnum_List,
        name        = "Options Popover Enum",
        description = "Options Popover Enum",
        default     = "OPTIONS"
    )

    cutLocation_List = [
        ("UNSET",  "Unset",  "Use Last Known Settings", "",                   0),
        ("LOCAL",  "Local",  "",                        "ORIENTATION_LOCAL",  1),
        ("GLOBAL", "Global", "",                        "ORIENTATION_GLOBAL", 2),
    ]

    cutLocation : EnumProperty (
        items       = cutLocation_List,
        name        = "Cut Location",
        description = "Where the cut should begin",
        default     = "LOCAL"
    )

    cutRotation_List = [
        ("UNSET",  "Unset",  "Use Last Known Settings", "",                   0),
        ("LOCAL",  "Local",  "",                        "ORIENTATION_LOCAL",  1),
        ("GLOBAL", "Global", "",                        "ORIENTATION_GLOBAL", 2),
    ]

    cutRotation : EnumProperty (
        items       = cutRotation_List,
        name        = "Cut Rotation",
        description = "The rotation of the cut should",
        default     = "LOCAL"
    )

    fillAfterCut_List = [
        ("UNSET",   "Unset", "Use Last Known Settings", "", 0),
        ("FILL",    "Yes",   "",                        "", 1),
        ("NO_FILL", "No",    "",                        "", 2),
    ]

    fillAfterCut : EnumProperty (
        items       = fillAfterCut_List,
        name        = "Fill",
        description = "Fill the empty hole with an NGON after performing a cut",
        default     = "NO_FILL"
    )

    keepMirrorModifier_List = [
        ("UNSET", "Unset", "Use Last Known Settings", "", 0),
        ("NO",    "No",    "",                        "", 1),
        ("YES",   "Yes",   "",                        "", 2),
    ]

    keepMirrorModifier : EnumProperty (
        items       = keepMirrorModifier_List,
        name        = "Keep Mirror Modifier",
        description = "Preserves the mirror modifier when complete",
        default     = "NO"
    )

#END NTZSYM_ignitproperties()