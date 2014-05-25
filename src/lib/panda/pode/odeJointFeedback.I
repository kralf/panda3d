// Filename: odeJointFeedback.I
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

INLINE const LVecBase3f OdeJointFeedback::
get_force1() const {
  return LVecBase3f(_feedback.f1[0],
                    _feedback.f1[1],
                    _feedback.f1[2]);
}

INLINE const LVecBase3f OdeJointFeedback::
get_force2() const {
  return LVecBase3f(_feedback.f2[0],
                    _feedback.f2[1],
                    _feedback.f2[2]);
}

INLINE const LVecBase3f OdeJointFeedback::
get_torque1() const {
  return LVecBase3f(_feedback.t1[0],
                    _feedback.t1[1],
                    _feedback.t1[2]);
}

INLINE const LVecBase3f OdeJointFeedback::
get_torque2() const {
  return LVecBase3f(_feedback.t2[0],
                    _feedback.t2[1],
                    _feedback.t2[2]);
}
