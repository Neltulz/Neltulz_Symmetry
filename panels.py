import bpy
from . icons        import i as icons
from .              import misc_ot
from .              import miscLay
from .              import miscFunc

from bpy.props      import (StringProperty, BoolProperty, IntProperty, FloatProperty, FloatVectorProperty, EnumProperty, PointerProperty)
from bpy.types      import (Panel, Operator, AddonPreferences, PropertyGroup)

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

        #determine if panel is inside of a popop/pie menu
        panelInsidePopupOrPie = context.region.type == 'WINDOW'

        miscLay.createPanelOptionsSection(self, context, scn, lay, panelInsidePopupOrPie=panelInsidePopupOrPie)

    #END draw()

class NTZSYM_PT_optionscompactpopover(Panel):
    bl_idname = "NTZSYM_PT_optionscompactpopover"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Options"

    def draw(self, context):
        scn = context.scene
        lay = self.layout

        miscLay.createPanelOptionsSection(self, context, scn, lay, panelInsidePopupOrPie=True)

    #END draw()




class NTZSYM_PT_ntzsym(Panel):

    bl_idname = "ntz_sym.panel"
    bl_label = "Symmetry v1.0.1"
    bl_category = "Neltulz"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bUseCompactSidebarPanel = BoolProperty(
        name="Use Compact Panel",
        description="Use Compact Panel",
        default = False
    )

    bUseCompactPopupAndPiePanel = BoolProperty(
        name="Use Compact Popup & Pie Panel",
        description="Use Compact Popup & Pie Panel",
        default = True
    )

    def draw(self, context):

        scn = context.scene
        lay = self.layout.column(align=True)

        modeAtBegin = "OBJECT" #declare
        try:    modeAtBegin = bpy.context.object.mode
        except: pass

        selObjs = set(context.selected_objects)
        activeObj = context.view_layer.objects.active

        if modeAtBegin == "EDIT":
            editModeObjs = set(bpy.context.objects_in_mode)

            #combine selObjs and editModeObjs (useful for applying/removing modifiers in edit mode)
            selObjs = selObjs.union(editModeObjs)
        
        #determine if panel is inside of a popop/pie menu
        panelInsidePopupOrPie = context.region.type == 'WINDOW'

        if panelInsidePopupOrPie:

            if self.bUseCompactPopupAndPiePanel:
                lay.ui_units_x = 8
                lay.label(text="Symmetry")

            else:
                lay.ui_units_x = 13
                lay.label(text="Neltulz - Symmetry")


        compactPanelConditions = (panelInsidePopupOrPie and self.bUseCompactPopupAndPiePanel) or (not panelInsidePopupOrPie and self.bUseCompactSidebarPanel)

        if not compactPanelConditions:
            sepFactor = 1
            labelWidth = 2.75
        else:
            sepFactor = 0.25
            labelWidth = 1.75
        
        def opProperties(op, symType, axis, axisDir=None):
            op.symType = symType

            if not scn.ntzSym.cutLocation in ["UNSET"]: op.cutLocation = scn.ntzSym.cutLocation
            if not scn.ntzSym.cutRotation in ["UNSET"]: op.cutRotation = scn.ntzSym.cutRotation

            if scn.ntzSym.fillAfterCut == "FILL": op.use_fill = True
            else:                                 op.use_fill = False

            if scn.ntzSym.keepModifiers == "YES": op.keepModifiers = True
            else:                                 op.keepModifiers = False

            op.axis = axis

            if axisDir is not None:
                op.axisDir = axisDir

        emboss=False

        if not compactPanelConditions: labelHeight = 1.35
        else:                          labelHeight = 1

        # -----------------------------------------------------------------------------
        #   SLICE
        # ----------------------------------------------------------------------------- 
        sliceRow = lay.row(align=True)  

        sliceRowLabel = sliceRow.row(align=True)
        sliceRowLabel.alignment="RIGHT"
        sliceRowLabel.ui_units_x = labelWidth
        sliceRowLabel.scale_y = labelHeight
       
        if not compactPanelConditions:  sliceRowLabel.label(text="Slice:")
        else:                           sliceRowLabel.label(text="Slc:")
        
        if not compactPanelConditions:
            sliceRow = sliceRow.box()

        sliceRowButtons = sliceRow.grid_flow(align=True, columns=3, even_columns=True, even_rows=True)
        sliceRowButtons.scale_y = 1

        # X (Slice)
        #------------------------------------------------------------------------------------------------------
        
        opRow = sliceRowButtons.grid_flow(align=True)
        op = opRow.operator('ntz_sym.performsym', text='', icon_value=icons['xIcon'], emboss=emboss)
        opProperties(op, "SLICE", "X")
        op.tooltip = "Slice along the X axis"



        # Y (Slice)
        #------------------------------------------------------------------------------------------------------
        
        opRow = sliceRowButtons.grid_flow(align=True)
        op = opRow.operator('ntz_sym.performsym', text='', icon_value=icons['yIcon'], emboss=emboss)
        opProperties(op, "SLICE", "Y")
        op.tooltip = "Slice along the Y axis"



        # Z (Slice)
        #------------------------------------------------------------------------------------------------------
        
        opRow = sliceRowButtons.grid_flow(align=True)
        op = opRow.operator('ntz_sym.performsym', text='', icon_value=icons['zIcon'], emboss=emboss)
        opProperties(op, "SLICE", "Z")
        op.tooltip = "Slice along the Z axis"




        lay.separator(factor=sepFactor)



        # -----------------------------------------------------------------------------
        #   CUT
        # ----------------------------------------------------------------------------- 
        cutRow = lay.row(align=True)

        cutRowLabel = cutRow.row(align=True)
        cutRowLabel.alignment="RIGHT"
        cutRowLabel.ui_units_x = labelWidth
        cutRowLabel.scale_y = labelHeight
        cutRowLabel.label(text="Cut:")

        if not compactPanelConditions:
            cutRow = cutRow.box()

        cutRowButtons = cutRow.grid_flow(align=True, columns=3, even_columns=True, even_rows=True)
        cutRowButtons.scale_y = 1

        # X (Cut)
        #------------------------------------------------------------------------------------------------------
        

        xColRow = cutRowButtons.grid_flow(align=True, columns=2, even_columns=True)

        op = xColRow.operator('ntz_sym.performsym', text='', icon_value=icons['xIconLeft'], emboss=emboss)
        opProperties(op, "CUT", "X", axisDir="BACKWARD")
        op.tooltip = "Cut backward along the X axis"


        op = xColRow.operator('ntz_sym.performsym', text='', icon_value=icons['xIconRight'], emboss=emboss)
        opProperties(op, "CUT", "X", axisDir="FORWARD")
        op.tooltip = "Cut forward along the X axis"


        # Y (Cut)
        #------------------------------------------------------------------------------------------------------

        yColRow = cutRowButtons.grid_flow(align=True, columns=2, even_columns=True)

        op = yColRow.operator('ntz_sym.performsym', text='', icon_value=icons['yIconLeft'], emboss=emboss)
        opProperties(op, "CUT", "Y", axisDir="BACKWARD")
        op.tooltip = "Cut backward along the Y axis"

        op = yColRow.operator('ntz_sym.performsym', text='', icon_value=icons['yIconRight'], emboss=emboss)
        opProperties(op, "CUT", "Y", axisDir="FORWARD")
        op.tooltip = "Cut forward along the Y axis"

        # Z (Cut)
        #------------------------------------------------------------------------------------------------------

        zColRow = cutRowButtons.grid_flow(align=True, columns=2, even_columns=True)

        op = zColRow.operator('ntz_sym.performsym', text='', icon_value=icons['zIconLeft'], emboss=emboss)
        opProperties(op, "CUT", "Z", axisDir="BACKWARD")
        op.tooltip = "Cut backward along the Z axis"


        op = zColRow.operator('ntz_sym.performsym', text='', icon_value=icons['zIconRight'], emboss=emboss)
        opProperties(op, "CUT", "Z", axisDir="FORWARD")
        op.tooltip = "Cut forward along the Z axis"

        lay.separator(factor=sepFactor)




        # -----------------------------------------------------------------------------
        #   MIRROR
        # ----------------------------------------------------------------------------- 
        mirrorRow = lay.row(align=True)

        mirrorRowLabel = mirrorRow.row(align=True)
        mirrorRowLabel.alignment = "RIGHT"
        mirrorRowLabel.ui_units_x = labelWidth
        mirrorRowLabel.scale_y = labelHeight

        if not compactPanelConditions:  mirrorRowLabel.label(text="Mirror:")
        else:                           mirrorRowLabel.label(text="Mir:")

        if not compactPanelConditions:
            mirrorRow = mirrorRow.box()

        mirrorRowButtons = mirrorRow.grid_flow(align=True, columns=3, even_columns=True, even_rows=True)
        mirrorRowButtons.scale_y = 1

        # X (Mirror)
        #------------------------------------------------------------------------------------------------------
        xColRow = mirrorRowButtons.grid_flow(align=True, columns=2, even_columns=True)

        op = xColRow.operator('ntz_sym.performsym', text='', icon_value=icons['xIconLeft'], emboss=emboss)
        opProperties(op, "MIRROR", "X", axisDir="BACKWARD")
        op.tooltip = "Mirror backward along the X axis.  CTRL+Click to keep mirror modifier"


        op = xColRow.operator('ntz_sym.performsym', text='', icon_value=icons['xIconRight'], emboss=emboss)
        opProperties(op, "MIRROR", "X", axisDir="FORWARD")
        op.tooltip = "Mirror forward along the X axis.  CTRL+Click to keep mirror modifier"


        # Y (Mirror)
        #------------------------------------------------------------------------------------------------------
        yColRow = mirrorRowButtons.grid_flow(align=True, columns=2, even_columns=True)

        op = yColRow.operator('ntz_sym.performsym', text='', icon_value=icons['yIconLeft'], emboss=emboss)
        opProperties(op, "MIRROR", "Y", axisDir="BACKWARD")
        op.tooltip = "Mirror backward along the Y axis.  CTRL+Click to keep mirror modifier"


        op = yColRow.operator('ntz_sym.performsym', text='', icon_value=icons['yIconRight'], emboss=emboss)
        opProperties(op, "MIRROR", "Y", axisDir="FORWARD")
        op.tooltip = "Mirror forward along the Y axis.  CTRL+Click to keep mirror modifier"

        # Z (Mirror)
        #------------------------------------------------------------------------------------------------------
        zColRow = mirrorRowButtons.grid_flow(align=True, columns=2, even_columns=True)

        op = zColRow.operator('ntz_sym.performsym', text='', icon_value=icons['zIconLeft'], emboss=emboss)
        opProperties(op, "MIRROR", "Z", axisDir="BACKWARD")
        op.tooltip = "Mirror backward along the Z axis.  CTRL+Click to keep mirror modifier"


        op = zColRow.operator('ntz_sym.performsym', text='', icon_value=icons['zIconRight'], emboss=emboss)
        opProperties(op, "MIRROR", "Z", axisDir="FORWARD")
        op.tooltip = "Mirror forward along the Z axis.  CTRL+Click to keep mirror modifier"

        # -----------------------------------------------------------------------------
        #   APPLY / REMOVE Mirror Modifiers
        # ----------------------------------------------------------------------------- 

        
        foundMirrorModifier = False #declare
        for obj in selObjs:
            if not foundMirrorModifier:
                
                #check if mirrorParent exists on empty or bisectPlane
                mirrorParent = getattr(obj, "mirrorParent", None)

                if mirrorParent is not None:
                    foundMirrorModifier = True
                    break
                
                #check if object has a mirror modifier
                if miscFunc.findModifier(obj=obj, modifierType='MIRROR') is not None:
                    foundMirrorModifier = True
                    break


        if foundMirrorModifier:
            
            lay.separator(factor=sepFactor)

            row = lay.row(align=True)

            op = row.operator('ntz_sym.applyorremovemodifier', text='Apply', icon="CHECKMARK")
            op.method = "APPLY"
            op.tooltip = "Apply any mirror and bisect (boolean) modifiers from the selected objects.  CTRL+Click to keep Empties & Bisect Planes"

            op = row.operator('ntz_sym.applyorremovemodifier', text='Remove', icon="X")
            op.method = "REMOVE"
            op.tooltip = "Removes any mirror and bisect (boolean) modifiers from the selected objects.  CTRL+Click to keep Empties & Bisect Planes"

        # -----------------------------------------------------------------------------
        #   OPTIONS
        # ----------------------------------------------------------------------------- 

        lay.separator(factor=sepFactor)

        optionsSection = lay.column(align=True)

        if panelInsidePopupOrPie:
            
            popoverRow = optionsSection.row(align=True)
            popoverRow.scale_x = 1.2
            popoverRow.alignment = "RIGHT"

            if self.bUseCompactPopupAndPiePanel:
                iconOnly = True
            else:
                iconOnly = False

            popover = popoverRow.prop_with_popover(
                scn.ntzSym,
                "optionsPopoverEnum",
                text="",
                icon="SETTINGS",
                icon_only=iconOnly,
                panel="NTZSYM_PT_options",
            )

        elif (not panelInsidePopupOrPie and self.bUseCompactSidebarPanel):
            
            popoverRow = optionsSection.row(align=True)
            popoverRow.scale_x = 1.2
            popoverRow.alignment = "CENTER"
            popover = popoverRow.prop_with_popover(
                scn.ntzSym,
                "optionsPopoverEnum",
                text="",
                icon="SETTINGS",
                icon_only=False,
                panel="NTZSYM_PT_optionscompactpopover",
            )

        else:


            #create show/hide toggle for options section
            miscLay.createShowHide(self, context, scn, "ntzSym", "bShowOptions", None, "Options", optionsSection)

            optionsSection.separator()

            if scn.ntzSym.bShowOptions:

                miscLay.createPanelOptionsSection(self, context, scn, lay, panelInsidePopupOrPie=panelInsidePopupOrPie)



    #END draw()