import maya
import maya.cmds as cmds
import pymel.core as pm
from pymel.all import *
import os
import inspect
import __main__
import mod_ui_scripts.UVTransfer as uvTrans
import mod_ui_scripts.Shading_Network_Renamer as shdrename
import tools.mod_ui_scripts.showxml
# import tools.pub_ui

WINDOW_SIDE_TITLE = "Modelling Tools"
WINDOW_DISPLAY_TEXT = "TAV Tools Modelling Toolkit"

def windes():
    cmds.scrollLayout(w=240)
    cmds.columnLayout(w=220, co=("left",10))
    cmds.text(l="",h=10)
    cmds.text(label=WINDOW_DISPLAY_TEXT, align='center', font='boldLabelFont')
    cmds.text(l="",h=10)
    
    cmds.button(label = "Modeling CheckList", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/Assets_Publisher.mel\"; CheckListUi;')")
    # cmds.button(label = "Publishing Tool", width=200, bgc=(0.1,0.1,0.1), c=launchpubui)
    
    cmds.rowLayout(nc=4, width=200)
    cmds.button(label = "CP", width=49, bgc=(0.1,0.1,0.1), c="maya.cmds.xform(cpc=1)")
    cmds.button(label = "FT", width=49, bgc=(0.1,0.1,0.1), c="maya.cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)")
    cmds.button(label = "DH", width=49, bgc=(0.1,0.1,0.1), c="maya.mel.eval(\"DeleteHistory;\")")
    cmds.button(label = "NDH", width=49, bgc=(0.1,0.1,0.1), c="maya.mel.eval('doBakeNonDefHistory( 1, {\"prePost\"});')")
    cmds.setParent('..')
    
    cmds.rowLayout(nc=4, width=200)
    cmds.button(label = "All Geo", width=49, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"cpa\")"))
    cmds.button(label = "All Geo", width=49, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"fta\")"))
    cmds.button(label = "All Geo", width=49, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"dha\")"))
    cmds.button(label = "All Geo", width=49, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"ndha\")"))
    cmds.setParent('..')
    
    cmds.rowLayout(nc=4, width=200)
    cmds.button(label = "All Grp", width=49, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"cpaGrp\")"))
    cmds.button(label = "All Grp", width=49, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"ftaGrp\")"))
    cmds.button(label = "All Grp", width=49, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"dhaGrp\")"))
    cmds.button(label = "All Grp", width=49, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"ndhaGrp\")"))
    cmds.setParent('..')
    cmds.button(label = "CP,FT,DH,NDH ALL Geo Grp", width=200, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"cpftdhndh\")"))
    
    cmds.separator()
    
    cmds.frameLayout(label='Smooth Options', cll=1, cl=0, lv=1, w=200)
    cmds.columnLayout(w=200, adjustableColumn=1)
    cmds.button(label = "Set All Default Smooth", bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/Default_smooth.mel\"; set_smooth_default;')")
    cmds.button(label = "Select All Polysmooth mesh", bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/xtras.mel\"; slctsmthmsh;')")
    cmds.rowLayout(nc=3, width=200)
    cmds.text(label="Remove Polysmooth", font='tinyBoldLabelFont')
    cmds.button(label = "Selected", bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/xtras.mel\"; asDelSelPS;')")
    cmds.button(label = "All Mesh", bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/xtras.mel\"; asDelAllPS;')")
    cmds.setParent('..')
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.frameLayout(label='Face Selection', cll=1, cl=0, lv=1, w=200)
    cmds.rowLayout(nc=4, width=200)
    cmds.button(label = "Triangles", w=58, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/xtras.mel\"; polyselectcon(\"tri\");')")
    cmds.button(label = "Quads", w=58, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/xtras.mel\"; polyselectcon(\"qua\");')")
    cmds.button(label = "Nsided", w=58, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/xtras.mel\"; polyselectcon(\"nside\");')")
    cmds.symbolButton(ann = "Refresh all Selection", bgc=(0.1,0.1,0.1), w=18, h=18, image="refresh.png", c="maya.mel.eval('source \"mod_ui_scripts/xtras.mel\"; polyselectcon(\"refresh\");')")
    cmds.setParent('..')
    cmds.setParent('..')
    
    
    cmds.frameLayout(label='Mesh Tools', cll=1, cl=0, lv=1, w=200)
    cmds.columnLayout(w=200, adjustableColumn=1)
    cmds.rowLayout(nc=3, width=200)
    cmds.text(label="Set CVs \'0\'", w=69, font='tinyBoldLabelFont')
    cmds.button(label = "Selected", w=64, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/xtras.mel\"; scva;')")
    cmds.button(label = "All Mesh", w=64, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"cvz\")"))
    cmds.setParent('..')
    cmds.button(label = "Check Duplicate Mesh", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/Duplicate_mesh.mel\"; dupmeshui;')")
    cmds.button(label = "abSymMesh", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/abSymMesh.mel\"; abSymMesh;')")
    cmds.button(label = "Rename", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/RenameScript.mel\"; cometRename;')")
    cmds.button(label = "Duplicate Auto Rename", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/Duplicate_Auto_Rename.mel\"; autodupwin;')")
    cmds.button(label = "UV Transfer", width=200, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"uvtrans\")"))
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.frameLayout(label='Shader Tools', cll=1, cl=0, lv=1, w=200)
    cmds.columnLayout(w=200, adjustableColumn=1)
    cmds.button(label = "Rename Shading Network", width=200, bgc=(0.1,0.1,0.1), c=(__name__+".cpftam(\"shdrename\")"))
    cmds.button(label = "FTM", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/FileTextureManager.mel\"; FileTextureManager_2018;')")
    cmds.button(label = "Material List", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/Material_List.mel\"; NameSceneUI;')")
    cmds.button(label = "Basic Shader\'s", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/Basic_shader.mel\"; defaultshaderwin;')")
    cmds.button(label = "Remove Duplicate Shader", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/Remove_Duplicate_Shader.mel\"; clean_Shaders;')")
    cmds.button(label = "Remove Unused Shader", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('MLdeleteUnused;')")
    cmds.setParent('..')
    cmds.setParent('..')
    
    cmds.frameLayout(label='File Cleening', cll=1, cl=0, lv=1, w=200)
    cmds.columnLayout(w=200, adjustableColumn=1)
    cmds.button(label = "FINALIZE", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/Finalize.mel\"; finalizze;')")
    cmds.button(label = "Clean File", width=200, bgc=(0.1,0.1,0.1), c="maya.mel.eval('source \"mod_ui_scripts/Clean_FIle.mel\"; CleenFilewin;')")
    cmds.button(label = "CLOSE EDITORS / BOUNDING BOX", width=200, bgc=(0.22, 1.0, 0.09), c="maya.mel.eval('source \"mod_ui_scripts/xtras.mel\"; Clean_Editors;')")
    cmds.setParent('..')
    cmds.setParent('..')

    cmds.setParent('..')

def windowui():
    
    try:
        pm.deleteUI('modwin')
        pm.workspaceControlState('modwin', remove=True)
    except:
        pass
        
    print(__name__)
    cmds.workspaceControl('modwin', tabToControl=('AttributeEditor', -1), li=1, r=1, mw=250 , label=WINDOW_SIDE_TITLE, uiScript=(__name__+".windes()"))
   
# def launchpubui(item=None):
#     pth = tools.showxml.findpath()
#     if(pth == ""):
#         cmds.confirmDialog( title='File Unidentified',  icon="critical", message='File not identified\nProvide correct file name or code.', button=['Okay'], defaultButton='Okay', cancelButton='Okay')
#     else:
#         tools.pub_ui.pubwinui()






def getGroup():
    getconstraint = cmds.ls(type="constraint")
    getplacetex = cmds.ls(type="place3dTexture")
    toremove = getconstraint
    toremove.extend(getplacetex)
    diff = cmds.ls(type="transform")
    getTrs = [i for i in diff if not i in toremove or toremove.remove(i)]
    getGroup = []
    for each in getTrs:
        getShape = cmds.listRelatives(each, s=1)
        if(not getShape):
            getGroup.append(each)
    return getGroup   

def cpftam(rcvstr):
    transforms = maya.cmds.ls(tr=True)
    shapes = maya.cmds.filterExpand(transforms, sm=12)
    groups = getGroup()
    
    if rcvstr == "cpa":
        for shape in shapes:
            maya.cmds.select(shape)
            maya.cmds.xform(cpc=1)
            maya.cmds.select(cl=1)
            
    if rcvstr == "fta":
        for shape in transforms:
            maya.cmds.select(shape)
            maya.cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
            maya.cmds.select(cl=1)
    
    if rcvstr == "dha":
        for shape in shapes:
            maya.cmds.select(shape)
            maya.mel.eval("DeleteHistory;")
            maya.cmds.select(cl=1)
            
    if rcvstr == "ndha":
        for shape in shapes:
            maya.cmds.select(shape)
            maya.mel.eval('doBakeNonDefHistory( 1, {\"prePost\"});')
            maya.cmds.select(cl=1)
            
    if rcvstr == "cpaGrp":
        for group in groups:
            maya.cmds.select(group)
            maya.cmds.xform(cpc=1)
            maya.cmds.select(cl=1)
            
    if rcvstr == "ftaGrp":
        for group in groups:
            maya.cmds.select(group)
            maya.cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
            maya.cmds.select(cl=1)
    
    if rcvstr == "dhaGrp":
        for group in groups:
            maya.cmds.select(group)
            maya.mel.eval("DeleteHistory;")
            maya.cmds.select(cl=1)
            
    if rcvstr == "ndhaGrp":
        for group in groups:
            maya.cmds.select(group)
            maya.mel.eval('doBakeNonDefHistory( 1, {\"prePost\"});')
            maya.cmds.select(cl=1) 
            
    if rcvstr == "cpftdhndh":
        alltra = groups + shapes
        for tra in alltra:
            maya.cmds.select(tra)
            maya.cmds.xform(cpc=1)
            maya.cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
            maya.mel.eval("DeleteHistory;")
            maya.mel.eval('doBakeNonDefHistory( 1, {\"prePost\"});')
            maya.cmds.select(cl=1)
        
            
    if rcvstr == "cvz":
        for shape in shapes:
            maya.cmds.select(shape)
            maya.cmds.polyMoveVertex(localTranslate=[0,0,0])
            maya.mel.eval('doBakeNonDefHistory( 1, {\"prePost\"});')
            maya.cmds.select(cl=1)
    
    if rcvstr == "uvtrans":
        MCuvTrans = uvTrans.MainClassUVTransfer()
        MCuvTrans.uvTransUI()
    
    if rcvstr == "shdrename":
        shdrename.mainui()

if __name__ == "__main__":
    windowui()
