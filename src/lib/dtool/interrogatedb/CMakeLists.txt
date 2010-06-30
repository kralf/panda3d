remake_add_library(interrogatedb *.cxx LINK dconfig dbase prc
  ${PYTHON_LIBRARIES})
remake_add_headers(*.h *.I *.T)
