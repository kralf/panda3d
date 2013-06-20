panda3d_interrogate_module(panda MODULE panda)

remake_add_library(panda *.cxx FORCE_LINK recorder pgraph pgraphnodes
  pipeline grutil chan pstatclient char collide cull device dgraph display
  event framework gobj gsgbase linmath mathutil movies net nativenet
  parametrics pgraph pnmimagetypes pnmimage pnmtext text tform lerp putil
  audio pgui pbase panda_express)
remake_add_headers(*.h *.I *.T)
