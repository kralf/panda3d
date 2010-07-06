remake_add_library(panda *.cxx LINK recorder pgraph pgraphnodes pipeline   
  grutil chan pstatclient char collide cull device dgraph display event
  framework gobj gsgbase linmath mathutil movies net nativenet parametrics
  pnmimagetypes pnmimage pnmtext text tform lerp putil audio pgui pbase)
remake_add_headers(*.h *.I *.T)
