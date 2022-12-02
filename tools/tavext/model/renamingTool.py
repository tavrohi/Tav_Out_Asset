###############################################################################
##																																					 ##
## DESCRIPTION:																															 ##
##	  A renaming utility with basic Prefix, Suffix, Search &                 ##
##	Replace, and Rename with number and padding option .  Works on           ##
##	Selected objects, Heirarchy and all objects and option for               ##
##	specifing object type.																								   ##
##																																					 ##
## USAGE:                                                                    ##
##		import renamingTool																									   ##
##		cls = renamingTool.mainClassRNT()																	     ##
##		cls.mainUI_RNT()																										   ##
##																																					 ##
## AUTHORS:			                                                             ##
##	Arun . S - arunpillaii@gmail.com                                         ##
##												                       				                     ##
## VERSIONS:                                                                 ##
##	1.00 - March 27, 2009.                                                   ##
##									                                                         ##
###############################################################################

#importing modules
import maya.cmds as mc
import maya.mel as mm
import string

#Class Start..	
class mainClassRNT:

	#dictionary
	ren_Dic = {'renRBG':None,'typeOPM':None ,'objtype':None , 'mainTFG':None , 'strtIF':None , 'padIF':None,'prefixTF':None,'suffixTF':None }
		
###################################################################################
	#class initilizaion
	def __init__ (self):
		 pass

