panda3d_interrogate_module(panda_ode MODULE pandaode)

remake_add_library(panda_ode *.cxx LINK pode panda_express)
remake_add_headers(*.h *.I *.T)
