from panda3d.direct.extensions_native.Helpers import *
Dtool_PreloadDLL("panda_egg")
from panda_egg import *

####################################################################
#Dtool_funcToMethod(func, class)        
#del func
#####################################################################
    # For iterating over vertices
def getVertices(self):
        """Returns a Python list of the egg primitive's vertices."""
        result = []
        for i in range(self.getNumVertices()):
            result.append(self.getVertex(i))
        return result
Dtool_funcToMethod(getVertices, EggPrimitive)        
del getVertices
