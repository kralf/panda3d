panda3d_interrogate(pgui MODULE panda)

remake_add_library(pgui *.cxx LINK pgraph tform grutil)
remake_add_headers(*.h *.I *.T)
