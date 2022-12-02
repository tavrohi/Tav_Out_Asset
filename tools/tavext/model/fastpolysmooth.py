
# Script done by: Igor Dmytrenko

########### fast poly smooth #########
# how to use scrip - create button on the shelf in maya and put this code inside:
# don't forgen delete '#' befor line

# import fastpolysmooth as sd
# reload(sd)
# sd.SubdWindow().show()

import maya.cmds as cmds

class SubdWindow(object):

    window_name = "Fast_poly_Smooth"

    def subdivide(self, x):
               
        sel = cmds.ls(sl=1)

        for obj in sel:
            cmds.select(obj)
            cmds.polySmooth(obj+".", sdt=2, dv= x )

    def show(self):
        sel = cmds.ls(sl=1)

        # if len(sel) == 0:
        #     print "You need select object"

        # if len(sel) > 0:

        if cmds.window(self.window_name, query=True, exists=True):
            cmds.deleteUI(self.window_name)

        cmds.window(self.window_name, w = 250, h = 300)

        self.buildUI()

        cmds.showWindow()


    def buildUI(self):

        column = cmds.columnLayout()

        cmds.text(label="Use this slider to set subdivision level")

        row = cmds.rowLayout(numberOfColumns = 5)

        self.label = cmds.text(label="1")

        self.slider = cmds.intSliderGrp(min=1, max=5, value=1, step=1, dragCommand = self.sdv)  # changeCommand=subdivide
              
        # cmds.button(label="Reset", command=self.reset)
        cmds.button(label="Subdivide", command=self.subd)
        # cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def sdv(self, sdvcount):
        cmds.text(self.label, edit = True, label=sdvcount)
        # print sdvcount

    def subd(self, *args):
        subd_count = cmds.intSliderGrp(self.slider, query = True, value = True)
        self.subdivide(subd_count)
        # self.close()
        
    # def reset(self, sdvcount):
    #     cmds.intSlider(self.slider, edit=True, value=1)
                
             
    def close(self, *args):
        cmds.deleteUI(self.window_name)