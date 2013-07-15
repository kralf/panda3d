// Filename: pandatiny.cxx
// Created by:  kralf (15Jul13)
// 
////////////////////////////////////////////////////////////////////

#include "pandatiny.h"

#include "config_tinydisplay.h"

#ifdef WIN32
#include "tinyWinGraphicsPipe.h"
#endif

#ifdef IS_OSX
#include "tinyOsxGraphicsPipe.h"
#endif

#ifdef IS_LINUX
#include "tinyXGraphicsPipe.h"
#endif

// By including checkPandaVersion.h, we guarantee that runtime
// attempts to load libpandagl.so/.dll will fail if they inadvertently
// link with the wrong version of libdtool.so/.dll.

#include "checkPandaVersion.h"

////////////////////////////////////////////////////////////////////
//     Function: init_libpandatiny
//  Description: Initializes the library.  This must be called at
//               least once before any of the functions or classes in
//               this library can be used.  Normally it will be
//               called by the static initializers and need not be
//               called explicitly, but special cases exist.
////////////////////////////////////////////////////////////////////
void
init_libpandatiny() {
  init_libtinydisplay();
}

////////////////////////////////////////////////////////////////////
//     Function: get_pipe_type
//  Description: Returns the TypeHandle index of the recommended
//               graphics pipe type defined by this module.
////////////////////////////////////////////////////////////////////
int
get_pipe_type() {
#ifdef WIN32
  return TinyWinGraphicsPipe::get_class_type().get_index();
#endif

#ifdef IS_OSX
  return TinyOsxGraphicsPipe::get_class_type().get_index();
#endif

#ifdef IS_LINUX
  return TinyXGraphicsPipe::get_class_type().get_index();
#endif

  return 0;
}
