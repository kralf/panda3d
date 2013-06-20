panda3d_interrogate(gobj MODULE panda)

if(CG_FOUND AND CGGL_FOUND)
  remake_set(LINK_LIBRARIES ${CG_LIBRARY} ${CGGL_LIBRARY} ${GL_LIBRARIES})
else(CG_FOUND AND CGGL_FOUND)
  remake_unset(LINK_LIBRARIES)
endif(CG_FOUND AND CGGL_FOUND)

remake_add_library(gobj *.cxx LINK event mathutil pnmimage gsgbase
  ${LINK_LIBRARIES})
remake_add_headers(*.h *.I *.T)
