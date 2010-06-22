remake_add_library(dtoolinterrogatedb *.cxx LINK dtoolconfig dtoolbase dtoolprc
  ${PYTHON_LIBRARIES})
remake_add_headers(*.h *.I *.T)
