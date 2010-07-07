remake_add_generated(FLEX egg *.lxx LANG CXX PREFIX eggyy IGNORE_CASE)
remake_add_generated(BISON egg *.yxx LANG CXX PREFIX eggyy HEADERS)

panda3d_interrogate(egg)

remake_add_library(egg *.cxx LINK linmath)
remake_add_headers(*.h *.I *.T)
