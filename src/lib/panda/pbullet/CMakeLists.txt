panda3d_interrogate_include(parser-inc ${BULLET_HEADERS})
panda3d_interrogate(pbullet MODULE pandabullet)

remake_add_library(pbullet *.cxx LINK express ${BULLET_LIBRARIES})
remake_add_headers(*.h *.I *.T)

remake_add_directories(parser-inc)