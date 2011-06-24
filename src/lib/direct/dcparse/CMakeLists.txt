remake_add_generated(FLEX dcparse *.lxx LANG CXX PREFIX dcyy)
remake_add_generated(BISON dcparse *.yxx LANG CXX PREFIX dcyy HEADERS)

panda3d_interrogate(dcparse MODULE p3direct)

remake_add_library(dcparse *.cxx LINK panda)
remake_add_headers(*.h *.I *.T)
