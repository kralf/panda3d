// Filename: atomicAdjustWin32Impl.h
// Created by:  drose (07Feb06)
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

#ifndef ATOMICADJUSTWIN32IMPL_H
#define ATOMICADJUSTWIN32IMPL_H

#include "dtoolbase.h"
#include "selectThreadImpl.h"

#ifdef WIN32_VC

#include "numeric_types.h"
#define WIN32_LEAN_AND_MEAN
#include <windows.h>

////////////////////////////////////////////////////////////////////
//       Class : AtomicAdjustWin32Impl
// Description : Uses Windows native calls to implement atomic
//               adjustments.
////////////////////////////////////////////////////////////////////
class EXPCL_DTOOL AtomicAdjustWin32Impl {
public:
  typedef LONG Integer;

  INLINE static void inc(TVOLATILE Integer &var);
  INLINE static bool dec(TVOLATILE Integer &var);
  INLINE static void add(TVOLATILE Integer &var, Integer delta);
  INLINE static Integer set(TVOLATILE Integer &var, Integer new_value);
  INLINE static Integer get(const TVOLATILE Integer &var);

  INLINE static void *set_ptr(void * TVOLATILE &var, void *new_value);
  INLINE static void *get_ptr(void * const TVOLATILE &var);

  INLINE static Integer compare_and_exchange(TVOLATILE Integer &mem, 
                                             Integer old_value,
                                             Integer new_value);

  INLINE static void *compare_and_exchange_ptr(void * TVOLATILE &mem, 
                                               void *old_value,
                                               void *new_value);
};

#include "atomicAdjustWin32Impl.I"

#endif  // WIN32_VC

#endif
