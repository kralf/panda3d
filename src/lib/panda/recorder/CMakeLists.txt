panda3d_interrogate(recorder MODULE panda)

remake_add_library(recorder *.cxx LINK dgraph downloader)
remake_add_headers(*.h *.I *.T)
