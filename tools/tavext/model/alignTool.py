import maya.mel as mel
import maya.cmds as cmds
from functools import partial
 
 
 
class AlignSelection():
     
 
    #####_______ALIGN SELECTION DEFINITION_______#####
    def align_object(self, *args):
 
 
        # Define Source and Target Obj
        current_object = cmds.textFieldGrp('curObj', q=True, tx=True)
        target_object = cmds.textFieldGrp('tarObj', q=True, tx=True)
         
        if current_object == "Select an Obj + update":
            cmds.confirmDialog( title='Warning', message="Select a source and a target object and press Update")
        
        if current_object != "Select an Obj + update":
        
            current_object_evaluate = cmds.polyEvaluate(current_object, boundingBox=True)
            target_object_evaluate = cmds.polyEvaluate(target_object, boundingBox=True)
             
             
            # Get Initial pivot position
            current_object_initialPivot = cmds.xform(current_object,q=1,ws=1,rp=1)
            target_object_initialPivot = cmds.xform(target_object,q=1,ws=1,rp=1)
             
            # Center pivot
            cmds.xform(current_object,  cp=1)
            current_object_centerPivot = cmds.xform(current_object,q=1,ws=1,rp=1)
     
             
            #Reset Pivot position
            current_object_resetPivot = cmds.move(current_object_initialPivot[0],current_object_initialPivot[1],current_object_initialPivot[2], current_object+".scalePivot", current_object+".rotatePivot", absolute=True)
             
           
            #Rounded list to generate relative pivot
            current_object_initialPivot_FormatedList = [ '%.10f' % elem for elem in current_object_initialPivot ]
            current_object_centerPivot_FormatedList = [ '%.10f' % elem for elem in current_object_centerPivot ]
             
             
            ######___CURRENT OBJECT____#####
             
      
            # CURRENT OBJECT = PIVOT
            if cmds.radioButtonGrp("radio_current_object", query=True, sl=True)==3:
                # Calculate relative pivot from center object
                current_object_relativePivot = [float(current_object_initialPivot_FormatedList[0])-float(current_object_centerPivot_FormatedList[0]), float(current_object_initialPivot_FormatedList[1])-float(current_object_centerPivot_FormatedList[1]), float(current_object_initialPivot_FormatedList[2])-float(current_object_centerPivot_FormatedList[2])]
             
             
            # CURRENT OBJECT = CENTER
            if cmds.radioButtonGrp("radio_current_object", query=True, sl=True)==2:
                cmds.xform(current_object,  cp=1)
                # Calculate relative pivot from center object
                current_object_relativePivot = [float(current_object_initialPivot_FormatedList[0])-float(current_object_centerPivot_FormatedList[0]), float(current_object_initialPivot_FormatedList[1])-float(current_object_centerPivot_FormatedList[1]), float(current_object_initialPivot_FormatedList[2])-float(current_object_centerPivot_FormatedList[2])]
             
             
            # CURRENT OBJECT = MINIMUM
            if cmds.radioButtonGrp("radio_current_object", query=True, sl=True)==1:
                Ymin = current_object_evaluate[1][0]
                current_object_pivotRelativeY = current_object_initialPivot[1]- Ymin
                 
                # Calculate relative pivot from minimum object
                current_object_relativePivot = [0,current_object_pivotRelativeY, 0]
     
                cmds.move(current_object_initialPivot[0], Ymin, current_object_initialPivot[2], current_object+".scalePivot",current_object+".rotatePivot", absolute=True)
                 
            # CURRENT OBJECT = MAXIMUM
            if cmds.radioButtonGrp("radio_current_object", query=True, sl=True)==4:
                Ymax = current_object_evaluate[1][1]
                current_object_pivotRelativeY = current_object_initialPivot[1]-Ymax
                 
                # Calculate relative pivot from minimum object
                current_object_relativePivot = [0,current_object_pivotRelativeY, 0]
     
                cmds.move(current_object_initialPivot[0], Ymax, current_object_initialPivot[2], current_object+".scalePivot",current_object+".rotatePivot", absolute=True)
                 
                 
                 
            ######___TARGET OBJECT____#####  
               
             
            # TARGET OBJECT = PIVOT
            if cmds.radioButtonGrp("radio_target_object", query=True, sl=True)==3:
                pass
             
            # TARGET OBJECT = CENTER
            if cmds.radioButtonGrp("radio_target_object", query=True, sl=True)==2:
                cmds.xform(target_object,  cp=1)
                 
            # TARGET OBJECT = MINIMUM  
            if cmds.radioButtonGrp("radio_target_object", query=True, sl=True)==1:
                cmds.xform(target_object,  cp=1)
                Ymin = target_object_evaluate[1][0]
                target_object_minPivot = cmds.xform(target_object,q=1,ws=1,rp=1)
                cmds.move(target_object_minPivot[0], Ymin, target_object_minPivot[2], target_object+".scalePivot",target_object+".rotatePivot", absolute=True)
               
             # TARGET OBJECT = MAXIMUM    
            if cmds.radioButtonGrp("radio_target_object", query=True, sl=True)==4:
                cmds.xform(target_object,  cp=1)
                Ymin = target_object_evaluate[1][1]
                target_object_minPivot = cmds.xform(target_object,q=1,ws=1,rp=1)
                cmds.move(target_object_minPivot[0], Ymin, target_object_minPivot[2], target_object+".scalePivot",target_object+".rotatePivot", absolute=True)
             
             
            skipRotate = []
            skipTranslate=[]
            skipScale=[]
             
            if cmds.checkBox('xAxisO', query=True, value=True)== 0:
                skipRotate.append("x")
            if cmds.checkBox('yAxisO', query=True, value=True)== 0:
                skipRotate.append("y")
            if cmds.checkBox('zAxisO', query=True, value=True)== 0:
                skipRotate.append("z")
             
            if cmds.checkBox('xpos', query=True, value=True) == 0:
                skipTranslate.append("x")
            if cmds.checkBox('ypos', query=True, value=True) == 0:
                skipTranslate.append("y")
            if cmds.checkBox('zpos', query=True, value=True) == 0:
                skipTranslate.append("z")
     
            if cmds.checkBox('xAxisS',query=True, value=True) == 0:
                skipScale.append("x")
            if cmds.checkBox('yAxisS',query=True, value=True) == 0:
                skipScale.append("y")
            if cmds.checkBox('zAxisS',query=True, value=True) == 0:
                skipScale.append("z")
     
            # Apply and remove parent and Scale Constraints
            parent_cst = cmds.parentConstraint(target_object, current_object, skipRotate=skipRotate, skipTranslate=skipTranslate, maintainOffset=False, weight = 1)
            scale_cst = cmds.scaleConstraint(target_object, current_object, skip=skipScale, weight=1, mo=False)
            cmds.delete(parent_cst, scale_cst)
             
            # Get new pivot at position
            current_object_newPivot = cmds.xform(current_object,q=1,ws=1,rp=1)
             
            # Rounded list to generate new pivot
            current_object_newPivotFormatedList = [ '%.10f' % elem for elem in current_object_newPivot ]
             
            # Calculate new pivot position for current_object
            current_object_newPivot = [float(current_object_newPivotFormatedList[0])+float(current_object_relativePivot[0]),float(current_object_newPivotFormatedList[1])+float(current_object_relativePivot[1]),float(current_object_newPivotFormatedList[2])+float(current_object_relativePivot[2])]
             
            # Reset pivot position thanks to new pivot position
            current_object_resetPivot = cmds.move(current_object_newPivot[0],current_object_newPivot[1],current_object_newPivot[2], current_object+".scalePivot", current_object+".rotatePivot", absolute=True)
             
            
            # Reset pivot position for Target
            #target_object_pivotFormatedList = [ '%.10f' % elem for elem in target_object_initialPivot ]
            target_object_resetPivot = cmds.move(target_object_initialPivot[0],target_object_initialPivot[1],target_object_initialPivot[2], target_object+".scalePivot", target_object+".rotatePivot", absolute=True)
 
  
 
    #####_______CANCEL DEFINITION_______#####
     
    def cancel(self, *args):
         
        if cmds.window("align_window", exists=True)==1:
            cmds.deleteUI("align_window")
         
         
    #####_______UPDATE OBJECTS DEFINITION_______#####
     
    def checkbox_check(self, check_val, *args):
              
        cmds.checkBox('xpos', e=True, v=check_val)
        cmds.checkBox('ypos', e=True, v=check_val)
        cmds.checkBox('zpos',  e=True, v=check_val)
 
        cmds.checkBox('xAxisO', e=True, v=check_val)
        cmds.checkBox('yAxisO',  e=True, v=check_val)
        cmds.checkBox('zAxisO',  e=True, v=check_val)
         
        cmds.checkBox('xAxisS', e=True, v=check_val)
        cmds.checkBox('yAxisS', e=True, v=check_val)
        cmds.checkBox('zAxisS', e=True, v=check_val)
 
    #####_______UPDATE OBJECTS DEFINITION_______#####
 
    def update_objects(self, *args):
         
        sel = cmds.ls(sl=True)
         
        if len(sel)!= 2:
             cur_obj="Select an Obj + update"
             tar_obj="Select an Obj + update"
        if len(sel)== 2:
            cur_obj=sel[0]
            tar_obj=sel[1]
             
        cmds.textFieldGrp('curObj', edit=True, tx=cur_obj)
        cmds.textFieldGrp('tarObj', edit=True, tx=tar_obj) 
 
    
    #####_______INTERACTIVE DEFINITION_______#####
 
    def interactive_Align(self, *args):
         
        if cmds.iconTextCheckBox('interactive',query=True, v=True) == 1 :
            self.align_object()
     
    #####_______ALIGN SELECTION UI DEFINITION_______#####
     
    def align_UI(self, *args): 
     
        sel = cmds.ls(sl=True)
         
        if len(sel)!= 2:
             cur_obj="Select an Obj + update"
             tar_obj="Select an Obj + update"
              
             if len(sel)>2:
                 cmds.warning("Too many Objects selected")
              
        if len(sel)== 2:
            cur_obj=sel[0]
            tar_obj=sel[1]
     
        mainBg=[0,0,0]
        secBg=[0.3,0.6,1]
        width = 230
        height= 465
        allowedAreas = ['right', 'left']
 
        if cmds.window("align_window", exists=True)==1:
            cmds.deleteUI("align_window")
         
        cmds.window("align_window",  title="Align Selection v1.0", iconName='ALS', widthHeight=(width, height) )
 
        if cmds.dockControl("dockwindowALS", exists=True)==1:
            cmds.deleteUI("dockwindowALS")
 
        cmds.columnLayout( adjustableColumn=True,rs=0)
         
        cmds.dockControl("dockwindowALS", area='left', content="align_window", allowedArea=allowedAreas, fl=True, l='Align Selection v1.0', width=width, height=height )
         
        cmds.frameLayout(l="Objects :", bgc=mainBg, marginHeight =5)
         
        cmds.button("update", l="Update", bgc=secBg, c=partial(self.update_objects))
         
        cmds.textFieldGrp('curObj', l='Current Object', tx=cur_obj, cw2=[85,150], ed =False)
        cmds.textFieldGrp('tarObj', l='Target Object', tx=tar_obj, cw2=[85,150], ed =False)
         
        cmds.setParent( '..' )
         
 
        ####___ALIGN POSITION___####
        cmds.frameLayout(l="Align Position (World)", cl=False, cll=True, bgc=mainBg, marginHeight =5)
         
        cmds.flowLayout() 
         
        cmds.checkBox('xpos', l="X Position", v=1)
        cmds.checkBox('ypos', l="Y Position", v=1)
        cmds.checkBox('zpos', l="Z Position", v=1)
 
        cmds.setParent( '..' )
         
        cmds.iconTextCheckBox('interactive', style='textOnly',  label='INTERACTIVE ALIGN' )
         
        cmds.flowLayout()
         
        cmds.frameLayout(l="Current Object :",  bgc=[0.1,0.1,0.1], marginHeight =5)
        cmds.radioButtonGrp("radio_current_object", label='', labelArray4=['Minimum', 'Center', 'Pivot Point', 'Maximum'], sl=3,cw2=[5,100], numberOfRadioButtons=4, vr=True, cc=partial(self.interactive_Align) )
        cmds.setParent( '..' )
         
        cmds.frameLayout(l="Target Object :", bgc=[0.1,0.1,0.1], marginHeight =5)
        cmds.radioButtonGrp("radio_target_object", label='', labelArray4=['Minimum', 'Center', 'Pivot Point', 'Maximum'], sl=3, cw2=[5,100],numberOfRadioButtons=4, vr=True, cc=partial(self.interactive_Align) )
        cmds.setParent( '..' )
         
        cmds.setParent( '..' ) 
        cmds.setParent( '..' )
         
         
        ####___ALIGN ROTATION####
         
        cmds.frameLayout(l="Align Orientation (Local)", cl=False, cll=True, bgc=mainBg, marginHeight =5)
         
        cmds.flowLayout() 
         
        cmds.checkBox('xAxisO', l="X Axis", v=1)
        cmds.checkBox('yAxisO', l="Y Axis", v=1)
        cmds.checkBox('zAxisO', l="Z Axis", v=1)
         
        cmds.setParent( '..' )
         
        cmds.setParent( '..' )
         
        ####___MATCH SCALE####
         
        cmds.frameLayout(l="Match Scale", cl=False, cll=True, bgc=mainBg, marginHeight =5)
         
        cmds.flowLayout() 
         
        cmds.checkBox('xAxisS', l="X Axis")
        cmds.checkBox('yAxisS', l="Y Axis")
        cmds.checkBox('zAxisS', l="Z Axis")
         
        cmds.setParent( '..' )
         
        cmds.setParent( '..' )
         
        cmds.flowLayout() 
        cmds.button("check_all", l="Check All", w=width/2, bgc=secBg, c=partial(self.checkbox_check, 1))
        cmds.button("uncheck_all", l="Uncheck All", w=width/2,bgc=secBg, c=partial(self.checkbox_check, 0))
        cmds.setParent( '..' )
         
        cmds.flowLayout() 
         
         
        cmds.button("apply", l="Apply", w=width/2, c=partial(self.align_object))
         
        cmds.button("cancel", l="Cancel", w=width/2, c=partial(self.cancel))
         
        #cmds.showWindow("align_window")
         
ALS=AlignSelection()
ALS.align_UI()