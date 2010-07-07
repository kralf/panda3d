// Filename: eggToDXFLayer.h
// Created by:  drose (04May04)
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

#ifndef EGGTODXFLAYER_H
#define EGGTODXFLAYER_H

#include "pandatoolbase.h"
#include "pmap.h"
#include "pvector.h"
#include "luse.h"

class EggPolygon;
class EggGroupNode;

////////////////////////////////////////////////////////////////////
//       Class : EggToDXFLayer
// Description : A single layer in the DXF file to be written by
//               EggToDXF.
////////////////////////////////////////////////////////////////////
class EggToDXFLayer {
public:
  EggToDXFLayer(EggGroupNode *group);
  EggToDXFLayer(const EggToDXFLayer &copy);
  void operator = (const EggToDXFLayer &copy);

  void add_color(const Colorf &color);
  void choose_overall_color();

  void write_layer(ostream &out);
  void write_polyline(EggPolygon *poly, ostream &out);
  void write_3d_face(EggPolygon *poly, ostream &out);
  void write_entities(ostream &out, bool use_polyline);

private:
  int get_autocad_color(const Colorf &color);

  typedef pmap<int, int> ColorCounts;
  ColorCounts _color_counts;

  EggGroupNode *_group;
  int _layer_color;
};

typedef pvector<EggToDXFLayer> EggToDXFLayers;

#endif
