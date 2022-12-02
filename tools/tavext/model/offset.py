from maya import cmds as cmds

windowName="offsetter"
itemsOrigPos={}

if (cmds.window(windowName, exists=True)):
	cmds.deleteUI(windowName,window=True)
	
window=cmds.window(windowName,title="Offsetter", width=303, height=180, sizeable=False)

cmds.columnLayout("columnLayoutName01", adjustableColumn = True) 
cmds.text( "stepValueText", label = "Set step value", parent = "columnLayoutName01")
cmds.floatField( "floatFieldName", minValue = -100, maxValue = 100, precision = 4, value = 1, parent = "columnLayoutName01")
cmds.button("reset",label="reset", width=100, height=30,command=lambda x:offset("reset"),backgroundColor = [0.75294,0.75686,0.46275])
cmds.button("update",label="update last position", width=100, height=30,command=lambda x:offset("update"),backgroundColor =[0.96078,0.20784,0.20784])



cmds.gridLayout("layout", columnsResizable=True,cellWidthHeight=(100, 100), width=300, height=200)
#make buttons
cmds.button("moveXUP",label="move X+", width=100, height=100, parent="layout",command=lambda x:offset("X+"))
cmds.button("moveYUP",label="move Y+", width=100, height=100, parent="layout",command=lambda x:offset("Y+"))
cmds.button("moveZUP",label="move Z+", width=100, height=100, parent="layout",command=lambda x:offset("Z+"))
cmds.button("moveXDOWN",label="move X-", width=100, height=100, parent="layout",command=lambda x:offset("X-"))
cmds.button("moveYDOWN",label="move Y-", width=100, height=100, parent="layout",command=lambda x:offset("Y-"))
cmds.button("moveZDOWN",label="move Z-", width=100, height=100, parent="layout",command=lambda x:offset("Z-"))




cmds.showWindow(window)

def offset(axis):
	obj = cmds.ls(selection=True)[0]
	if obj not in itemsOrigPos:
		itemsOrigPos[obj]=cmds.xform(obj, translation=True, os=True, q=True)
	stepValue=cmds.floatField("floatFieldName", query=True, value=True)
	values=[0,0,0]
	if axis=="X+":
		values=[stepValue,0,0]
	if axis=="X-":
		values=[-1*stepValue,0,0]
	if axis=="Y+":
		values=[0,stepValue,0]
	if axis=="Y-":
		values=[0,-1*stepValue,0]
	if axis=="Z+":
		values=[0,0,stepValue]
	if axis=="Z-":
		values=[0,0,-1*stepValue]	
	cmds.move(values[0],values[1],values[2],obj, relative=True)
	if axis=="reset":
		try:
			currentPos=cmds.xform(obj, translation=True, os=True, q=True)
			if itemsOrigPos.get(obj)!=currentPos:
				cmds.move(itemsOrigPos.get(obj)[0],itemsOrigPos.get(obj)[1],itemsOrigPos.get(obj)[2],obj)
		except Exception, e:
			print e	
	if axis=="update":
		if obj in itemsOrigPos:
			itemsOrigPos[obj]=cmds.xform(obj, translation=True, ws=True, q=True)
			print "new stored position is {0}".format(itemsOrigPos[obj])
	