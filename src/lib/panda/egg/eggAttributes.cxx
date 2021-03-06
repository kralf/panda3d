// Filename: eggAttributes.cxx
// Created by:  drose (16Jan99)
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

#include "eggAttributes.h"
#include "eggParameters.h"
#include "eggMorph.h"
#include "eggMorphList.h"

#include "indent.h"

TypeHandle EggAttributes::_type_handle;


////////////////////////////////////////////////////////////////////
//     Function: EggAttributes::Constructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
EggAttributes::
EggAttributes() {
  _flags = 0;
}

////////////////////////////////////////////////////////////////////
//     Function: EggAttributes::Copy constructor
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
EggAttributes::
EggAttributes(const EggAttributes &copy) {
  (*this) = copy;
}

////////////////////////////////////////////////////////////////////
//     Function: EggAttributes::Copy assignment operator
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
EggAttributes &EggAttributes::
operator = (const EggAttributes &copy) {
  _flags = copy._flags;
  _normal = copy._normal;
  _color = copy._color;
  _dnormals = copy._dnormals;
  _drgbas = copy._drgbas;
  return *this;
}

////////////////////////////////////////////////////////////////////
//     Function: EggAttributes::Destructor
//       Access: Published, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
EggAttributes::
~EggAttributes() {
}


////////////////////////////////////////////////////////////////////
//     Function: EggAttributes::write
//       Access: Published
//  Description: Writes the attributes to the indicated output stream in
//               Egg format.
////////////////////////////////////////////////////////////////////
void EggAttributes::
write(ostream &out, int indent_level) const {
  if (has_normal()) {
    if (_dnormals.empty()) {
      indent(out, indent_level)
        << "<Normal> { " << get_normal() << " }\n";
    } else {
      indent(out, indent_level) << "<Normal> {\n";
      indent(out, indent_level + 2) << get_normal() << "\n";
      _dnormals.write(out, indent_level + 2, "<DNormal>", 3);
      indent(out, indent_level) << "}\n";
    }
  }
  if (has_color()) {
    if (_drgbas.empty()) {
      indent(out, indent_level)
        << "<RGBA> { " << get_color() << " }\n";
    } else {
      indent(out, indent_level) << "<RGBA> {\n";
      indent(out, indent_level + 2) << get_color() << "\n";
      _drgbas.write(out, indent_level + 2, "<DRBGA>", 4);
      indent(out, indent_level) << "}\n";
    }
  }
}


////////////////////////////////////////////////////////////////////
//     Function: EggAttributes::compare_to
//       Access: Published
//  Description: An ordering operator to compare two vertices for
//               sorting order.  This imposes an arbitrary ordering
//               useful to identify unique vertices.
////////////////////////////////////////////////////////////////////
int EggAttributes::
compare_to(const EggAttributes &other) const {
  if (_flags != other._flags) {
    return (int)_flags - (int)other._flags;
  }

  if (has_normal()) {
    int compare =
      _normal.compare_to(other._normal, egg_parameters->_normal_threshold);
    if (compare != 0) {
      return compare;
    }
    compare = _dnormals.compare_to(other._dnormals);
    if (compare != 0) {
      return compare;
    }
  }

  if (has_color()) {
    int compare =
      _color.compare_to(other._color, egg_parameters->_color_threshold);
    if (compare != 0) {
      return compare;
    }
    compare = _drgbas.compare_to(other._drgbas);
    if (compare != 0) {
      return compare;
    }
  }

  return 0;
}

////////////////////////////////////////////////////////////////////
//     Function: EggAttributes::transform
//       Access: Published, Virtual
//  Description: Applies the indicated transformation matrix to the
//               attributes.
////////////////////////////////////////////////////////////////////
void EggAttributes::
transform(const LMatrix4d &mat) {
  if (has_normal()) {
    _normal = _normal * mat;
    LVector3d old_normal = _normal;
    _normal.normalize();

    EggMorphNormalList::iterator mi;
    for (mi = _dnormals.begin(); mi != _dnormals.end(); ++mi) {
      // We can safely cast the morph object to a non-const, because
      // we're not changing its name, which is the only thing the set
      // cares about preserving.
      EggMorphNormal &morph = (EggMorphNormal &)(*mi);

      // A bit of funny business to ensure the offset normal is
      // normalized after the transform.  This will break strange
      // normal morphs that want to change the length of the normal,
      // but what else can we do?
      LVector3d offset = (*mi).get_offset() * mat;
      LVector3d n = old_normal + offset;
      n.normalize();
      morph.set_offset(n - _normal);
    }
  }
}
