panda3d_interrogate(mathutil)

remake_add_library(mathutil *.cxx LINK linmath putil event)
remake_add_headers(*.h *.I *.T)
