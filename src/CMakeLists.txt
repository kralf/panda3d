remake_find_package(ZLIB)
remake_find_package(openssl CONFIG)
remake_find_package(freetype2 CONFIG)
remake_find_package(JPEG)
remake_find_package(PNG)
remake_find_package(TIFF)
remake_find_library(ode ode/ode.h)
remake_find_package(bullet CONFIG)
remake_find_package(gl CONFIG)
remake_find_library(Cg Cg/cg.h PACKAGE Cg OPTIONAL)
remake_find_library(CgGL Cg/cgGL.h PACKAGE CgGL OPTIONAL)
remake_find_package(OpenAL)
remake_find_package(PythonLibs)

if(CG_FOUND)
  remake_set(HAVE_CG ON)
endif(CG_FOUND)
if(CGGL_FOUND)
  remake_set(HAVE_CGGL ON)
endif(CGGL_FOUND)

remake_include(
  ${FREETYPE2_INCLUDE_DIRS}
  ${BULLET_INCLUDE_DIRS}
  ${GL_INCLUDE_DIRS}
  ${PYTHON_INCLUDE_PATH}
)
remake_define(dDOUBLE ON)

remake_component(tools)
if(PANDA3D_TOOLS_COMPONENT_BUILD)
  remake_find_package(GTK+2 CONFIG gtk+-2.0)
endif(PANDA3D_TOOLS_COMPONENT_BUILD)

remake_project_get(CONFIGURATION_DESTINATION DESTINATION)
remake_project_header(config.h.remake INSTALL)

remake_add_directories(lib)
remake_add_directories(metalib)
remake_add_directories(bin)

remake_pkg_config_generate(COMPONENT dtool REQUIRES openssl)
remake_pkg_config_generate(REQUIRES panda3d-dtool ode bullet openal
  freetype2 libpng12 gl)
remake_pkg_config_generate(COMPONENT direct REQUIRES panda3d)
if(PANDA3D_TOOLS_COMPONENT_BUILD)
  remake_pkg_config_generate(COMPONENT tools REQUIRES panda3d gtk+-2.0)
endif(PANDA3D_TOOLS_COMPONENT_BUILD)
