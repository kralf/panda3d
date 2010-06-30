remake_find_library(dl dlfcn.h)

remake_add_library(dutil *.cxx LINK dbase ${DL_LIBRARY})
remake_add_headers(*.h *.I *.T)
