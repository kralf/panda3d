remake_find_package(ZLIB)

remake_add_library(express *.cxx LINK base ${ZLIB_LIBRARIES})
remake_add_headers(*.h *.I *.T)
