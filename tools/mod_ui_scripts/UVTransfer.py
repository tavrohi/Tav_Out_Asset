# UVTransfer v1.0
# License: MIT Licence (See LICENSE.txt or https://choosealicense.com/licenses/mit/)
# Copyright (c) 2017 Erik Lehmann
# Date: 08/21/17
#
# Description: 
#	Transfer UVs from one to several other objects.
# 
# How to use:
#	1. Select sample space (World, Local, Component, Topology).
#	2. Select and set source object.
# 	3. Select and set target object(s).
#	4. Run "Copy UVs".
#
# Installation: 
# 	1. 	Copy UVTransfer.py to '\Users\[USER]\Documents\maya\[MAYAVERSION]\prefs\scripts'
# 	2. 	Launch / Restart Maya
#	3.	Type into 'Script Editor' (Python tab) and execute:
#       import UVTransfer as uvTrans
#       MCuvTrans = uvTrans.MainClassUVTransfer()
#       MCuvTrans.uvTransUI()


import maya.cmds as cmds

class MainClassUVTransfer:
    
	def __init__(self):
		self.uvTransSourceObject = []
		self.uvTransTargetObject = []
		self.uvTransSampleSpace = 0
		self.uvTransProgressControl = ""
		self.uvTransControlCheck = False
		self.uvTransAmount = 0

	def uvTransUI(self, _=False):	
		
		# C H E C K  W I N D O W

		if (cmds.window("uvTransWin", exists=True)):
			cmds.deleteUI("uvTransWin", wnd=True)
			cmds.windowPref("uvTransWin", r=True)

			
		# C R E A T E  U I

		cmds.window("uvTransWin", s=False, tlb=True, rtf=True, t="UV Transfer")
		cmds.columnLayout(adj=True)


		# S A M P L E  S P A C E

		cmds.frameLayout(l="Sample Space", la="top", bgc=(0.3, 0.3, 0.3), cll=False, cl=False)

		cmds.gridLayout(numberOfRowsColumns=(1, 3), cellWidthHeight=(70, 30))

		cmds.radioCollection()
		self.worldRB = cmds.radioButton( label='World')
		self.cmptRB = cmds.radioButton( label='Cmpt' )
		self.topoRB = cmds.radioButton( label='Topo', select=True )

		cmds.setParent('..')
		cmds.setParent('..')


		# S O U R C E

		cmds.frameLayout(l="Source", la="top", bgc=(0.3, 0.3, 0.3), cll=False, cl=False, w = 200)
		cmds.columnLayout(adj=True)

		cmds.button(label="Set Source Object", c = self.uvTransSetSource, h = 30 )

		cmds.textScrollList("uvTransSourceList", h=30, ams=False)
		
		cmds.setParent('..')
		cmds.setParent('..')
		

		# T A R G E T

		cmds.frameLayout(l="Target", la="top", bgc=(0.3, 0.3, 0.3), cll=False, cl=False, w = 200)
		cmds.columnLayout(adj=True)

		cmds.button(label="Set Target Object(s)", c = self.uvTransSetTarget, h = 30 )

		cmds.textScrollList("uvTransTargetList", h=100, ams=False)

		
		# C O P Y  U V S
		
		cmds.button(label="Copy UVs", bgc=(0.24, 0.72, 0.46), c = self.uvTransCopyUVs, h = 40 )

		cmds.setParent('..')
		cmds.setParent('..')

		
		# S H O W  W I N D O W

		cmds.showWindow("uvTransWin")		
	
	
	# M E T H O D S

	# S O U R C E
          
	def uvTransSetSource(self, _=False):
		
		self.uvTransSourceObject = cmds.ls(sl=True)

		cmds.textScrollList("uvTransSourceList", e=True, ra=True)

		for i in self.uvTransSourceObject:
			cmds.textScrollList("uvTransSourceList", e=True, a=(i))
		
		
	# T A R G E T
		
	def uvTransSetTarget(self, _=False):
		
		self.uvTransTargetObject = cmds.ls(sl=True)

		cmds.textScrollList("uvTransTargetList", e=True, ra=True)

		for i in self.uvTransTargetObject:
			cmds.textScrollList("uvTransTargetList", e=True, a=(i))
	
	
	# C O P Y
		
	def uvTransCopyUVs(self, _=False):
	    
		if cmds.radioButton(self.worldRB, q=True, select=True):
			self.uvTransSampleSpace = 0
			
		if cmds.radioButton(self.cmptRB, q=True, select=True):
			self.uvTransSampleSpace = 4
			
		if cmds.radioButton(self.topoRB, q=True, select=True):
			self.uvTransSampleSpace = 5

		self.uvTransAmount = len(self.uvTransTargetObject)

		if self.uvTransAmount > 100:
			self.uvTransProgressControl = cmds.progressWindow(t="In progress...", ii=True, maxValue = self.uvTransAmount)
			self.uvTransControlCheck = True
			
		
			
		for i in self.uvTransTargetObject:
			cmds.select(self.uvTransSourceObject)
			cmds.select(i, add=True)
			cmds.transferAttributes(pos=0, nml=0, uvs=2, col=0, 
			spa=self.uvTransSampleSpace, sus="map1", tus="map1", sm=3, fuv=0, clb=1)

			cmds.DeleteHistory()

			if self.uvTransControlCheck == True and cmds.progressWindow(self.uvTransProgressControl, q=True, ic=True):
					break

			if self.uvTransControlCheck == True:
				cmds.progressWindow(self.uvTransProgressControl, edit=True, step=1)

		
		cmds.select(cl=True, d=True) 
		cmds.progressWindow(self.uvTransProgressControl, edit=True, ep=True)
		   

#MCuvTrans = MainClassUVTransfer()
#MCuvTrans.uvTransUI()