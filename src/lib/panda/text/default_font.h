// Filename: default_font.h
// Created by:  drose (31Jan03)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////

#ifndef DEFAULT_FONT_H
#define DEFAULT_FONT_H

#include "pandabase.h"

#if defined(COMPILE_IN_DEFAULT_FONT) && !defined(CPPPARSER)

extern const unsigned char default_font_data[];
extern const int default_font_size;

#endif  // HAVE_FREETYPE && COMPILE_IN_DEFAULT_FONT && !CPPPARSER

#endif

