panda3d_interrogate(pstatclient MODULE panda)

remake_add_library(pstatclient *.cxx LINK dtool dtool_config putil net)
remake_add_headers(*.h *.I *.T)
