cmake_minimum_required(VERSION 2.6)

include(ReMake)

remake_project(
  Panda3D
  VERSION 1.6.2
  RELEASE stable
  SUMMARY "A framework for 3D rendering and game development."
  AUTHOR "Carnegie Mellon Entertainment Technology Center"
  CONTACT "etc-panda3d@lists.andrew.cmu.edu"
  HOME "http://panda3d.org"
  LICENSE "Modified BSD License"
  INSTALL /usr
  NOTES ReleaseNotes
)

remake_add_directories(
  models
  COMPONENT models
)

remake_pack_deb(
  COMPONENT dtool
  DESCRIPTION "deployment tool"
)
remake_pack_deb(
  panda3d-dtool
)

remake_pack_deb(
  COMPONENT dtool-dev
  DESCRIPTION "deployment development headers"
  panda3d-dtool
)
remake_pack_deb(
  COMPONENT dev
  DESCRIPTION "development headers"
  panda3d-dtool-dev
)