####################################################################################
	#Main UI Creation
	def mainUI_RNT(self):
		#Check for Window and WindowPreference Exists
		if mc.window('winRename',exists = 1):
			mc.deleteUI('winRename',window = 1)
		if mc.windowPref('winRename',exists = 1):
			mc.windowPref('winRename',remove = True)
			
		#Main window and Menu Creation
		win = mc.window('winRename',t = "ReNamingTool",menuBar  = True ,s = 0 ,wh = (360,486))
		mc.menu(label = "File")
		mc.menuItem(label = "New",c = lambda event:self.mainUI_RNT())
		mc.menuItem(label = "Close",c = "renamingTool.mc.deleteUI('winRename',window = 1)")
		mc.menu(label = "Help")
		mc.menuItem(label = "Help.." ,c = lambda event:self.NamingToolHelp())
		mc.menuItem(label = "About",c = lambda event:self.NamingToolAbout())
		mc.columnLayout('maincolmlay')
		mc.separator(h = 10 , style = 'none')
		
		#Selection Option and Type
		mc.rowLayout('RL_OPnTY',nc = 5,cw5 = [65,70,45,100,70], ct5 = ["both", "both" , "both" , "both", "both"] , co5 = [1 , 1 , 2 , 2 , 2])
		mc.text(l='  Rename :', fn='boldLabelFont')
		self.ren_Dic['renRBG'] = mc.radioButtonGrp(numberOfRadioButtons=3 ,vr = 1,labelArray3=['Selected', 'Hierarchy',' All '] , sl = 1)
		mc.text(l='Type :',fn='boldLabelFont')
		mc.columnLayout(rs = 10, co = ['both' , 1])
		self.ren_Dic['typeOPM'] = mc.optionMenu( 'nOptionMenu_01')
		self.objtype = ("All","Joint", "IkHandle" ,"Transform","Locator","Geometry","Polygon","NurbsSurface","SubDivision","NurbsCurve","Cluster","Lattice","Particle")
		for objname in self.objtype:
			mc.menuItem((objname + "mode"),to = 1, label = objname)
		mc.setParent('..')
		mc.button('objBTN',l = " ObjectsInfo", w = 18, h = 35,al = 'center',ann = "Click Here to Get Target Objects Information", c =lambda event:self.selectionpro(1))
		mc.setParent('..')
		
		#Enter Name , start and Padding for Renaming
		mc.separator(w = 375 , h = 20 , style = 'double')
		mc.rowLayout(nc = 2,cw2 = [294,56], ct2 = ["both", "both"] , co2 = [2 , 1])
		self.ren_Dic['mainTFG'] = mc.textFieldGrp('maintfg',label = 'Enter Name -->', cw2 = [87,200])
		mc.button('getnameBTN' , l = 'GetName' ,w = 56, h = 25,ann = "Click Here to Get Current Object Name", c = lambda event:self.getname())
		mc.setParent('..')
		mc.separator(w = 375 , h = 10 , style = 'none')
		mc.rowLayout(nc = 4,cw4 = [75,75,77,75], ct4 = ["both", "both" , "both" , "both"] , co4 = [5 , 5 , 5 , 5])
		mc.text(l='      Start # -->')
		self.ren_Dic['strtIF'] = mc.intField(min = 0)
		mc.text(l=' Padding # -->')
		self.ren_Dic['padIF'] = mc.intField('padIF',min = 0,ed = 0,ann = "Right Click Here")
		mc.popupMenu()
		for i in range(10):
		 mc.menuItem(('menuitempadIF%d' % i),l = i ,c = "renamingTool.mc.intField(\'padIF\' ,e = 1, v =  %d" % i + ")" )	
		mc.setParent('..')
		
		mc.separator(w = 375 , h = 10 , style = 'none')
		mc.button('renBTN' , l = 'Rename' ,w = 350, h = 25, c = lambda event:self.renamepro())
		mc.separator(w = 375 , h = 20 , style = 'in')
		
		#Suffix and Prefix
		mc.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 175), (2, 175)],co = [(1 , "left" , 2.5), (2 , "left" , 5)] )
		prefsuf = ("Left" , "Right" , "L" , "R" , "Center" , "Geo" , "Jnt")
		mc.text(l='Prefix*',al = 'center', fn = "tinyBoldLabelFont")
		mc.text(l='*Suffix',al = 'center',fn = "tinyBoldLabelFont")
		
		self.ren_Dic['prefixTF'] = mc.textField('prefixtf', h = 25,ann = "Right Click Here")
		mc.popupMenu()
		for objpref in prefsuf:
				mc.menuItem((objpref + 'pre'),l = (objpref + "*") ,c = "renamingTool.mc.textField(\'prefixtf\' ,e = 1, tx = \""+objpref+"\")" )	
		
		self.ren_Dic['suffixTF'] = mc.textField('suffixtf',ann = "Right Click Here")
		mc.popupMenu()
		for objsuf in prefsuf:
				mc.menuItem((objsuf + 'pre'),l = ("*" + objsuf) ,c = "renamingTool.mc.textField(\'suffixtf\' ,e = 1, tx = \""+objsuf+"\")" )	
		
		mc.separator(h = 10 , style = 'none')
		mc.separator(style = 'none')
		mc.button('prefixBTN' , l = 'Add Prefix' ,w = 350, h = 25 , al = 'center',c = lambda event:self.sufpref(0))
		mc.button('suffixBTN' , l = 'Add Suffix' ,w = 350, h = 25 , al = 'center',c = lambda event:self.sufpref(1))
		mc.setParent("..")
		mc.separator(w = 375 , h = 20 , style = 'in')
		
		#Search and Replace
		mc.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 175), (2, 175)],co = [(1 , "left" , 2.5), (2 , "left" , 5)] )
		searchleft = ("Left" , "L" , "Lt" , "L_" , "_L")
		searchright = ("Right" , "R" , "Rt" , "R_" ,"_R")
		sizesearch = len(searchleft)
		mc.text(l='Search For',al = 'center')
		mc.text(l='Replace With',al = 'center')
		self.ren_Dic['searchTF'] = mc.textField('searchtf', h = 25,ann = "Right Click Here")
		mc.popupMenu()
		for i in range(0,sizesearch,1):
			mc.menuItem((searchleft[i] + "srch"),l = searchleft[i] ,c = "renamingTool.mc.textField(\'searchtf\' ,e = 1, tx = \""+searchleft[i]+"\");renamingTool.mc.textField(\'replacetf\' ,e = 1, tx = \""+searchright[i]+"\")")
			mc.menuItem((searchright[i] + "srch"),l = searchright[i] ,c = "renamingTool.mc.textField(\'replacetf\' ,e = 1, tx = \""+searchleft[i]+"\");renamingTool.mc.textField(\'searchtf\' ,e = 1, tx = \""+searchright[i]+"\")")
		self.ren_Dic['replaceTF'] = mc.textField('replacetf', h = 25)
		mc.setParent("..")
		mc.separator(h = 5 , style = 'none')
		mc.button('serNrepBTN' , l = "<<----- Search 'n' Replace ----->>" ,w = 352, h = 25 , al = 'center',c = lambda event:self.SearchnReplace())
		mc.separator(w = 375 , h = 15 , style = 'double')
		
		#Extra Buttons
		mc.rowColumnLayout(numberOfColumns=4, columnWidth=[(1, 87), (2, 87),(3,87),(4,90)] )
		mc.button('lowerBTN' , l = "To Lower" ,w = 352 ,h = 30, al = 'center',ann = "Click Here to convert to Lower Case", c = lambda event:self.stringfunctions(0))
		mc.button('upperBTN' , l = "To Upper" ,w = 352 , al = 'center',ann = "Click Here to convert to Upper Case", c = lambda event:self.stringfunctions(1))
		mc.button('CapBTN' , l = "Capitilize" ,w = 352 , al = 'center',ann = "Click Here to Capitilize", c = lambda event:self.stringfunctions(2))
		mc.button('ResetBTN' , l = "Reset All" ,w = 352, al = 'center', c = lambda event:self.mainUI_RNT())
		mc.button('FDNBTN' , l = "FindDupliName" ,w = 352,h = 30, al = 'center',ann = "Click Here to Find Duplicate Names", c = lambda event:self.multiplenames(0))
		mc.button('CDNBTN' , l = "CrtDupliName" ,w = 352, al = 'center',ann = "Click Here to Correct Duplicate Names", c = lambda event:self.multiplenames(1))
		mc.button('shpnameBTN' , l = "CrtShapeName" ,w = 352,  al = 'center',ann = "Click Here to Correct Shape Names",c = lambda event:self.correctshape())
		mc.button('CloseBTN' , l = "Close" ,w = 352,  al = 'center', c = "renamingTool.mc.deleteUI('winRename',window = 1)")
		mc.setParent('..')
		mc.separator(w = 375,h = 10 , style = 'in')
		mc.showWindow(win)

