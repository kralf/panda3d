panda3d_interrogate_module(panda_skel MODULE pandaskel)

remake_add_library(panda_skel *.cxx LINK skel panda)
remake_add_headers(*.h *.I *.T)
