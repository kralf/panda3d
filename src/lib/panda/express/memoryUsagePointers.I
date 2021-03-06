// Filename: memoryUsagePointers.I
// Created by:  drose (25May00)
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
//     Function: MemoryUsagePointers::Entry::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE MemoryUsagePointers::Entry::
Entry(ReferenceCount *ref_ptr, TypedObject *typed_ptr,
      TypeHandle type, double age) :
  _ref_ptr(ref_ptr),
  _typed_ptr(typed_ptr),
  _type(type),
  _age(age)
{
  _ref_ptr->ref();
}

////////////////////////////////////////////////////////////////////
//     Function: MemoryUsagePointers::Entry::Copy Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE MemoryUsagePointers::Entry::
Entry(const Entry &copy) :
  _ref_ptr(copy._ref_ptr),
  _typed_ptr(copy._typed_ptr),
  _type(copy._type),
  _age(copy._age)
{
  _ref_ptr->ref();
}

////////////////////////////////////////////////////////////////////
//     Function: MemoryUsagePointers::Entry::Copy Assigment Operator
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void MemoryUsagePointers::Entry::
operator = (const Entry &copy) {
  if (_ref_ptr != copy._ref_ptr) {
    _ref_ptr->unref();
    _ref_ptr = copy._ref_ptr;
    // We can't call unref_delete(), because we don't know what kind
    // of pointer it is precisely.  Potential leak.
    _ref_ptr->ref();
  }
  _typed_ptr = copy._typed_ptr;
  _type = copy._type;
  _age = copy._age;
}

////////////////////////////////////////////////////////////////////
//     Function: MemoryUsagePointers::Entry::Destructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE MemoryUsagePointers::Entry::
~Entry() {
  // We can't call unref_delete(), because we don't know what kind
  // of pointer it is precisely.  Potential leak.
  _ref_ptr->unref();
}

