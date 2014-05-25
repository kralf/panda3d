// Filename: odeJointFeedback.h
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

#ifndef ODEJOINTFEEDBACK_H
#define ODEJOINTFEEDBACK_H

#include "pandabase.h"
#include "typedObject.h"
#include "luse.h"

#include "ode_includes.h"

////////////////////////////////////////////////////////////////////
//       Class : OdeJointFeedback
// Description : 
////////////////////////////////////////////////////////////////////
class EXPCL_PANDAODE OdeJointFeedback : public TypedObject {
PUBLISHED:
  OdeJointFeedback();
  virtual ~OdeJointFeedback();

  INLINE const LVecBase3f get_force1() const;
  INLINE const LVecBase3f get_force2() const;
  INLINE const LVecBase3f get_torque1() const;
  INLINE const LVecBase3f get_torque2() const;

public:
  dJointFeedback* get_feedback_ptr();
  
private:
  dJointFeedback _feedback;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedObject::init_type();
    register_type(_type_handle, "OdeJointFeedback",
		  TypedObject::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "odeJointFeedback.I"

#endif

