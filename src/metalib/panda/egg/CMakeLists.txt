panda3d_interrogate_module(panda_egg MODULE pandaegg)

remake_add_library(panda_egg *.cxx LINK egg2pg egg panda)
remake_add_headers(*.h *.I *.T)