####################################################################################
	#Common Selection Def Based On Type Of Object and Mode Of Selection 
	def selectionpro(self,ret):
		# query selection Mode and objects type
		selType = mc.radioButtonGrp((self.ren_Dic['renRBG']),q = True, sl = 1)		
		geobjType = mc.optionMenu((self.ren_Dic['typeOPM']) , q = 1, v = 1)			
		objType = string.lower(geobjType[:1]) + geobjType[1:]
		selectobjs = mc .ls(sl = True,long = True)																						
		try:
			returnobjarray = []
			objarray = [""]
			#Heiracy selection
			if selType == 2:																												
				objarray = mc.ls(tr = True , sl = True,l = True,dag = True)
			#select all Objects
			elif selType == 3:																											
			 objarray = mc.ls(tr= 1,l = True,dag = True)
			 removwcam = ['|persp','|top','|front','|side']
			 for obj in removwcam:
			 	objarray.remove(obj)
			else:
				objarray = selectobjs	
			if ret == 1:
				switch = 0
				for obj in objarray:
					shrtname = mm.eval('shortNameOf("%s")' % obj)
					if "|" in shrtname:
						switch = 1
						pass
				if switch == 1:
					mc.confirmDialog( title='DuplicateNames', message= "Duplicate Names are Found ! \n Correct it for Proper Renaming.." , button=['OK'])
			#Checking object Types
			if objType != "all":																									
					sizearray = len(objarray)
					for i in range (0,sizearray):
						node = mc.nodeType(objarray[i])
						try:
							objshape = mc.listRelatives(objarray[i], s = 1,pa = 1)
							if node == 'transform' and objshape != None:
								objshapenode = mc.nodeType(objshape[0])
								if objType == 'geometry' and (objshapenode == 'mesh'or objshapenode =='nurbssurface' or objshapenode == 'subdiv'):
									returnobjarray.append(objarray[i])	
								elif objType == 'polygon' and objshapenode == 'mesh':
									returnobjarray.append(objarray[i])
								elif objType == 'nurbsSurface' and objshapenode == 'nurbsurface':
									returnobjarray.append(objarray[i])
								elif objType == 'subDivision' and objshapenode == 'subdiv':
									returnobjarray.append(objarray[i])
								elif objType == 'nurbsCurve' and objshapenode == 'nurbsCurve':
									returnobjarray.append(objarray[i])
								elif objType == 'cluster' and objshapenode == 'clusterHandle':
									returnobjarray.append(objarray[i])
								elif objType == objshapenode:
									returnobjarray.append(objarray[i])
							elif node == objType:
								returnobjarray.append(objarray[i])
						except TypeError:
							pass
			else:
				returnobjarray = objarray
			#Error if no objects are selected
			if (len(returnobjarray)) == 0 or returnobjarray == [''] :
				self.errorMsg('No Objects are Found..')
			else:
			#Return the objects name
				if ret == 1:
					if mc.window('winRenametarget',exists = 1):
 						mc.deleteUI('winRenametarget',window = 1)
					if mc.windowPref('winRenametarget',exists = 1):
 						mc.windowPref('winRenametarget',remove = True)
					wintargt = mc.window('winRenametarget',t = "Target Objects List",tlb = 1 ,s = 0,w = 210 )
					mc.rowColumnLayout(cw = [1, 200])
					tslTarget = mc.textScrollList ('tslTarget',ams = 1,h = 250,shi = 1,nr = 8, sc = "renamingTool.mc.select(renamingTool.mc.textScrollList('tslTarget',q = True,si = True))")
					for obj in returnobjarray:
 						mc.textScrollList (tslTarget,e = 1,a = obj)
					mc.button(label = "CloseWindow",c = "mc.deleteUI('winRenametarget',window = 1)")
					mc.showWindow('winRenametarget')
		except TypeError:
			self.errorMsg("No Objects Are Selected.....")
		return returnobjarray

