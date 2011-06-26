remake_include(
  *
  ../dtool/*
  ../panda/*
)
panda3d_interrogate_include(
  ../dtool/cppparse/include
)

remake_define(WITHIN_PANDA ON)

remake_add_directories()
