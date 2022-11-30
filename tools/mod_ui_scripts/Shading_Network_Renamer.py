import maya.cmds as cmd
# ShadingEngine textfield value
sgQname = None

# Grab the values inside the text field
def textFieldSgQ(*args):
    global sgQname
    sgQname = cmd.textField(chNameFieldSg, q=True, text=True)
    return sgQname


# Renamer function
def sgRenamer(*args):
    # select object then the shape
    sel = cmd.ls(sl=True)
    objectName = sel[0]
    # list the shading group
    selShape = cmd.listRelatives(shapes=1)
    selSG = cmd.listConnections(selShape, type='shadingEngine')
    cmd.select(clear=True)

    # list connections
    sgCnt = cmd.hyperShade(lun=selSG[0], noShapes=True, noTransforms=True)
    # List all shading engine's nodes
    utilitySet = cmd.listNodeTypes('utility')
    shaderSet = cmd.listNodeTypes('shader')
    textureSet = cmd.listNodeTypes('texture')
    textureSuffix = txtQname
    shaderSuffix = shdQname
    utilitySuffix = utlQname

    if cmd.checkBox(checkBoxCmd, q=True, v=True) == True:

        # rename the shading group
        cmd.rename(selSG, objectName + '_SG')

        for i in list(sgCnt):
            if cmd.nodeType(i) in textureSet:
                cmd.rename(i, objectName + '_' + cmd.nodeType(i) + '_TXT')
            elif cmd.nodeType(i) in shaderSet:
                cmd.rename(i, objectName + '_SHD')
            elif cmd.nodeType(i) in utilitySet:
                cmd.rename(i, objectName + '_' + cmd.nodeType(i) + '_UTL')

    elif cmd.checkBox(checkBoxCmd, q=True, v=True) == False:

        # rename the shading group
        cmd.rename(selSG, objectName + '_' + str(sgQname))
        for i in list(sgCnt):
            if cmd.nodeType(i) in textureSet:
                cmd.rename(i, objectName + '_' + cmd.nodeType(i) + '_' + str(textureSuffix))
            elif cmd.nodeType(i) in shaderSet:
                cmd.rename(i, objectName + '_' + str(shaderSuffix))
            elif cmd.nodeType(i) in utilitySet:
                cmd.rename(i, objectName + '_' + cmd.nodeType(i) + '_' + str(utilitySuffix))

            # UI


utlQname = None
shdQname = None
txtQname = None


def textFieldUtlQ(*args):
    global utlQname
    utlQname = cmd.textField(chNameFieldUtl, q=True, text=True)
    return utlQname


def textFieldShdQ(*args):
    global shdQname
    shdQname = cmd.textField(chNameFieldShd, q=True, text=True)
    return shdQname


def textFieldTxtQ(*args):
    global txtQname
    txtQname = cmd.textField(chNameFieldTxt, q=True, text=True)
    return txtQname


def mainui():
    global chNameFieldUtl, chNameFieldShd, chNameFieldTxt, chNameFieldSg, checkBoxCmd
    windowID = 'RenamerWindow'
    if cmd.window(windowID, exists=True):
        cmd.deleteUI(windowID)
    ui = cmd.window(windowID, title='Renamer', rtf=True)
    layoutW = cmd.columnLayout('Renamer', adj=True)
    cmd.separator(style='none')
    cmd.text('Utilities', p=layoutW)
    cmd.separator(style='none')
    chNameFieldUtl = cmd.textField(cc=textFieldUtlQ, ec=textFieldUtlQ, p=layoutW)
    cmd.separator(style='none')
    cmd.text('Shaders', p=layoutW)
    cmd.separator(style='none')
    chNameFieldShd = cmd.textField(cc=textFieldShdQ, ec=textFieldShdQ, p=layoutW)
    cmd.separator(style='none')
    cmd.text('Textures', p=layoutW)
    cmd.separator(style='none')
    chNameFieldTxt = cmd.textField(cc=textFieldTxtQ, ec=textFieldTxtQ, p=layoutW)
    cmd.separator(style='none')
    cmd.text('ShadingEngines', p=layoutW)
    cmd.separator(style='none')
    chNameFieldSg = cmd.textField(cc=textFieldSgQ, ec=textFieldSgQ, p=layoutW)
    cmd.separator(style='none')
    cmd.button(label='Rename', width=200, height=25, command=sgRenamer, p=layoutW)
    cmd.separator(style='none')
    checkBoxCmd = cmd.checkBox(label='Use default prefix', p=layoutW)
    cmd.separator(style='none')
    cmd.showWindow(ui)



# -----------------------------------------------------------#
