panda3d_interrogate(nativenet)

remake_add_library(nativenet *.cxx LINK express pbase dtool dtool_config)
remake_add_headers(*.h *.I *.T)
