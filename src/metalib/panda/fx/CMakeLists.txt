panda3d_interrogate_module(panda_fx MODULE pandafx)

remake_add_library(panda_fx *.cxx LINK distort effects panda_express)
remake_add_headers(*.h *.I *.T)
