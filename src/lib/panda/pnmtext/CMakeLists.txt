panda3d_interrogate(pnmtext MODULE panda)

remake_add_library(pnmtext *.cxx LINK ${FREETYPE2_LIBRARIES})
remake_add_headers(*.h *.I *.T)
