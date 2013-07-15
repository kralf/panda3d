panda3d_interrogate_include(${BULLET_HEADERS})
panda3d_interrogate(pbullet MODULE pandabullet)

remake_add_library(pbullet *.cxx LINK express ${BULLET_LIBRARY})
remake_add_headers(*.h *.I *.T)
