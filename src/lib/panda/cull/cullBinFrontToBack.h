// Filename: cullBinFrontToBack.h
// Created by:  drose (29May02)
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

#ifndef CULLBINFRONTTOBACK_H
#define CULLBINFRONTTOBACK_H

#include "pandabase.h"

#include "cullBin.h"
#include "geom.h"
#include "transformState.h"
#include "renderState.h"
#include "pointerTo.h"

////////////////////////////////////////////////////////////////////
//       Class : CullBinFrontToBack
// Description : A specific kind of CullBin that sorts geometry in
//               order from nearest to furthest based on the center of
//               its bounding volume.
//
//               This is useful for rendering opaque geometry, taking
//               optimal advantage of a hierarchical Z-buffer.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDA_CULL CullBinFrontToBack : public CullBin {
public:
  INLINE CullBinFrontToBack(const string &name, 
                            GraphicsStateGuardianBase *gsg,
                            const PStatCollector &draw_region_pcollector);
  virtual ~CullBinFrontToBack();

  static CullBin *make_bin(const string &name, 
                           GraphicsStateGuardianBase *gsg,
                           const PStatCollector &draw_region_pcollector);

  virtual void add_object(CullableObject *object, Thread *current_thread);
  virtual void finish_cull(SceneSetup *scene_setup, Thread *current_thread);
  virtual void draw(bool force, Thread *current_thread);

protected:
  virtual void fill_result_graph(ResultGraphBuilder &builder);

private:
  class ObjectData {
  public:
    INLINE ObjectData(CullableObject *object, float dist);
    INLINE bool operator < (const ObjectData &other) const;
    
    CullableObject *_object;
    float _dist;
  };

  typedef pvector<ObjectData> Objects;
  Objects _objects;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    CullBin::init_type();
    register_type(_type_handle, "CullBinFrontToBack",
                  CullBin::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "cullBinFrontToBack.I"

#endif


  
