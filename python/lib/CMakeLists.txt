remake_add_directories()

remake_python_package_name(DEFAULT_PACKAGE
  ${REMAKE_PYTHON_COMPONENT_SUFFIX})
remake_python_package_name(CONFIG_PACKAGE config)
remake_python_package_name(DIRECT_PACKAGE direct)
remake_python_distribute(PACKAGES ${DEFAULT_PACKAGE} ${CONFIG_PACKAGE}
  ${DIRECT_PACKAGE})
