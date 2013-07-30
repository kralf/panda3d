remake_find_executable(python)
remake_generate_custom(
  store_pixel
  ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/store_pixel.py
  TARGET tinydisplay
  SOURCES store_pixel_code.h store_pixel_table.h
)
remake_generate_custom(
  ztriangle
  ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/ztriangle.py
  TARGET tinydisplay
  SOURCES ztriangle_code_1.h ztriangle_code_2.h ztriangle_code_3.h
    ztriangle_code_4.h ztriangle_table.h ztriangle_1.cxx ztriangle_2.cxx
    ztriangle_3.cxx ztriangle_4.cxx ztriangle_table.cxx
)
remake_include(${CMAKE_CURRENT_BINARY_DIR})

remake_add_plugin(tinydisplay *.cxx)
