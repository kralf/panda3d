// Filename: orthographicLens.cxx
// Created by:  mike (18Feb99)
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

#include "orthographicLens.h"
#include "indent.h"
#include "bamReader.h"

TypeHandle OrthographicLens::_type_handle;


////////////////////////////////////////////////////////////////////
//     Function: OrthographicLens::make_copy
//       Access: Public, Virtual
//  Description: Allocates a new Lens just like this one.
////////////////////////////////////////////////////////////////////
PT(Lens) OrthographicLens::
make_copy() const {
  return new OrthographicLens(*this);
}

////////////////////////////////////////////////////////////////////
//     Function: OrthographicLens::is_linear
//       Access: Published, Virtual
//  Description: Returns true if the lens represents a linear
//               projection (e.g. PerspectiveLens, OrthographicLens),
//               and therefore there is a valid matrix returned by
//               get_projection_mat(), or false otherwise.
////////////////////////////////////////////////////////////////////
bool OrthographicLens::
is_linear() const {
  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: OrthographicLens::is_orthographic
//       Access: Published, Virtual
//  Description: Returns true if the lens represents a orthographic
//               projection (i.e. it is a OrthographicLens), false
//               otherwise.
////////////////////////////////////////////////////////////////////
bool OrthographicLens::
is_orthographic() const {
  return true;
}

////////////////////////////////////////////////////////////////////
//     Function: OrthographicLens::write
//       Access: Public, Virtual
//  Description: 
////////////////////////////////////////////////////////////////////
void OrthographicLens::
write(ostream &out, int indent_level) const {
  indent(out, indent_level) << get_type() << " film size = " << get_film_size() << "\n";
}

////////////////////////////////////////////////////////////////////
//     Function: OrthographicLens::compute_projection_mat
//       Access: Protected, Virtual
//  Description: Computes the complete transformation matrix from 3-d
//               point to 2-d point, if the lens is linear.
////////////////////////////////////////////////////////////////////
void OrthographicLens::
compute_projection_mat() {
  CoordinateSystem cs = _cs;
  if (cs == CS_default) {
    cs = get_default_coordinate_system();
  }

  float a = 2.0f / (_far_distance - _near_distance);
  float b = -(_far_distance + _near_distance) / (_far_distance - _near_distance);

  LMatrix4f canonical;
  switch (cs) {
  case CS_zup_right:
    canonical.set(1.0f,  0.0f,  0.0f,  0.0f,
                  0.0f,  0.0f,     a,  0.0f,
                  0.0f,  1.0f,  0.0f,  0.0f,
                  0.0f,  0.0f,     b,  1.0f);
    break;

  case CS_yup_right:
    canonical.set(1.0f,  0.0f,  0.0f,  0.0f,
                  0.0f,  1.0f,  0.0f,  0.0f,
                  0.0f,  0.0f,    -a,  0.0f,
                  0.0f,  0.0f,     b,  1.0f);
    break;

  case CS_zup_left:
    canonical.set(1.0f,  0.0f,  0.0f,  0.0f,
                  0.0f,  0.0f,    -a,  0.0f,
                  0.0f,  1.0f,  0.0f,  0.0f,
                  0.0f,  0.0f,     b,  1.0f);
    break;

  case CS_yup_left:
    canonical.set(1.0f,  0.0f,  0.0f,  0.0f,
                  0.0f,  1.0f,  0.0f,  0.0f,
                  0.0f,  0.0f,     a,  0.0f,
                  0.0f,  0.0f,     b,  1.0f);
    break;

  default:
    gobj_cat.error()
      << "Invalid coordinate system " << (int)cs << " in OrthographicLens!\n";
    canonical = LMatrix4f::ident_mat();
  }

  _projection_mat = get_lens_mat_inv() * canonical * get_film_mat();
  _projection_mat_left = _projection_mat_right = _projection_mat;

  adjust_comp_flags(CF_projection_mat_inv | CF_projection_mat_left_inv | 
                    CF_projection_mat_right_inv,
                    CF_projection_mat);
}

////////////////////////////////////////////////////////////////////
//     Function: OrthographicLens::register_with_read_factory
//       Access: Public, Static
//  Description: Tells the BamReader how to create objects of type
//               Lens.
////////////////////////////////////////////////////////////////////
void OrthographicLens::
register_with_read_factory() {
  BamReader::get_factory()->register_factory(get_class_type(), make_from_bam);
}

////////////////////////////////////////////////////////////////////
//     Function: OrthographicLens::make_from_bam
//       Access: Protected, Static
//  Description: This function is called by the BamReader's factory
//               when a new object of type Lens is encountered
//               in the Bam file.  It should create the Lens
//               and extract its information from the file.
////////////////////////////////////////////////////////////////////
TypedWritable *OrthographicLens::
make_from_bam(const FactoryParams &params) {
  OrthographicLens *lens = new OrthographicLens;
  DatagramIterator scan;
  BamReader *manager;

  parse_params(params, scan, manager);
  lens->fillin(scan, manager);

  return lens;
}
