import bpy
from . import misc_ot
from . import misc_layout

from bpy.props import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types import (Panel, Operator, AddonPreferences, PropertyGroup)

# -----------------------------------------------------------------------------
#   Panel
# ----------------------------------------------------------------------------- 

class NTZSYM_PT_options(Panel):
    bl_idname = "NTZSYM_PT_options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Options"

    def draw(self, context):
        scn = context.scene
        lay = self.layout

        misc_layout.createPanelOptionsSection(self, context, scn, lay)

    #END draw()

class NTZSYM_PT_ntzsym(Panel):

    bl_idname = "ntz_sym.panel"
    bl_label = "Symmetry v1.0.0"
    bl_category = "Neltulz"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        

        scn = context.scene
        lay = self.layout

        #determine if panel is inside of a popop/pie menu
        panelInsidePopupOrPie = context.region.type == 'WINDOW'

        if panelInsidePopupOrPie:
            lay.ui_units_x = 13
            lay.label(text="Neltulz - Symmetry v1.0.0")
            lay.separator()

        misc_layout.createSymmetryOperators(scn, "SLICE", lay)

        sepRow = lay.row(align=True)
        sepRow.label(text=" ")
        
        if panelInsidePopupOrPie: sepRow.ui_units_y = 0.25
        else:                     sepRow.ui_units_y = 0.01

        misc_layout.createSymmetryOperators(scn, "CUT", lay)

        sepRow = lay.row(align=True)
        sepRow.label(text=" ")
        
        if panelInsidePopupOrPie: sepRow.ui_units_y = 0.25
        else:                     sepRow.ui_units_y = 0.01

        misc_layout.createSymmetryOperators(scn, "MIRROR", lay)


        optionsSection = lay.column(align=True)

        if not panelInsidePopupOrPie:

            #create show/hide toggle for options section
            misc_layout.createShowHide(self, context, scn, "ntzSym", "bShowOptions", None, "Options", optionsSection)

            if scn.ntzSym.bShowOptions:

                misc_layout.createPanelOptionsSection(self, context, scn, lay)
        
        else:

            optionsSection.separator()

            popover = optionsSection.prop_with_popover(
                scn.ntzSym,
                "optionsPopoverEnum",
                text="",
                icon="NONE",
                icon_only=False,
                panel="NTZSYM_PT_options",
            )





    #END draw()