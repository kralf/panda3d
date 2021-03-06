// Filename: parabola_src.I
// Created by:  drose (10Oct07)
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


////////////////////////////////////////////////////////////////////
//     Function: Parabola::Default Constructor
//       Access: Published
//  Description: Constructs a meaningless degenerate parabola.
////////////////////////////////////////////////////////////////////
INLINE_MATHUTIL FLOATNAME(Parabola)::
FLOATNAME(Parabola)() :
  _a(FLOATNAME(LVecBase3)::zero()), 
  _b(FLOATNAME(LVecBase3)::zero()), 
  _c(FLOATNAME(LVecBase3)::zero())
{
}

////////////////////////////////////////////////////////////////////
//     Function: Parabola::Constructor
//       Access: Published
//  Description: Constructs a parabola given the three points of the
//               parametric equation: the acceleration, initial
//               velocity, and start point.
////////////////////////////////////////////////////////////////////
INLINE_MATHUTIL FLOATNAME(Parabola)::
FLOATNAME(Parabola)(const FLOATNAME(LVecBase3) &a,
                    const FLOATNAME(LVecBase3) &b,
                    const FLOATNAME(LVecBase3) &c) :
  _a(a), _b(b), _c(c)
{
}

////////////////////////////////////////////////////////////////////
//     Function: Parabola::Copy Constructor
//       Access: Published
//  Description: 
////////////////////////////////////////////////////////////////////
INLINE_MATHUTIL FLOATNAME(Parabola)::
FLOATNAME(Parabola)(const FLOATNAME(Parabola) &copy) :
  _a(copy._a),
  _b(copy._b),
  _c(copy._c)
{
}

////////////////////////////////////////////////////////////////////
//     Function: Parabola::Copy Assignment Operator
//       Access: Published
//  Description: 
////////////////////////////////////////////////////////////////////
INLINE_MATHUTIL void FLOATNAME(Parabola)::
operator = (const FLOATNAME(Parabola) &copy) {
  _a = copy._a;
  _b = copy._b;
  _c = copy._c;
}

////////////////////////////////////////////////////////////////////
//     Function: Parabola::Destructor
//       Access: Published
//  Description: 
////////////////////////////////////////////////////////////////////
INLINE_MATHUTIL FLOATNAME(Parabola)::
~FLOATNAME(Parabola)() {
}

////////////////////////////////////////////////////////////////////
//     Function: Parabola::get_a
//       Access: Published
//  Description: Returns the first point of the parabola's parametric
//               equation: the acceleration.
////////////////////////////////////////////////////////////////////
INLINE_MATHUTIL const FLOATNAME(LVecBase3) &FLOATNAME(Parabola)::
get_a() const {
  return _a;
}

////////////////////////////////////////////////////////////////////
//     Function: Parabola::get_b
//       Access: Published
//  Description: Returns the second point of the parabola's parametric
//               equation: the initial velocity.
////////////////////////////////////////////////////////////////////
INLINE_MATHUTIL const FLOATNAME(LVecBase3) &FLOATNAME(Parabola)::
get_b() const {
  return _b;
}

////////////////////////////////////////////////////////////////////
//     Function: Parabola::get_c
//       Access: Published
//  Description: Returns the third point of the parabola's parametric
//               equation: the start point.
////////////////////////////////////////////////////////////////////
INLINE_MATHUTIL const FLOATNAME(LVecBase3) &FLOATNAME(Parabola)::
get_c() const {
  return _c;
}

////////////////////////////////////////////////////////////////////
//     Function: Parabola::calc_point
//       Access: Published
//  Description: Computes the point on the parabola at time t.
////////////////////////////////////////////////////////////////////
INLINE_MATHUTIL FLOATNAME(LPoint3) FLOATNAME(Parabola)::
calc_point(FLOATTYPE t) const {
  return _a * t * t + _b * t + _c;
}
