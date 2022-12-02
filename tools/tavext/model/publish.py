import maya.cmds as cmds
import pymel.core as pm
from maya import mel
import os


if cmds.pluginInfo('AbcExport.mll' , query = True, loaded = True) == False:
    pm.loadPlugin("AbcExport.mll")
    print "\n****ABC Plugin Loaded****"
else:
    print "\n****ABC Plugin Already Loaded****"


def createSet(*args):
    subDiv = cmds.optionMenu("CreateSet", q = True, v = True)
    mesh = cmds.ls(selection=True, dag = True, type ="transform")
    if mesh == []:
        cmds.error("***Please select an object***")
    else:
        set1 = cmds.ls("forSmooth",type = "objectSet")
        set2 = cmds.ls("forSmooth_2",type = "objectSet")
        if set1 == [] or set2 == []:
            cmds.sets(n="forSmooth", empty = True)
            cmds.addAttr ("forSmooth" + "." , longName='smoothness',keyable=True, minValue=0, maxValue=2, defaultValue=0)
            cmds.sets(n="forSmooth_2", empty = True)
            cmds.addAttr ("forSmooth_2"+ "." , longName='smoothness',keyable=True, minValue=0, maxValue=2, defaultValue=0)
        for each in mesh:
                if int(subDiv) == 0:
                        cmds.sets(each, rm = "forSmooth")
                        cmds.sets(each, rm = "forSmooth_2")
                if int(subDiv) == 1:
                        cmds.sets(each, include="forSmooth")
                        cmds.sets(each, rm = "forSmooth_2")
                if int(subDiv) == 2:
                        cmds.sets(each, include="forSmooth_2")
                        cmds.sets(each, rm = "forSmooth")
        
        print "------- Sub Divisions added Sucessfully ---------"
       
       
       
def attr(*args):

    try:
        'forSmooth'
        if 'forSmooth':   
            cmds.select("forSmooth")    
            sel = cmds.ls(sl = True)
            for each in sel:
                
                poly = cmds.polySmooth  (each, sdt=2, dv=0, kb=0, suv=1)
                cmds.connectAttr ("forSmooth" + '.smoothness', poly[0] + '.divisions')
                
                
        set = cmds.ls("forSmooth_2",type = "objectSet")
        if set[0] == "forSmooth_2":
            cmds.select("forSmooth_2")    
            sel = cmds.ls(sl = True)
            for each in sel:
                
                poly = cmds.polySmooth  (each, sdt=2, dv=0, kb=0, suv=1)
                cmds.connectAttr ("forSmooth_2" + '.smoothness', poly[0] + '.divisions')
    
            
    except:
        print "\n\n******NO SET TO SELECT********"
		
		
def ref(*args):
    
    cmds.delete('*polySmoothFace*')
    
    set1 = cmds.ls("forSmooth",type = "objectSet")
    set2 = cmds.ls("forSmooth_2",type = "objectSet")
    
    if set1 == []:
        cmds.sets(n="forSmooth", empty = True)
        cmds.addAttr ("forSmooth"+ "." , longName='smoothness',keyable=True, minValue=0, maxValue=2, defaultValue=0)
    if set2 == []:
        cmds.sets(n="forSmooth_2", empty = True)
        cmds.addAttr ("forSmooth_2"+ "." , longName='smoothness',keyable=True, minValue=0, maxValue=2, defaultValue=0)

    try:
        'forSmooth'
        if 'forSmooth':   
            cmds.select("forSmooth")    
            sel = cmds.ls(sl = True)
            for each in sel:
                
                poly = cmds.polySmooth  (each, sdt=2, dv=0, kb=0, suv=1)
                cmds.connectAttr ("forSmooth" + '.smoothness', poly[0] + '.divisions')
                
                
        set = cmds.ls("forSmooth_2",type = "objectSet")
        if set[0] == "forSmooth_2":
            cmds.select("forSmooth_2")    
            sel = cmds.ls(sl = True)
            for each in sel:
                
                poly = cmds.polySmooth  (each, sdt=2, dv=0, kb=0, suv=1)
                cmds.connectAttr ("forSmooth_2" + '.smoothness', poly[0] + '.divisions')
    
            
    except:
        print "\n\n******NO SET TO SELECT********"		
        

def prev(prv):
    print prv
    if str(prv) == 'ON':
        cmds.select("forSmooth")
        cmds.setAttr ("forSmooth" + '.smoothness', 1)
        cmds.select("forSmooth_2")
        cmds.setAttr ("forSmooth_2" + '.smoothness', 2)
                
    elif str(prv) == 'OFF':
        cmds.select("forSmooth")
        cmds.setAttr ("forSmooth" + '.smoothness', 0)
        cmds.select("forSmooth_2")
        cmds.setAttr ("forSmooth_2" + '.smoothness', 0)
        
def cSet(*args):
    mesh = cmds.ls(selection=True)
    
    if mesh == []:
        cmds.error("***Please select an object***")
    else:
        cmds.sets(mesh, n="forCache")     
        
