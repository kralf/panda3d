remake_find_package(PythonLibs)
remake_find_package(openssl CONFIG)

remake_include(${PYTHON_INCLUDE_PATH})

#remake_project_header(config.h.remake)
remake_include()

remake_add_directories(lib)
remake_add_directories(bin)
  