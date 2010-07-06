remake_find_package(ZLIB)
remake_find_package(openssl CONFIG)
remake_find_package(freetype2 CONFIG)
remake_find_package(JPEG)
remake_find_package(PNG)
remake_find_package(TIFF)
remake_find_library(ode ode.h)
remake_find_package(gl CONFIG)
remake_find_package(PythonLibs)

remake_include(
  ${FREETYPE2_INCLUDE_DIRS}
  ${GL_INCLUDE_DIRS}
  ${PYTHON_INCLUDE_PATH}
)

remake_project_get(CONFIGURATION_DESTINATION DESTINATION)
#remake_project_header(config.h.remake)
remake_include()

remake_add_directories(lib)
remake_add_directories(metalib)
remake_add_directories(bin)
