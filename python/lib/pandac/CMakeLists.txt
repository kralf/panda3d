remake_set(PANDA3D_PYTHON_PATH ${REMAKE_PYTHON_BINARY_DIR}/lib)
remake_set(PANDA3D_EXPRESS_PATH
  ${REMAKE_PROJECT_BINARY_DIR}/metalib/panda/express)

panda3d_python_package(${REMAKE_PYTHON_SOURCE_DIR}/bin/direct/gen_pycode
  NAME panda3d.pandac PATH ${PANDA3D_PYTHON_PATH} ${PANDA3D_EXPRESS_PATH})
remake_python_distribute(NAME panda3d.pandac PACKAGES panda3d.pandac
  DESCRIPTION "Python bindings")
