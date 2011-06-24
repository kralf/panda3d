panda3d_interrogate(pipeline MODULE panda)

remake_add_library(pipeline *.cxx LINK express pbase)
remake_add_headers(*.h *.I *.T)
