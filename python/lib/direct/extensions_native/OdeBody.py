from panda3d.direct.extensions_native.Helpers import *
Dtool_PreloadDLL("panda")
from panda import *

####################################################################
#Dtool_funcToMethod(func, class)
#del func
#####################################################################

"""
OdeBody-extensions module: contains methods to extend functionality
of the OdeBody classe
"""

def getConvertedJoint(self, index):
    """
    Return a downcast joint on this body.
    """
    return self.getJoint(index).convert()
Dtool_funcToMethod(getConvertedJoint, OdeBody)
del getConvertedJoint

