panda3d_interrogate_include(${ODE_HEADERS}/..)
panda3d_interrogate(pode MODULE pandaode)

remake_add_library(pode *.cxx LINK express ${ODE_LIBRARY})
remake_add_headers(*.h *.I *.T)
