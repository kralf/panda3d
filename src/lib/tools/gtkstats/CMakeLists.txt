remake_include(${GTK+2_INCLUDE_DIRS})

remake_add_library(gtkstats *.cxx LINK pstatserver ${GTK+2_LIBRARIES})
remake_add_headers(*.h *.I *.T)
