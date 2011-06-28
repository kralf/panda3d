panda3d_interrogate_module(panda MODULE panda)

remake_set(LINK_LIBRARIES ${GL_LIBRARIES})
if(CG_FOUND AND CGGL_FOUND)
  remake_list_push(LINK_LIBRARIES ${CG_LIBRARY} ${CGGL_LIBRARY})
endif(CG_FOUND AND CGGL_FOUND)

remake_add_library(panda *.cxx LINK recorder pgraph pgraphnodes pipeline
  grutil chan pstatclient char collide cull device dgraph display event
  framework gobj gsgbase linmath mathutil movies net nativenet parametrics
  pgraph pnmimagetypes pnmimage pnmtext text tform lerp putil audio pgui
  pbase panda_express ${LINK_LIBRARIES})
remake_add_headers(*.h *.I *.T)
