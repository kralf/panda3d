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
)
