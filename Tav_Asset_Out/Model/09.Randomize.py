import maya.cmds as cmds
import maya.mel as mel

def random(*args):
    FNME = "RandomGeom.mel"
    abc = mel.eval('getenv("PYTHONPATH")')
    abc = abc.split(";")
    for ech in abc:
        melf  = os.path.join(ech,"tools","tavext","model",FNME).replace("\\","/")
        if os.path.isfile(melf):
            mel.eval('source "'+melf+'"')
            break
    
random()