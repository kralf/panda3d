// Filename: atomicAdjustI386Impl.I
// Created by:  drose (01Apr06)
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
//     Function: AtomicAdjustI386Impl::inc
//       Access: Public, Static
//  Description: Atomically increments the indicated variable.
////////////////////////////////////////////////////////////////////
INLINE void AtomicAdjustI386Impl::
inc(TVOLATILE AtomicAdjustI386Impl::Integer &var) {
#ifdef _M_IX86
  // Windows case
  TVOLATILE Integer *var_ptr = &var;
  __asm {
    mov edx, var_ptr;
    lock inc dword ptr [edx];
  }
#elif !defined(__EDG__)
  // GCC case
  __asm__ __volatile__("lock; incl %0"
                       :"=m" (var)
                       :"m" (&var));
#endif  // __EDG__
}

////////////////////////////////////////////////////////////////////
//     Function: AtomicAdjustI386Impl::dec
//       Access: Public, Static
//  Description: Atomically decrements the indicated variable and
//               returns true if the new value is nonzero, false if it
//               is zero.
////////////////////////////////////////////////////////////////////
INLINE bool AtomicAdjustI386Impl::
dec(TVOLATILE AtomicAdjustI386Impl::Integer &var) {
  unsigned char c;
#ifdef _M_IX86
  // Windows case
  TVOLATILE Integer *var_ptr = &var;
  __asm {
    mov edx, var_ptr;
    lock dec dword ptr [edx];
    sete c;
  }
#elif !defined(__EDG__)
  // GCC case
  __asm__ __volatile__("lock; decl %0; sete %1"
                       :"=m" (var), "=qm" (c)
                       :"m" (&var) : "memory");
#endif  // __EDG__
  return (c == 0);
}

////////////////////////////////////////////////////////////////////
//     Function: AtomicAdjustI386Impl::add
//       Access: Public, Static
//  Description: Atomically computes var += delta.  It is legal for
//               delta to be negative.
////////////////////////////////////////////////////////////////////
INLINE void AtomicAdjustI386Impl::
add(TVOLATILE AtomicAdjustI386Impl::Integer &var, AtomicAdjustI386Impl::Integer delta) {
  Integer orig_value = var;
  while (compare_and_exchange(var, orig_value, orig_value + delta) != orig_value) {
    orig_value = var;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: AtomicAdjustI386Impl::set
//       Access: Public, Static
//  Description: Atomically changes the indicated variable and
//               returns the original value.
////////////////////////////////////////////////////////////////////
INLINE AtomicAdjustI386Impl::Integer AtomicAdjustI386Impl::
set(TVOLATILE AtomicAdjustI386Impl::Integer &var, AtomicAdjustI386Impl::Integer new_value) {
  Integer orig_value = var;
  var = new_value;
  return orig_value;
}

////////////////////////////////////////////////////////////////////
//     Function: AtomicAdjustI386Impl::get
//       Access: Public, Static
//  Description: Atomically retrieves the snapshot value of the
//               indicated variable.  This is the only guaranteed safe
//               way to retrieve the value that other threads might be
//               asynchronously setting, incrementing, or decrementing
//               (via other AtomicAjust methods).
////////////////////////////////////////////////////////////////////
INLINE AtomicAdjustI386Impl::Integer AtomicAdjustI386Impl::
get(const TVOLATILE AtomicAdjustI386Impl::Integer &var) {
  return var;
}

////////////////////////////////////////////////////////////////////
//     Function: AtomicAdjustI386Impl::set_ptr
//       Access: Public, Static
//  Description: Atomically changes the indicated variable and
//               returns the original value.
////////////////////////////////////////////////////////////////////
INLINE void *AtomicAdjustI386Impl::
set_ptr(void * TVOLATILE &var, void *new_value) {
  void *orig_value = var;
  var = new_value;
  return orig_value;
}

////////////////////////////////////////////////////////////////////
//     Function: AtomicAdjustI386Impl::get_ptr
//       Access: Public, Static
//  Description: Atomically retrieves the snapshot value of the
//               indicated variable.  This is the only guaranteed safe
//               way to retrieve the value that other threads might be
//               asynchronously setting, incrementing, or decrementing
//               (via other AtomicAjust methods).
////////////////////////////////////////////////////////////////////
INLINE void *AtomicAdjustI386Impl::
get_ptr(void * const TVOLATILE &var) {
  return var;
}

////////////////////////////////////////////////////////////////////
//     Function: AtomicAdjustI386Impl::compare_and_exchange
//       Access: Public, Static
//  Description: Atomic compare and exchange.  
//
//               If mem is equal to old_value, store new_value in mem.
//               In either case, return the original value of mem.
//               The caller can test for success by comparing
//               return_value == old_value.
//
//               The atomic function expressed in pseudo-code:
//
//                 orig_value = mem;
//                 if (mem == old_value) {
//                   mem = new_value;
//                 }
//                 return orig_value;
//
////////////////////////////////////////////////////////////////////
INLINE AtomicAdjustI386Impl::Integer AtomicAdjustI386Impl::
compare_and_exchange(TVOLATILE AtomicAdjustI386Impl::Integer &mem, AtomicAdjustI386Impl::Integer old_value,
                     AtomicAdjustI386Impl::Integer new_value) {
  Integer prev;
#ifdef _M_IX86
  // Windows case
  TVOLATILE Integer *mem_ptr = &mem;
  __asm {
    mov edx, mem_ptr;
    mov ecx, new_value;
    mov eax, old_value;
    lock cmpxchg dword ptr [edx], ecx;
    mov prev, eax;
  }
#elif !defined(__EDG__)
  // GCC case
  __asm__ __volatile__("lock; cmpxchgl %1,%2"
                       : "=a"(prev)
                       : "r"(new_value), "m"(mem), "0"(old_value)
                       : "memory");
#endif  // __EDG__
  return prev;
}

////////////////////////////////////////////////////////////////////
//     Function: AtomicAdjustI386Impl::compare_and_exchange_ptr
//       Access: Public, Static
//  Description: Atomic compare and exchange.  
//
//               As above, but works on pointers instead of integers.
////////////////////////////////////////////////////////////////////
INLINE void *AtomicAdjustI386Impl::
compare_and_exchange_ptr(void * TVOLATILE &mem, void *old_value,
                         void *new_value) {
  void *prev;
#ifdef _M_IX86
  // Windows case
  void * TVOLATILE *mem_ptr = &mem;
  __asm {
    mov edx, mem_ptr;
    mov ecx, new_value;
    mov eax, old_value;
    lock cmpxchg dword ptr [edx], ecx;
    mov prev, eax;
  }
#elif !defined(__EDG__)
  // GCC case
  __asm__ __volatile__("lock; cmpxchgl %1,%2"
                       : "=a"(prev)
                       : "r"(new_value), "m"(mem), "0"(old_value)
                       : "memory");
#endif  // __EDG__
  return prev;
}
