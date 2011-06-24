panda3d_interrogate(gsgbase MODULE panda)

remake_add_library(gsgbase *.cxx LINK express putil)
remake_add_headers(*.h *.I *.T)
