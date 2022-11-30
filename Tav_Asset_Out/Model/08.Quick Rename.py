import maya.cmds as cmds
import maya.mel as mel

def quickrename(*args):
    FNME = "Quick_rename_tool.mel"
    abc = mel.eval('getenv("PYTHONPATH")')
    abc = abc.split(";")
    for ech in abc:
        melf  = os.path.join(ech,"tools","tavext","model",FNME).replace("\\","/")
        if os.path.isfile(melf):
            mel.eval('source "'+melf+'"')
            mel.eval('Quick_rename_tool()')
            break
    
quickrename()