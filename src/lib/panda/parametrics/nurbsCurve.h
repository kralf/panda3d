// Filename: nurbsCurve.h
// Created by:  drose (27Feb98)
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

#ifndef NURBSCURVE_H
#define NURBSCURVE_H

#include "pandabase.h"

#include "piecewiseCurve.h"
#include "nurbsCurveInterface.h"
#include "cubicCurveseg.h"

////////////////////////////////////////////////////////////////////
//       Class : NurbsCurve
// Description : A Nonuniform Rational B-Spline.
//
//               This class is actually implemented as a
//               PiecewiseCurve made up of several CubicCurvesegs,
//               each of which is created using the nurbs_basis()
//               method.  The list of CV's and knots is kept here,
//               within the NurbsCurve class.
//
//               This class is the original Panda-native
//               implementation of a NURBS curve.  It is typedeffed as
//               "NurbsCurve" and performs all NURBS curve functions
//               if we do not have the NURBS++ library available.
//
//               However, if we *do* have the NURBS++ library, another
//               class exists, the NurbsPPCurve, which is a wrapper
//               around that library and provides some additional
//               functionality.  In that case, the other class is
//               typedeffed to "NurbsCurve" instead of this one, and
//               performs most of the NURBS curve functions.  This
//               class then becomes vestigial.
////////////////////////////////////////////////////////////////////
class EXPCL_PANDA_PARAMETRICS NurbsCurve : public PiecewiseCurve, public NurbsCurveInterface {
PUBLISHED:
  NurbsCurve();
  NurbsCurve(const ParametricCurve &pc);
public:
  NurbsCurve(int order, int num_cvs,
                    const float knots[], const LVecBase4f cvs[]);
PUBLISHED:
  virtual ~NurbsCurve();

public:
  virtual PandaNode *make_copy() const;

  // We don't need to re-publish these, since they're all published
  // from NurbsCurveInterface.
  virtual void set_order(int order);
  virtual int get_order() const;

  virtual int get_num_cvs() const;
  virtual int get_num_knots() const;

  virtual bool insert_cv(float t);

  virtual bool remove_cv(int n);
  virtual void remove_all_cvs();

  virtual bool set_cv(int n, const LVecBase4f &v);
  virtual LVecBase4f get_cv(int n) const;

  virtual bool set_knot(int n, float t);
  virtual float get_knot(int n) const;

  virtual bool recompute();

public:
  virtual bool
  rebuild_curveseg(int rtype0, float t0, const LVecBase4f &v0,
                   int rtype1, float t1, const LVecBase4f &v1,
                   int rtype2, float t2, const LVecBase4f &v2,
                   int rtype3, float t3, const LVecBase4f &v3);

  virtual bool stitch(const ParametricCurve *a, const ParametricCurve *b);

  INLINE CubicCurveseg *get_curveseg(int ti);

  virtual NurbsCurveInterface *get_nurbs_interface();
  virtual bool convert_to_nurbs(ParametricCurve *nc) const;
  virtual void write(ostream &out, int indent_level = 0) const;

protected:
  virtual int append_cv_impl(const LVecBase4f &v);
  virtual bool format_egg(ostream &out, const string &name,
                          const string &curve_type, int indent_level) const;

  int find_cv(float t);

  int _order;

  class CV {
  public:
    CV() {}
    CV(const LVecBase4f &p, float t) : _p(p), _t(t) {}
    LVecBase4f _p;
    float _t;
  };

  pvector<CV> _cvs;


// TypedWritable stuff
public:
  static void register_with_read_factory();

protected:
  static TypedWritable *make_NurbsCurve(const FactoryParams &params);
  virtual void write_datagram(BamWriter *manager, Datagram &me);
  void fillin(DatagramIterator &scan, BamReader *manager);

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    PiecewiseCurve::init_type();
    NurbsCurveInterface::init_type();
    register_type(_type_handle, "NurbsCurve",
                  PiecewiseCurve::get_class_type(),
                  NurbsCurveInterface::get_class_type());
 }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#include "nurbsCurve.I"

#endif
