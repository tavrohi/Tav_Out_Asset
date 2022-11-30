import maya.cmds as cmds
import maya.mel as mel

def nsided(*args):
    FNME = "highlightNgons.mel"
    abc = mel.eval('getenv("PYTHONPATH")')
    abc = abc.split(";")
    for ech in abc:
        melf  = os.path.join(ech,"tools","tavext","model",FNME).replace("\\","/")
        if os.path.isfile(melf):
            mel.eval('source "'+melf+'"')
            break
    
nsided()