panda3d_interrogate_module(panda_bullet MODULE pandabullet)

remake_add_library(panda_bullet *.cxx FORCE_LINK pbullet panda)
remake_add_headers(*.h *.I *.T)
