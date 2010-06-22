remake_find_library(dl dlfcn.h)

remake_add_library(dtoolutil *.cxx LINK dtoolbase ${DL_LIBRARY})
remake_add_headers(*.h *.I *.T)
