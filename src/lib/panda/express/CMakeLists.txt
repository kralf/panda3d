panda3d_interrogate(express)

remake_add_library(express *.cxx LINK pbase ${ZLIB_LIBRARIES})
remake_add_headers(*.h *.I *.T)
