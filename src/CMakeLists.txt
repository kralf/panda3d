remake_find_package(ZLIB)
remake_find_package(openssl CONFIG)
remake_find_package(freetype2 CONFIG)
remake_find_package(PythonLibs)

remake_include(${FREETYPE2_INCLUDE_DIRS} ${PYTHON_INCLUDE_PATH})

#remake_project_header(config.h.remake)
remake_include()

remake_add_directories(lib)
remake_add_directories(bin)
  