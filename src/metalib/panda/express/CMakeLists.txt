panda3d_interrogate_module(panda_express MODULE pandaexpress)

remake_add_library(panda_express *.cxx FORCE_LINK downloader express)
remake_add_headers(*.h *.I *.T)
