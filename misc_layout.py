import bpy

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


def createSymmetryOperators(scn, symType, lay):

    if symType in ["CUT", "MIRROR"]:
        xyzList = ["X -", "Y -", "Z -", "X +", "Y +", "Z +"]
    else:
        xyzList = ["X", "Y", "Z"]

    labelText = "Cut" #declare

    if symType == "SLICE":
        labelText = "Slice:"

    elif symType == "CUT":
        labelText = "Cut:"

    elif symType == "MIRROR":
        labelText = "Mirror:"

    labelWidth = 3

    section = lay.row(align=True)
    
    
    labelCol = section.column(align=True)
    labelCol.alignment="RIGHT"
    labelCol.ui_units_x = labelWidth
    
    labelCol.label(text=labelText, icon="NONE")

    if symType == "SLICE":           labelCol.scale_y = 1
    if symType in ["CUT", "MIRROR"]: labelCol.scale_y = 1.75

    buttonRowWrapper = section.row(align=True)
    buttonRowWrapper.scale_y = 1
    
        
    xCol = buttonRowWrapper.column(align=True)

    if symType in ["CUT", "MIRROR"]:

        buttonRowWrapper.separator()
        buttonRowWrapper.separator()

    yCol = buttonRowWrapper.column(align=True)

    if symType in ["CUT", "MIRROR"]:
        buttonRowWrapper.separator()
        buttonRowWrapper.separator()

    zCol = buttonRowWrapper.column(align=True)

    if symType in ["CUT", "MIRROR"]:
        labelHeight = 0.4

        xColLabelBox = xCol.box()
        xColLabelBox.scale_y = labelHeight
        xColLabel = xColLabelBox.label(text="X")

        yColLabelBox = yCol.box()
        yColLabelBox.scale_y = labelHeight
        yColLabel = yColLabelBox.label(text="Y")

        zColLabelBox = zCol.box()
        zColLabelBox.scale_y = labelHeight
        zColLabel = zColLabelBox.label(text="Z")

    xColButtonWrapper = xCol.row(align=True)
    yColButtonWrapper = yCol.row(align=True)
    zColButtonWrapper = zCol.row(align=True)

    

    buttonGrid = buttonRowWrapper.grid_flow(row_major=True, columns=3, even_columns=False, even_rows=False, align=True)

    for item in xyzList:

        axisDir = "MINUS" #declare

        opText = " " #declare
        plusOrMinusSign = " " #declare
        
        if item in ["X -", "Y -", "Z -"]:
            axisDir = "MINUS"
            plusOrMinusSign = "-"
        elif item in ["X +", "Y +", "Z +"]:
            axisDir = "PLUS"
            plusOrMinusSign = "+"

        axis = "X" #declare

        if item in ["X", "X -", "X +"]:
            buttonCol = xColButtonWrapper
            axis = "X"

        elif item in ["Y", "Y -", "Y +"]:
            buttonCol = yColButtonWrapper
            axis = "Y"

        elif item in ["Z", "Z -", "Z +"]:
            buttonCol = zColButtonWrapper
            axis = "Z"

        if symType == "SLICE":
            opText = axis

        elif symType in ["CUT", "MIRROR"]:
            opText = plusOrMinusSign
            


        op = buttonCol.operator('ntz_sym.performsym', text=opText)
        op.symType = symType

        if scn.ntzSym.cutLocation != "UNSET": op.cutLocation = scn.ntzSym.cutLocation
        if scn.ntzSym.cutRotation != "UNSET": op.cutRotation = scn.ntzSym.cutRotation

        if scn.ntzSym.fillAfterCut == "FILL": op.use_fill = True
        else:                                 op.use_fill = False

        if scn.ntzSym.keepMirrorModifier == "YES": op.keepMirrorModifier = True
        else:                                      op.keepMirrorModifier = False

        op.axis = axis
        op.axisDir = axisDir

def createProp(self, context, scn, properties, propItem, labelText, labelWidth, scale_y, bExpandProp, layout):

    if properties is not None:
        data = eval(f"scn.{properties}")
    else:
        data = self

    propRow = layout.row(align=True)
    propRow.scale_y = scale_y

    propRowLabel = propRow.column(align=True)
    propRowLabel.alignment="RIGHT"
    propRowLabel.ui_units_x = labelWidth
    propRowLabel.label(text=labelText)

    propRowItem = propRow.column(align=True)
    propRowItem.alignment="EXPAND"
    propRowItem.scale_x = 1
    propRowItem.prop(data, propItem, text="", expand=bExpandProp)

def createPanelOptionsSection(self, context, scn, lay):

    optionsSectionRow = lay.row(align=True)

    spacer = optionsSectionRow.column(align=True)
    spacer.label(text="", icon="BLANK1")

    optionsSectionCol = optionsSectionRow.column(align=True)

    labelWidth = 4

    createProp(self, context, scn, "ntzSym", "cutLocation", "Cut Location", labelWidth, 1, False, optionsSectionCol)
    
    optionsSectionCol.separator()

    createProp(self, context, scn, "ntzSym", "cutRotation", "Cut Rotation", labelWidth, 1, False, optionsSectionCol)
    
    optionsSectionCol.separator()

    createProp(self, context, scn, "ntzSym", "fillAfterCut", "Fill Cut", labelWidth, 1, False, optionsSectionCol)
    
    optionsSectionCol.separator()

    createProp(self, context, scn, "ntzSym", "keepMirrorModifier", "Keep Mirror Modifier", labelWidth, 1, False, optionsSectionCol)

    resetOP = lay.operator('ntz_sym.resetallsettings', text="Reset all Settings")