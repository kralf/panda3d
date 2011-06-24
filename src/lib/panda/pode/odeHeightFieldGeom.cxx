// Filename: odeHeightFieldGeom.cxx
// Created by:  joswilso (27Dec06)
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

#include "config_ode.h"
#include "odeHeightFieldGeom.h"

TypeHandle OdeHeightfieldGeom::_type_handle;

OdeHeightfieldGeom::
OdeHeightfieldGeom(dGeomID id) :
  OdeGeom(id) {
}

OdeHeightfieldGeom::
OdeHeightfieldGeom() :
  OdeGeom(dCreateHeightfield(0, 0, false)) {
}

OdeHeightfieldGeom::
~OdeHeightfieldGeom() {
}
