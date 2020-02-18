import bpy

from . import icons

#Show hide section with arrow, optional checkbox, and text
def createShowHide(self, context, scene, properties, showHideBool, optionalCheckboxBool, text, layout):

    if scene is not None:
        data = eval( f"scene.{properties}" )
        boolThing = eval( f"scene.{properties}.{showHideBool}" )
    else:
        data = self
        boolThing = eval( f"self.{showHideBool}")

    if boolThing:
        showHideIcon = "TRIA_DOWN"
    else:
        showHideIcon = "TRIA_RIGHT"

    row = layout.row(align=True)

    downArrow = row.column(align=True)
    downArrow.alignment = "LEFT"
    downArrow.prop(data, showHideBool, text="", icon=showHideIcon, emboss=False )

    if optionalCheckboxBool is not None:
        checkbox = row.column(align=True)
        checkbox.alignment = "LEFT"
        checkbox.prop(data, optionalCheckboxBool, text="" )

    textRow = row.column(align=True)
    textRow.alignment = "LEFT"
    textRow.prop(data, showHideBool, text=text, emboss=False )

    emptySpace = row.column(align=True)
    emptySpace.alignment = "EXPAND"
    emptySpace.prop(data, showHideBool, text=" ", emboss=False)




def createProp(self, context, scn, bEnabled, bActive, bUseCol, labelText, data, checkboxProp, propItem, scale_y, labelScale, propScale, labelAlign, propAlignment, propAlign, propText, bExpandProp, propColCount, bUseSlider, resetProp, layout):

    if bUseCol:
        propSection = layout.column(align=True)
    else:
        propSection = layout.row(align=True)

    propSection.scale_y = scale_y

    propSectionLabel = propSection.row(align=True)
    propSectionLabel.alignment="EXPAND"
    propSectionLabel.ui_units_x = labelScale

    if checkboxProp is not None:
        checkbox = propSection.row(align=True)
        checkbox.prop(self, checkboxProp, text='')

        propSection.separator()

    propSectionLabel1 = propSectionLabel.row(align=True)
    propSectionLabel1.alignment=labelAlign
    propSectionLabel1.scale_x = 1
    propSectionLabel1.enabled = bEnabled
    propSectionLabel1.active = bActive


    propSectionLabel1.label(text=labelText)

    propSectionItem = propSection.row(align=True)

    propSectionItem.enabled = bEnabled
    propSectionItem.active = bActive

    propSectionItem.alignment=propAlignment
    
    if (propColCount <= 1) or (not bExpandProp):
        propSectionItem1 = propSectionItem.row(align=propAlign)
    else:
        propSectionItem1 = propSectionItem.column_flow(columns=propColCount, align=propAlign)

    if resetProp is not None:
        propSection.separator()
        resetBtn = propSection.row(align=True)
        resetBtn.active = False
        resetBtn.prop(self, resetProp, icon="LOOP_BACK", toggle=True, emboss=False, icon_only=True)

    propSectionItem1.alignment=propAlignment
    propSectionItem1.ui_units_x = propScale
    propSectionItem1.scale_x = 100

    propSectionItem1.prop(data, propItem, text=propText, expand=bExpandProp, slider=bUseSlider)

def createPanelOptionsSection(self, context, scn, lay, panelInsidePopupOrPie=False):

    if panelInsidePopupOrPie:
        optionsSectionRow = lay

    else:
        optionsSectionRow = lay.row(align=True)

        spacer = optionsSectionRow.column(align=True)
        spacer.label(text="", icon="BLANK1")

    optionsSectionCol = optionsSectionRow.column(align=True)

    scale_y = 1
    labelScale = 4.6
    propScale = 5
    labelAlign = "RIGHT"
    propAlignment = "EXPAND"
    propAlign = True
    propText = ""

    #createProp(self, context, scn,  bEnabled,   bActive, bUseCol,       labelText,              data,        checkboxProp,       propItem,                      scale_y, labelScale, propScale, labelAlign,   propAlignment, propAlign,   propText, bExpandProp, propColCount, bUseSlider, resetProp, layout            )
    createProp( self, context, scn,  True,       True,    False,         "Location",             scn.ntzSym,  None,               "cutLocation",                 scale_y, 3,          propScale, labelAlign,   propAlignment, propAlign,   propText, False,       1,            False,      None,      optionsSectionCol )
    optionsSectionCol.separator()
    createProp( self, context, scn,  True,       True,    False,         "Rotation",             scn.ntzSym,  None,               "cutRotation",                 scale_y, 3,          propScale, labelAlign,   propAlignment, propAlign,   propText, False,       1,            False,      None,      optionsSectionCol )
    
    optionsSectionCol.separator(factor=2)

    cutOptionsSection = optionsSectionCol.column(align=True)
    label = cutOptionsSection.row(align=True)
    label.label(text="Cut", icon="MOD_BOOLEAN")
    
    optionsSectionCol.separator()

    cutOptionsSection = optionsSectionCol.box().column(align=True)

    createProp( self, context, scn,  True,       True,    False,         "Fill Cut",             scn.ntzSym,  None,               "fillAfterCut",                scale_y, labelScale, propScale, labelAlign,   propAlignment, propAlign,   propText, False,       1,            False,      None,      cutOptionsSection )
    
    optionsSectionCol.separator(factor=2)
    

    mirrorOptionsSection = optionsSectionCol.row(align=True)
    label = mirrorOptionsSection.row(align=True)
    optionsSectionCol.separator()
    label.label(text="Mirror", icon="MOD_MIRROR")
    
    mirrorOptionsSection = optionsSectionCol.box().column(align=True)
    
    createProp( self, context, scn,  True,       True,    False,         "Keep Modifiers",       scn.ntzSym,  None,               "keepModifiers",               scale_y, 5, propScale, labelAlign,   propAlignment, propAlign,   propText, False,       1,            False,      None,      mirrorOptionsSection )
    
    optionsSectionCol.separator(factor=2)

    opOptionsSection = optionsSectionCol.row(align=True)
    label = opOptionsSection.row(align=True)
    label.label(text="Operator", icon="PROPERTIES")

    optionsSectionCol.separator()

    opOptionsSection = optionsSectionCol.box().column(align=True)

    createProp( self, context, scn,  True,       True,    False,         "OP Options",           scn.ntzSym,  None,               "defaultOperatorShowOptions",  scale_y, labelScale, propScale, labelAlign,   propAlignment, propAlign,   propText, False,       1,            False,      None,      opOptionsSection )
    
    optionsSectionCol.separator(factor=2)

    applyRemoveSection = optionsSectionCol.row(align=True)
    label = applyRemoveSection.row(align=True)

    optionsSectionCol.separator()
    label.label(text="Applying & Removing", icon="TRASH")

    applyRemoveSection = optionsSectionCol.box().column(align=True)
    
    createProp( self, context, scn,  True,       True,    False,         "Del Empties",           scn.ntzSym,  None,              "removeEmpties",               scale_y, labelScale, propScale, labelAlign,   propAlignment, propAlign,   propText, False,       1,            False,      None,      applyRemoveSection )
    applyRemoveSection.separator()
    createProp( self, context, scn,  True,       True,    False,         "Del Bisect",            scn.ntzSym,  None,              "removeBisectPlanes",          scale_y, labelScale, propScale, labelAlign,   propAlignment, propAlign,   propText, False,       1,            False,      None,      applyRemoveSection )

    optionsSectionCol.separator(factor=2)

    resetOP = optionsSectionCol.operator('ntz_sym.resetallsettings', text="Reset all Settings", icon="LOOP_BACK")