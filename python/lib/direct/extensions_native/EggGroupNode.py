from panda3d.direct.extensions_native.Helpers import *
Dtool_PreloadDLL("panda_egg")
from panda_egg import *

####################################################################
#Dtool_funcToMethod(func, class)        
#del func
#####################################################################
    # For iterating over children
def getChildren(self):
        """Returns a Python list of the egg node's children."""
        result = []
        child = self.getFirstChild()
        while (child != None):
            result.append(child)
            child = self.getNextChild()
        return result
    
Dtool_funcToMethod(getChildren, EggGroupNode)        
del getChildren
