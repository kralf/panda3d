remake_file_configure(*.remake)

remake_python_package_name(CONFIG_PACKAGE config)
remake_python_package(NAME ${CONFIG_PACKAGE} DIRECTORY
  ${CMAKE_CURRENT_BINARY_DIR})
