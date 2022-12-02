import maya.cmds as cmds
    
def Sq(proj):#---------For Sequence List-----------
    proj = cmds.optionMenu("Project",q= True, v = True)
    if proj == 'NannyVsGranny':
        fold = "V:/NanniVsGranny/02_episodes/00_teaser/04_lighting"
  
    if proj == 'Space Delivery':
        fold = "V:/SPACE_DELIVERY/02_episodes/00_teaser/04_lighting" 
      
    
    for item in cmds.optionMenu("sequence",q=True, ill = True) or []:
            cmds.deleteUI(item) 
    list1 = cmds.getFileList(folder = fold)
    if not list1 == []:
        for seq in list1:
            cmds.menuItem(label = seq, parent = "sequence")
    else:
        print "\n\n No Folder Found "
        
        

def sh(seq):     #--------For Shot List -------- 
    proj = cmds.optionMenu("Project",q= True, v = True)
    if proj == 'NannyVsGranny':
        fold = "V:/NanniVsGranny/02_episodes/00_teaser/04_lighting"
  
    if proj == 'Space Delivery':
        fold = "V:/SPACE_DELIVERY/02_episodes/00_teaser/04_lighting" 
    for item in cmds.optionMenu("Shot",q=True, ill = True) or []:
            cmds.deleteUI(item) 
     
    Seq = cmds.optionMenu("sequence",q= True, v = True)
    var = Seq.split('_')
    out = fold + '/' + Seq + '/' + var[0] + '_Maya'
    list2 = cmds.getFileList(folder = out)
    if not list2 == []:
        for sh in list2:
            cmds.menuItem(label = sh, parent = "Shot")
    else:
        print "\n\n No Folder Found "
        
        
def imp(s):     #--------For Importing Alembic ----------
    proj = cmds.optionMenu("Project",q= True, v = True)
    if proj == 'NannyVsGranny':
        fold = "V:/NanniVsGranny/02_episodes/00_teaser/04_lighting"
  
    if proj == 'Space Delivery':
        fold = "V:/SPACE_DELIVERY/02_episodes/00_teaser/04_lighting"
    Sq = cmds.optionMenu("sequence",q= True, v = True)
    s = cmds.optionMenu("Shot",q= True, v = True)
    var = Sq.split('_')
    v = s.split('_')
    out = fold + '/' + Sq + '/' + var[0] + '_Maya'
    f = out + '/' + s + '/' + 'Cch/' + v[0] + '_Cch'
    list3 = cmds.getFileList(folder = f)
    if not list3 == []:
        for i in list3:
            im = f + '/' + i
            list4 = cmds.getFileList(folder = im)
            if not list4 == []:
                for each in list4:
                    cmds.file(f + '/' + i + '/' + each, i = True, ignoreVersion = True , type = "Alembic")
            else:
                cmds.confirmDialog(title = 'ERROR', message= "No Folder Found", button = 'OK', cancelButton = 'OK', defaultButton = 'OK')
    else:
        cmds.confirmDialog(title = 'ERROR', message= "No Folder Found", button = 'OK', cancelButton = 'OK', defaultButton = 'OK')
    cmds.confirmDialog(title = 'Successfull', message= "Alembic Imported", button = 'OK', cancelButton = 'OK', defaultButton = 'OK')
        

        
def cam(*args):
    #V:\NanniVsGranny\02_episodes\00_teaser\04_lighting\Sq02_lit\Sq02_Ue\Content\Cm\sh02_Cm
    proj = cmds.optionMenu("Project",q= True, v = True)
    if proj == 'NannyVsGranny':
        fold = "V:/NanniVsGranny/02_episodes/00_teaser/04_lighting"
  
    if proj == 'Space Delivery':
        fold = "V:/SPACE_DELIVERY/02_episodes/00_teaser/04_lighting"
        
    Sq = cmds.optionMenu("sequence",q= True, v = True)
    s = cmds.optionMenu("Shot",q= True, v = True)
    var = Sq.split('_')
    var2 = s.split('_')
    camOut = fold + '/' + Sq + '/' + var[0] + '_Maya/' + var2[0] + '/Cm/' + var2[0] + '_Cm'
    print camOut
    listCam = cmds.getFileList(folder = camOut)
    if not listCam == []:
        for each in listCam:
            cmds.file(camOut + '/' + each, i = True, ignoreVersion = True ,mergeNamespacesOnClash = True,namespace = ":" , type = "Fbx")
            cmds.confirmDialog(title = 'Successfull', message= "Camera Imported", button = 'OK', cancelButton = 'OK', defaultButton = 'OK')
    else:
        cmds.confirmDialog(title = 'ERROR', message= "No Camera Found", button = 'OK', cancelButton = 'OK', defaultButton = 'OK')
    



#---------------WINDOW-----------------        
       
if cmds.window("ImportUI", exists = True):
		cmds.deleteUI("ImportUI")
		                               
wide = 300
height = 200
window = cmds.window("ImportUI", t = "Import Alembic", w = wide, h = height, sizeable = False)

#cmds.columnLayout(w = wide,h = height, co =["left",10])
cmds.rowColumnLayout(nc=2, columnWidth = [(1,200),(2,200)], columnOffset = [(1,'left',10),(2,'right',50)])

#--------------PROJECT-----------------
cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')
cmds.text("Select Project : ")
cmds.optionMenu("Project", w = 150, cc = Sq)
cmds.menuItem(label = 'NannyVsGranny', parent = "Project")
cmds.menuItem(label = 'Space Delivery', parent = "Project")
        

#--------------SEQUENCE-----------------
cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')
cmds.text("Select Sequence : ")
cmds.optionMenu("sequence", w = 150, cc = sh)


#--------------SHOT-----------------
cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')
cmds.text("Select Shot : ")
cmds.optionMenu("Shot", w = 150)


#--------------IMPORT ALEMBIC-----------------
cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')

cmds.button(label = "IMPORT ALEMBIC", h = 20, w = 120,command = imp)


#--------------IMPORT CAM-----------------
cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')
cmds.separator(h=20, style='none')

cmds.button(label = "IMPORT CAMERA", h = 20, w = 120,command = cam)


cmds.showWindow(window)  

