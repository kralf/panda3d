// Filename: collisionVisualizer.h
// Created by:  drose (16Apr03)
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

#ifndef COLLISIONVISUALIZER_H
#define COLLISIONVISUALIZER_H

#include "pandabase.h"
#include "pandaNode.h"
#include "collisionRecorder.h"
#include "collisionSolid.h"
#include "nodePath.h"
#include "pmap.h"

#ifdef DO_COLLISION_RECORDING

////////////////////////////////////////////////////////////////////
//       Class : CollisionVisualizer
// Description : This class is used to help debug the work the
//               collisions system is doing.  It shows the polygons
//               that are detected as collisions, as well as those
//               that are simply considered for collisions.
//
//               It may be parented anywhere in the scene graph where
//               it will be rendered to achieve this.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDA_COLLIDE CollisionVisualizer : public PandaNode, public CollisionRecorder {
PUBLISHED:
  CollisionVisualizer(const string &name);
  virtual ~CollisionVisualizer();

  INLINE void set_point_scale(float point_scale);
  INLINE float get_point_scale() const;

  INLINE void set_normal_scale(float normal_scale);
  INLINE float get_normal_scale() const;

  void clear();

public:
  // from parent class PandaNode.
  virtual PandaNode *make_copy() const;
  virtual bool cull_callback(CullTraverser *trav, CullTraverserData &data);
  virtual bool is_renderable() const;
  virtual void output(ostream &out) const;

  // from parent class CollisionRecorder.
  virtual void begin_traversal();
  virtual void collision_tested(const CollisionEntry &entry, bool detected);

  // To disambiguate the multiple inheritance from TypedObject.
  INLINE TypedObject *as_typed_object();
  INLINE const TypedObject *as_typed_object() const;

private:
  CPT(RenderState) get_viz_state();

private:
  class SolidInfo {
  public:
    INLINE SolidInfo();
    int _detected_count;
    int _missed_count;
  };
  typedef pmap<CPT(CollisionSolid), SolidInfo> Solids;

  class CollisionPoint {
  public:
    LPoint3f _surface_point;
    LVector3f _surface_normal;
    LPoint3f _interior_point;
  };
  typedef pvector<CollisionPoint> Points;

  class VizInfo {
  public:
    Solids _solids;
    Points _points;
  };

  typedef pmap<CPT(TransformState), VizInfo> Data;
  Data _data;

  float _point_scale;
  float _normal_scale;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }

  static void init_type() {
    PandaNode::init_type();
    CollisionRecorder::init_type();
    register_type(_type_handle, "CollisionVisualizer",
                  PandaNode::get_class_type(),
                  CollisionRecorder::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "collisionVisualizer.I"

#endif  // DO_COLLISION_RECORDING  

#endif
