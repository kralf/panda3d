panda3d_interrogate(mathutil MODULE panda)

remake_add_library(mathutil *.cxx LINK linmath putil event)
remake_add_headers(*.h *.I *.T)
