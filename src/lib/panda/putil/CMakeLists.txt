panda3d_interrogate(putil)

remake_add_library(putil *.cxx LINK pipeline express pbase)
remake_add_headers(*.h *.I *.T)
