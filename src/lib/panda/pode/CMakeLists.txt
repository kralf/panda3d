panda3d_interrogate_include(${ODE_HEADERS}/..)
panda3d_interrogate(pode)

remake_add_library(pode *.cxx)
remake_add_headers(*.h *.I *.T)
