# Update "Tab Category Name" inspired by "Meta-Androcto's" "Edit Mesh Tools" Add-on
# recommended by "cytoo"

import bpy
from . panels           import NTZSYM_PT_ntzsym
from . miscFunc         import load_handler
from . miscFunc         import unload_handler

from bpy.props          import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types          import (Panel, Operator, AddonPreferences, PropertyGroup)

# Define Panel classes for updating
panels = (
        NTZSYM_PT_ntzsym,
        )

        

def update_panel(self, context):

    sidebarPanelSize_PropVal        = context.preferences.addons[__package__].preferences.sidebarPanelSize
    category_PropVal                = context.preferences.addons[__package__].preferences.category
    popupAndPiePanelSize_PropVal    = context.preferences.addons[__package__].preferences.popupAndPiePanelSize

    message = "Neltulz QuickSubD: Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        #Whatever the user typed into the text box in the add-ons settings, set that as the addon's tab category name
        for panel in panels:
            
            if sidebarPanelSize_PropVal == "HIDE":
                panel.bl_category = ""
                panel.bl_region_type = "WINDOW"

            else:
                if self.sidebarPanelSize == "DEFAULT":
                    panel.bUseCompactSidebarPanel = False
                else:
                    panel.bUseCompactSidebarPanel = True

                panel.bl_category = category_PropVal
                panel.bl_region_type = "UI"

            if self.popupAndPiePanelSize == "DEFAULT":
                panel.bUseCompactPopupAndPiePanel = False
            else:
                panel.bUseCompactPopupAndPiePanel = True

            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__package__, message, e))
        pass

def addRemoveUndoHandler(self, context):
    if context.preferences.addons[__package__].preferences.rememberOrientAndLocOnUndo:
        load_handler()
    else:
        unload_handler()

class NTZSYM_OT_addonprefs(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    category: StringProperty(
        name="Tab Category",
        description="Choose a name for the category of the panel",
        default="Neltulz",
        update=update_panel,
    )
        
    sidebarpanelSize_List = [
        ("DEFAULT", "Default", "", "", 0),
        ("COMPACT", "Compact", "", "", 1),
        ("HIDE",    "Hide",    "", "", 2),
    ]

    popupAndPiePanelSize_List = [
        ("DEFAULT", "Default", "", "", 0),
        ("COMPACT", "Compact", "", "", 1),
    ]

    sidebarPanelSize : EnumProperty (
        items       = sidebarpanelSize_List,
        name        = "Sidebar Panel Size",
        description = "Sidebar Panel Size",
        default     = "DEFAULT",
        update=update_panel,
    )

    popupAndPiePanelSize : EnumProperty (
        items       = popupAndPiePanelSize_List,
        name        = "Popup & Pie Panel Size",
        description = "Popup & Pie Panel Size",
        default     = "COMPACT",
        update=update_panel,
    )

    rememberOrientAndLocOnUndo : BoolProperty (
        name="Remember Orientation & Transform Pivot Point on Undo",
        description = "Whenever you perform an undo, sometimes blender will change your Orientation and Location , which can be annoying when you're trying to change pivot transform location and orientation before performing symmetry on a mesh object",
        default = True,
        update = addRemoveUndoHandler,
    )

    def draw(self, context):

        from . miscLay import createProp
        layout = self.layout

        scale_y = 1.25
        labelScale = 7
        propScale = 15
        propAlignment = "LEFT"
        propAlign = True
        labelJustify = "RIGHT"

        if self.sidebarPanelSize == "HIDE":
            bTabCatEnabled = False
        else:
            bTabCatEnabled = True

        #createProp(self, context, scn,  bEnabled,          bActive, bUseCol,  labelText,                                       data,    checkboxProp,       propItem,                      scale_y, labelScale, propScale, labelAlign,   propAlignment, propAlign,   propText, bExpandProp, propColCount, bUseSlider, resetProp, layout )
        createProp( self, context, None, True,              True,    False,    "Sidebar Panel",                                 self,    None,               "sidebarPanelSize",            scale_y, labelScale, propScale, labelJustify, propAlignment, propAlign,   None,     True,        1,            False,      None,      layout )
        createProp( self, context, None, bTabCatEnabled,    True,    False,    "Tab Category",                                  self,    None,               "category",                    scale_y, labelScale, propScale, labelJustify, propAlignment, propAlign,   "",       True,        1,            False,      None,      layout )
        createProp( self, context, None, True,              True,    False,    "Popup & Pie Panel",                             self,    None,               "popupAndPiePanelSize",        scale_y, labelScale, propScale, labelJustify, propAlignment, propAlign,   None,     True,        1,            False,      None,      layout )
        

        createProp( self, context, None, True,              True,    False,     "",                                             self,    None,               "rememberOrientAndLocOnUndo",  1,       labelScale, 30,        labelJustify, "EXPAND",      propAlign,   None,     True,        1,            False,      None,      layout )