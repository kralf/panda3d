panda3d_interrogate(net MODULE panda)

remake_add_library(net *.cxx LINK nativenet pipeline)
remake_add_headers(*.h *.I *.T)
