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

remake_project_get(FILE_DESTINATION DESTINATION OUTPUT MODEL_DESTINATION)

remake_add_directories(
  python
  data
)
remake_add_directories(
  modules
  COMPONENT dev
)
remake_doc(
  man INSTALL share
  ps
  html
)

remake_pack_deb(
  COMPONENT dtool
  DESCRIPTION "distribution tool"
  DEPENDS libpython2.[0-9]* libssl[0-9].[0-9].[0-9]
)
remake_pack_deb(
  DEPENDS panda3d-dtool zlib1g libode1 libopenal1 libfreetype6
    libjpeg[0-9]* libpng12-0 libtiff4 libcg
  EXTRA debian/*
)
remake_pack_deb(
  COMPONENT direct
  DESCRIPTION "Python interface"
  DEPENDS panda3d
)
remake_pack_deb(
  COMPONENT tools
  DESCRIPTION "tools"
  DEPENDS panda3d libgtk2.0-0
)
remake_pack_deb(
  COMPONENT python
  DESCRIPTION "Python modules"
  DEPENDS panda3d-direct python
)
remake_pack_deb(
  COMPONENT test
  DESCRIPTION "testing binaries"
  DEPENDS panda3d-dtool panda3d panda3d-tools
)

remake_pack_deb(
  COMPONENT dtool-dev
  DESCRIPTION "distribution tool development headers"
  DEPENDS panda3d-dtool python-dev libssl-dev
)
remake_pack_deb(
  COMPONENT dev
  DESCRIPTION "development headers"
  DEPENDS panda3d panda3d-dtool-dev zlib1g-dev libode-dev
    libopenal-dev libfreetype6-dev libjpeg[0-9][0-9]*-dev
    libpng12-dev libtiff4-dev libgl1-mesa-dev nvidia-cg-toolkit
)
remake_pack_deb(
  COMPONENT direct-dev
  DESCRIPTION "Python interface development headers"
  DEPENDS panda3d-direct panda3d-dev
)
remake_pack_deb(
  COMPONENT tools-dev
  DESCRIPTION "tools development headers"
  DEPENDS panda3d-tools panda3d-dev libgtk2.0-dev
)

remake_pack_deb(
  ARCH all
  COMPONENT models
  DESCRIPTION "models"
  DEPENDS panda3d
)
remake_pack_deb(
  COMPONENT samples
  DESCRIPTION "sample applications"
  DEPENDS panda3d-python panda3d-models
)

remake_pack_deb(
  COMPONENT blender
  DESCRIPTION "blender scripts"
  DEPENDS panda3d-tools blender
)

remake_pack_deb(
  ARCH all
  COMPONENT doc
  DESCRIPTION "documentation"
)

remake_distribute_deb(
  DISTRIBUTION lucid
  SECTION python
  UPLOAD ppa:kralf/asl
  DEPENDS remake python-dev libssl-dev libgtk2.0-dev zlib1g-dev
    libode-dev libgl1-mesa-dev libopenal-dev libfreetype6-dev
    libjpeg62-dev libpng12-dev libtiff4-dev nvidia-cg-toolkit bison
    flex python blender groff pkg-config
  PASS CMAKE_BUILD_TYPE PANDA3D_GIT_REVISION
)

remake_distribute_deb(
  DISTRIBUTION precise
  SECTION python
  UPLOAD ppa:kralf/asl
  DEPENDS remake python-dev libssl-dev libgtk2.0-dev zlib1g-dev
    libode-dev libgl1-mesa-dev libopenal-dev libfreetype6-dev
    libjpeg8-dev libpng12-dev libtiff4-dev nvidia-cg-toolkit bison
    flex python blender groff pkg-config
  PASS CMAKE_BUILD_TYPE PANDA3D_GIT_REVISION
)
