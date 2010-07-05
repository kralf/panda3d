panda3d_interrogate(gobj)

remake_add_library(gobj *.cxx LINK event mathutil pnmimage gsgbase)
remake_add_headers(*.h *.I *.T)
