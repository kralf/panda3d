remake_add_generated(FLEX egg *.lxx LANG CXX PREFIX eggyy)
remake_add_generated(BISON egg *.yxx LANG CXX PREFIX eggyy HEADERS)

remake_add_library(egg *.cxx LINK linmath)
remake_add_headers(*.h *.I *.T)
