remake_add_generated(FLEX vrml *.lxx LANG CXX PREFIX vrmlyy IGNORE_CASE)
remake_add_generated(BISON vrml *.yxx LANG CXX PREFIX vrmlyy HEADERS)

remake_add_library(vrml *.cxx LINK tbase)
remake_add_headers(*.h *.I *.T)