####################################################################################
	# def for loading a selected object name
	def getname(self):
		selectobjs = mc .ls(sl = True)
		if (len(selectobjs)) >= 1:
			mc.textFieldGrp(self.ren_Dic['mainTFG'] ,e = 1 , text = selectobjs[0])
		else:
			self.errorMsg("Select a Object To Add Name..")
			
####################################################################################
	#def for renaming objects 		
	def renamepro(self):
		#get objects
		inObj = self.selectionpro(0)
		sizeobjarray = len(inObj)
		#query inputs
		queryobjname = mc.textFieldGrp(self.ren_Dic['mainTFG'],q = 1, text = True)
		querystartno = mc.intField(self.ren_Dic['strtIF'],q = 1,v = True)
		querypadding = mc.intField(self.ren_Dic['padIF'],q = 1,v = True)
		for i in range (0 , sizeobjarray):
			try:
				#Add padding
				if queryobjname != "":
					addpad = querypadding + 1 
					startno = querystartno + i
					padno = ("%%0%d" % addpad + ".0f") % startno
					newobjname = queryobjname + padno
					print inObj[i]
					mc.rename (self.selectionpro(0)[i] , newobjname)
					#inObj = self.selectionpro(0)
				else:
					self.errorMsg("Enter a Name To Rename..")
			except TypeError:
							self.errorMsg("No objects are Found")
							