def abcEx(*args):
    #path = cmds.file(q=True, sn=True)
    
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    path, filename = os.path.split(filepath)
    head, tail = os.path.splitext(filename)
    f = head.split('_')[:-1]
    fo =  r'_'.join(f)
    
    f1 = cmds.playbackOptions(q=True, min=True)
    f2 = cmds.playbackOptions(q=True, max=True)
    
    ######################## Export ASSET #########################

    ABCoutput =  path + '/' + fo + "_abc"
    FBXoutput =  path + '/' + fo + "_fbx"
    cmds.sysFile(ABCoutput, makeDir=True)
    cmds.select("forCache")
    object = cmds.ls(selection=True, long=True)
    root = r' -root '.join(object)
    ABCpath = ABCoutput + '/' + fo + ".abc"
    ABCcommand = "-frameRange" + " " + str(int(f1)) + " " + str(int(f1)) + " " + "-uvWrite -worldSpace -writeVisibility -writeFaceSets -writeUVSets -root" + " " + str(root) + " " + "-file" + " " + str(ABCpath)
    cmds.AbcExport(j=ABCcommand)
    
    #cmds.deleteUI("publishUI")
    cmds.confirmDialog(title = 'Successfull', message= "Alembic Exported SuccessFully to :\n" + ABCpath , button = 'OK', cancelButton = 'OK', defaultButton = 'OK')
   

def aiCon(*args):
    import unreal.Convert_AI_to_Blinn
    unreal.Convert_AI_to_Blinn.convertUi()
    
def fbxEx(*args):
    
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    path, filename = os.path.split(filepath)
    head, tail = os.path.splitext(filename)
    f = head.split('_')[:-1]
    fo =  r'_'.join(f)
    
    f1 = cmds.playbackOptions(q=True, min=True)
    f2 = cmds.playbackOptions(q=True, max=True)
    
    ######################## Export ASSET #########################

    FBXoutput =  path + '/' + fo + "_fbx"
    cmds.sysFile(FBXoutput, makeDir=True)
    cmds.select("forCache")
    object = cmds.ls(selection=True, long=True)
    
    for each in object:
        cmds.delete(each, constructionHistory = True)
        
    FBXpath = FBXoutput + '/' + fo + ".fbx"
    pm.mel.eval('FBXExportFileVersion "FBX2018"')
    pm.mel.eval('FBXResetExport')
    pm.mel.eval('FBXExportInputConnections -v 0')
    pm.mel.eval('FBXExportEmbeddedTextures -v true')
    pm.mel.eval('FBXExportInAscii -v false')
    pm.mel.eval('FBXExportAnimationOnly -v false')

    cmds.select("forCache")
    
    cmds.file(FBXpath,force=True,typ="FBX export",pr=False, es=True)
    
    #cmds.deleteUI("publishUI")
    cmds.confirmDialog(title = 'Successfull', message= "FBX Exported SuccessFully to :\n" + FBXpath , button = 'OK', cancelButton = 'OK', defaultButton = 'OK')

                       
if cmds.window("publishUI", exists = True):
		cmds.deleteUI("publishUI")
		                               
wide = 500
height = 200
#create window
window = cmds.window("publishUI", t = "Publish Asset For Unreal Engine", w = wide, h = height, sizeable = False)


#create a main layout
cmds.rowColumnLayout(nc=2, columnWidth = [(1,400),(2,150)], columnOffset = [(1,'left',10),(2,'right',10)])

cmds.text("\n\n****Make Sure to select meshes before creating set.\n\n0. - To remove elements from both the SETS.\n1. - To add elements to 'forSmooth' SET.\n2. - To add elements to 'forSmooth_2' SET.", align='left')
cmds.text("")

cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')

cmds.optionMenu("CreateSet", w = 200, label = "1) Create SET:      ")
cmds.menuItem(label = "0", parent = "CreateSet")
cmds.menuItem(label = "1", parent = "CreateSet")
cmds.menuItem(label = "2", parent = "CreateSet")
cmds.button(label = "Create", h = 20, w = 100,command = createSet) 

cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')


cmds.text("1) Add Smoothness Attribute to the elements of both the SETS.")
cmds.button(label = "Add Attribute", h = 20, w = 100, command = attr)

cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')


cmds.text("1) Update SET connections.")
cmds.button(label = "Refresh Sets", h = 20, w = 100, command = ref)

cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')

cmds.text("1) create Export Set.")
cmds.button(label = "Create Cache Set", h = 20, w = 100, command = cSet)

cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')

cmds.text("2) Mesh Preview with Subdivision Values") 
cmds.optionMenu("MeshPrev", w = 100,changeCommand = prev)
cmds.menuItem(label = "OFF", parent = "MeshPrev")
cmds.menuItem(label = "ON", parent = "MeshPrev")


cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')

cmds.text("3) Alembic Export the elements of SET 'forCache.'") 
cmds.button(label = "Export Alembic", h = 20, w = 100,command = abcEx)

cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')

cmds.separator(h=20, style='none')
cmds.button(label = "Convert AI to Blinn", h = 20, w = 100,command = aiCon)
cmds.separator(h=20, style='none')

cmds.separator(h=20, style='none')
cmds.text("4)  FBX Export the elements of SET 'forCache.'") 
cmds.button(label = "Export FBX", h = 20, w = 100,command = fbxEx)
                                                                                                                                                              
cmds.showWindow(window)