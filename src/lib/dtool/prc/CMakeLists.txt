remake_add_library(dtoolprc *.cxx LINK dtoolutil dtoolbase ${OPENSSL_LIBRARIES})
remake_add_headers(*.h *.I *.T)