####################################################################################
	#def for adding suffuix r prefix
	def sufpref(self,mode):
	 inObj = self.selectionpro(0)
	 #query inputs
	 queryprefix = mc.textField(self.ren_Dic['prefixTF'],q = 1,text = True)
	 querysufix = mc.textField(self.ren_Dic['suffixTF'],q = 1,text = True)
	 if mode == 0 and queryprefix == "":
		self.errorMsg("Enter a Prefix..")
	 elif mode == 1 and querysufix == "":
		self.errorMsg("Enter a Suffix..")
	 #rename objects with suffix r prefix
	 for i in range (len(inObj)):
	 	tmpshrtname = inObj[i].split('|')
 		shrtname =  tmpshrtname[len(tmpshrtname)-1]
		if mode == 0:
		 mc.rename(inObj[i] , (queryprefix + shrtname))
		else:
		 mc.rename(inObj[i] , (shrtname + querysufix))
		inObj = self.selectionpro(0)
		 
 
####################################################################################
	#def for search n replace name
	def SearchnReplace(self):
		inObj = self.selectionpro(0)
		#query inputs
		querysearch = mc.textField(self.ren_Dic['searchTF'],q = 1,text = True)
		queryreplace = mc.textField(self.ren_Dic['replaceTF'],q = 1,text = True)
		if querysearch == "":
		 self.errorMsg('Enter a Name to Replace..')
		else:
		 for i in range(len(inObj)):
	 		tmpshrtname = inObj[i].split('|')
 			shrtname =  tmpshrtname[len(tmpshrtname)-1]
			newname = shrtname.replace(querysearch , queryreplace)
			mc.rename(inObj[i] , newname)
			inObj = self.selectionpro(0)
		  
####################################################################################
  #def for extra functions
	def stringfunctions(self,method):
		inObj = self.selectionpro(0)
		for i in range (len(inObj)):
			tmpshrtname = inObj[i].split('|')
 			shrtname =  tmpshrtname[len(tmpshrtname)-1]
			if method == 0: #to uppercase
				newname = shrtname.lower()
			if method == 1: #to lowercase
				newname = shrtname.upper()
			if method == 2: #Capilitize string
				newname = shrtname.capitalize()
			mc.rename(inObj[i] , newname)
			inObj = self.selectionpro(0)
			
####################################################################################
	#def for correcting shape name
	def correctshape(self):
		inObj = self.selectionpro(0)
		for i in range(len(inObj)):
			try:
				tmpshrtname = inObj[i].split('|')
 				shrtname =  tmpshrtname[len(tmpshrtname)-1]
				shapesname = mc.listRelatives(inObj[i], pa = 1 , s = 1)
				no = ""
				for j in range (len(shapesname)):
					if (mc.referenceQuery(shapesname[j], inr = True ) ==  1) or (mc.lockNode(shapesname[j], q = 1, l = 1) == [1]):
						pass
					else:
						newname = (shrtname + "Shape%s" % no)
						mc.rename(shapesname[j] , newname) 
						no = str(i + 1)
						inObj = self.selectionpro(0)
			except TypeError , RuntimeError:
				pass

####################################################################################
	#def for finding and resolving multiple namespace
	def multiplenames(self,mode):
		inObj = self.selectionpro(0)
		n = 0
		multinames = []
		for i in range (len(inObj)):
			shrtname = mm.eval('shortNameOf("%s")' % inObj[i])
			if "|" in shrtname:
				multinames.append(inObj[i])
				if mode == 1:
					newname = inObj[i].split("|")
					mc.rename(inObj[i] , newname[len(newname) - 1] + "_%d" % n)
					n = n + 1
					inObj = self.selectionpro(0)
		if mode == 0:
			objects = ""
			if len(multinames) >= 1:
				for obj in multinames:
						objects = objects + (obj+"\n")
				msg =  "The Following objects are found with Same Name:\n\n%s" % objects
			else:
				msg = "No Duplicate Names are Found.."
			mc.confirmDialog( title='DuplicateName', message= msg , button=['OK'])
  			
