remake_include(${CMAKE_CURRENT_BINARY_DIR})

remake_add_library(vrmlegg *.cxx LINK vrml eggbase converter)
remake_add_headers(*.h *.I *.T)
