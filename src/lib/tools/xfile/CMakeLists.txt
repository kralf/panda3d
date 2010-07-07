remake_add_generated(FLEX xfile *.lxx LANG CXX PREFIX xyy IGNORE_CASE)
remake_add_generated(BISON xfile *.yxx LANG CXX PREFIX xyy HEADERS)

remake_add_library(xfile *.cxx LINK tbase)
remake_add_headers(*.h *.I *.T)
