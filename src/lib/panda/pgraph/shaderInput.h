// Filename: shaderInput.h
// Created by: jyelon (01Sep05)
// Updated by: fperazzi, PandaSE (06Apr10)
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

#ifndef SHADERINPUT_H
#define SHADERINPUT_H

#include "pandabase.h"
#include "typedWritableReferenceCount.h"
#include "pointerTo.h"
#include "nodePath.h"
#include "texture.h"
#include "internalName.h"
#include "shader.h"
#include "pta_float.h"
#include "pta_double.h"
#include "pta_LMatrix4f.h"
#include "pta_LMatrix3f.h"
#include "pta_LVecBase4f.h"
#include "pta_LVecBase3f.h"
#include "pta_LVecBase2f.h"

////////////////////////////////////////////////////////////////////
//       Class : ShaderInput
// Description : This is a small container class that can hold any
//               one of the value types that can be passed as input
//               to a shader.
////////////////////////////////////////////////////////////////////

class EXPCL_PANDA_PGRAPH ShaderInput: public TypedWritableReferenceCount {
public:
  INLINE ~ShaderInput();

PUBLISHED:
  static const ShaderInput *get_blank();
  INLINE ShaderInput(InternalName *id, int priority=0);
  INLINE ShaderInput(InternalName *id, const NodePath &np, int priority=0);
  INLINE ShaderInput(InternalName *id, Texture  *tex,      int priority=0);
  INLINE ShaderInput(InternalName *id, const PTA_float &ptr, int priority=0);
  INLINE ShaderInput(InternalName *id, const PTA_double &ptr, int priority=0); 
  INLINE ShaderInput(InternalName *id, const PTA_LVecBase4f& ptr, int priority=0); 
  INLINE ShaderInput(InternalName *id, const PTA_LVecBase3f& ptr, int priority=0); 
  INLINE ShaderInput(InternalName *id, const PTA_LVecBase2f& ptr, int priority=0); 
  INLINE ShaderInput(InternalName *id, const PTA_LMatrix4f& ptr, int priority=0); 
  INLINE ShaderInput(InternalName *id, const PTA_LMatrix3f& ptr, int priority=0); 
  INLINE ShaderInput(InternalName *id, const LVecBase4f& vec, int priority=0); 
  INLINE ShaderInput(InternalName *id, const LVecBase3f& vec, int priority=0); 
  INLINE ShaderInput(InternalName *id, const LVecBase2f& vec, int priority=0); 
  INLINE ShaderInput(InternalName *id, const LMatrix4f& mat, int priority=0); 
  INLINE ShaderInput(InternalName *id, const LMatrix3f& mat, int priority=0);

  enum ShaderInputType {
    M_invalid = 0,
    M_texture,
    M_nodepath,
    M_numeric
  };
  
  INLINE InternalName *get_name() const;
  
  INLINE int                          get_value_type() const;
  INLINE int                          get_priority() const;
  INLINE Texture                      *get_texture() const;
  INLINE const NodePath               &get_nodepath() const;
  INLINE const LVector4f              &get_vector() const;
  INLINE const Shader::ShaderPtrData  &get_ptr() const;

public:
  static void register_with_read_factory();

private:
  PT(InternalName) _name;
  int _type;
  int _priority;
  PT(Texture)           _stored_texture;
  NodePath              _stored_nodepath;
  LVector4f             _stored_vector;
  Shader::ShaderPtrData _stored_ptr;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    ReferenceCount::init_type();
    register_type(_type_handle, "ShaderInput",
                  TypedWritableReferenceCount::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};


#include "shaderInput.I"

#endif  // SHADERINPUT_H

