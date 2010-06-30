remake_add_generated(BISON cppparser *.yxx LANG CXX PREFIX cppyy HEADERS)

remake_add_library(cppparser *.cxx)
remake_add_headers(*.h *.I *.T)
