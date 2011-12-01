remake_project_set(BLENDER_FILE_DESTINATION
  ${CMAKE_INSTALL_PREFIX}/share/blender/bpydata
  CACHE STRING "Install destination of project Blender files.")

remake_project_get(BLENDER_FILE_DESTINATION DESTINATION)
remake_add_files(*.png RECURSE INSTALL ${BLENDER_FILE_DESTINATION})