####################################################################################
	#Error Return
	def errorMsg(self,msg):		
		raise Exception(msg)

####################################################################################
	#Details about Naming Tool.
	def NamingToolAbout(self):
		if mc.window('winRenameabout',exists = 1):
			mc.deleteUI('winRenameabout',window = 1)
		if mc.windowPref('winRenameabout',exists = 1):
			mc.windowPref('winRenameabout',remove = True)
		win = mc.window('winRenameabout',t = "ReNamingTool 1.00 About",tlb = 1 ,s = 0 ,wh = (225,212))
 		mc.columnLayout()
 		mc.separator(h = 10 , style = 'none')
 		mc.rowColumnLayout(nc = 2 ,cw  = [(1, 125) , (2,125)] , cal = [2 , 'left'])
		mc.text(label = "   Title               :",font = "boldLabelFont")
		mc.text(label = "renamingTool.py")
		mc.text(label = "   Version           : ",font = "boldLabelFont")
		mc.text(label = "1.00")
		mc.text(label = "   Author            : ",font = "boldLabelFont")
		mc.text(label = "Arun.S")
		mc.text(label = "  Created           :",font = "boldLabelFont")
		mc.text(label = "March 2009")
		mc.text(label = " Last Updated    :",font = "boldLabelFont")
		mc.text(label = "02 . April . 2009")
		mc.setParent('..')
		mc.separator(h = 25,w = 225 , style = 'double')
		mc.text(label = "     Send Comments and Suggestions to")
		mc.text(label = "              arunpillaii@gmail.com      ",font = "boldLabelFont", h = 25)
		mc.button(l = "Close Window", c = "renamingTool.mc.deleteUI('winRenameabout',window = 1)",w = 217)
		mc.showWindow('winRenameabout')
		
####################################################################################
	#Tool Help Window
	def NamingToolHelp(self):
		if mc.window('winRenamehelp',exists = 1):
			mc.deleteUI('winRenamehelp',window = 1)
		if mc.windowPref('winRenamehelp',exists = 1):
			mc.windowPref('winRenamehelp',remove = True)
		win = mc.window('winRenamehelp',t = "ReNamingTool 1.00 Help",tlb = 1 ,s = 0 ,wh = (300,212))
 		mc.scrollLayout('scrLay',hst = 0)
 		mc.columnLayout()
 		mc.separator(h = 10 , style = 'none')
 		texthelp = """********About Tool********\n
    This tool is used for renaming related tasks in maya.
----------------------------------------------------------
Selection Method\n
Three types of selection are there for renaming.
' Selected '  ->    Selected Objects 
' Heirarchy ' ->    Selected Objects Heirarchy
' All '     ->    All objects in the Scene
----------------------------------------------------------
Type\n
 Type is used to select the type of objects.
so rename will affect that type of objects only.
----------------------------------------------------------
ObjectInfo\n
It returns the name of target objects 
----------------------------------------------------------
Rename\n
Rename with entered starting number and Padding.
Right Click on padding menu to get more.
----------------------------------------------------------
Prefix and Suffix\n
Adding entered siffix and prefix.Right click in the
menu to get some common used prefix and suffix.
----------------------------------------------------------
Search and Replace\n
This will search the entered name and replace
with new name.Right click in the menu to get
some common used names.
----------------------------------------------------------
Extra Buttons\n
'To Lower' - Convert name to Lower Caps
'To Upper' - Convert name to Upper Case
'Capitilize' - First Letter is Upper and others are small
"""
 		mc.text(label = texthelp)
		mc.showWindow('winRenamehelp')

##=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*##


cls = mainClassRNT()
cls.mainUI_RNT()