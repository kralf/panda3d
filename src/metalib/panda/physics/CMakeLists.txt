panda3d_interrogate_module(panda_physics MODULE pandaphysics)

remake_add_library(panda_physics *.cxx LINK physics particlesystem
  panda_express)
remake_add_headers(*.h *.I *.T)
