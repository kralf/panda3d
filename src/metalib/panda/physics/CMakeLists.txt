panda3d_interrogate_module(panda_physics MODULE pandaphysics)

remake_add_library(panda_physics *.cxx FORCE_LINK physics particlesystem panda)
remake_add_headers(*.h *.I *.T)
