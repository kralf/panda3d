panda3d_interrogate(collide MODULE panda)

remake_add_library(collide *.cxx LINK tform device pgraph)
remake_add_headers(*.h *.I *.T)
