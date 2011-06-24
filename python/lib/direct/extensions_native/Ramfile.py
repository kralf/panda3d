from panda3d.direct.extensions_native.Helpers import *
Dtool_PreloadDLL("panda_express")
from panda_express import *

"""
Ramfile_extensions module: contains methods to extend functionality
of the Ramfile class
"""

def readlines(self):
    """Reads all the lines at once and returns a list."""
    lines = []
    line = self.readline()
    while line:
        lines.append(line)
        line = self.readline()
    return lines

Dtool_funcToMethod(readlines, Ramfile)
del readlines    
