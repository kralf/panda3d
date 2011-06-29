remake_add_generated(BISON cppparse *.yxx LANG CXX PREFIX cppyy HEADERS)

remake_add_library(cppparse *.cxx)
remake_add_headers(*.h *.I *.T)

remake_add_directories(parser-inc)
