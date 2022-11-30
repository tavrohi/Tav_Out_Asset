def fsmt(*args):
    from tools.tavext.model import fastpolysmooth as sd
    reload(sd)
    sd.SubdWindow().show()
    
fsmt()