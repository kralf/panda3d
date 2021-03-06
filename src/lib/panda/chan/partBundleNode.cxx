// Filename: partBundleNode.cxx
// Created by:  drose (06Mar02)
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

#include "partBundleNode.h"
#include "datagram.h"
#include "datagramIterator.h"
#include "bamReader.h"
#include "bamWriter.h"
#include "sceneGraphReducer.h"

TypeHandle PartBundleNode::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: PartBundleNode::Destructor
//       Access: Public, Virtual
//  Description: 
////////////////////////////////////////////////////////////////////
PartBundleNode::
~PartBundleNode() {
  Bundles::iterator bi;
  for (bi = _bundles.begin(); bi != _bundles.end(); ++bi) {
    (*bi)->get_bundle()->remove_node(this);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: PartBundleNode::apply_attribs_to_vertices
//       Access: Public, Virtual
//  Description: Applies whatever attributes are specified in the
//               AccumulatedAttribs object (and by the attrib_types
//               bitmask) to the vertices on this node, if
//               appropriate.  If this node uses geom arrays like a
//               GeomNode, the supplied GeomTransformer may be used to
//               unify shared arrays across multiple different nodes.
//
//               This is a generalization of xform().
////////////////////////////////////////////////////////////////////
void PartBundleNode::
apply_attribs_to_vertices(const AccumulatedAttribs &attribs, int attrib_types,
                          GeomTransformer &transformer) {
  if ((attrib_types & SceneGraphReducer::TT_transform) != 0) {
    Bundles::iterator bi;
    for (bi = _bundles.begin(); bi != _bundles.end(); ++bi) {
      PT(PartBundleHandle) handle = (*bi);
      PartBundle *bundle = handle->get_bundle();
      PT(PartBundle) new_bundle = bundle->apply_transform(attribs._transform);
      update_bundle(handle, new_bundle);
    }

    // Make sure the Geom bounding volumes get recomputed due to this
    // update.
    r_mark_geom_bounds_stale(Thread::get_current_thread());
  }
}

////////////////////////////////////////////////////////////////////
//     Function: PartBundleNode::xform
//       Access: Public, Virtual
//  Description: Transforms the contents of this PandaNode by the
//               indicated matrix, if it means anything to do so.  For
//               most kinds of PandaNodes, this does nothing.
////////////////////////////////////////////////////////////////////
void PartBundleNode::
xform(const LMatrix4f &mat) {
  // With plain xform(), we can't attempt to share bundles across
  // different nodes.  Better to use apply_attribs_to_vertices(),
  // instead.

  if (mat.almost_equal(LMatrix4f::ident_mat())) {
    // Don't bother.
    return;
  }

  Bundles::iterator bi;
  for (bi = _bundles.begin(); bi != _bundles.end(); ++bi) {
    PT(PartBundleHandle) handle = (*bi);
    PartBundle *bundle = handle->get_bundle();
    if (bundle->get_num_nodes() > 1) {
      PT(PartBundle) new_bundle = DCAST(PartBundle, bundle->copy_subgraph());
      update_bundle(handle, new_bundle);
      bundle = new_bundle;
    }
    bundle->xform(mat);
  }
}

////////////////////////////////////////////////////////////////////
//     Function: PartBundleNode::add_bundle
//       Access: Protected
//  Description: 
////////////////////////////////////////////////////////////////////
void PartBundleNode::
add_bundle(PartBundle *bundle) {
  PT(PartBundleHandle) handle = new PartBundleHandle(bundle);
  add_bundle_handle(handle);
}

////////////////////////////////////////////////////////////////////
//     Function: PartBundleNode::add_bundle_handle
//       Access: Protected
//  Description: 
////////////////////////////////////////////////////////////////////
void PartBundleNode::
add_bundle_handle(PartBundleHandle *handle) {
  Bundles::iterator bi = find(_bundles.begin(), _bundles.end(), handle);
  if (bi != _bundles.end()) {
    // This handle is already within the node.
    return;
  }

  _bundles.push_back(handle);
  handle->get_bundle()->add_node(this);
}

////////////////////////////////////////////////////////////////////
//     Function: PartBundleNode::steal_bundles
//       Access: Protected
//  Description: Moves the PartBundles from the other node onto this
//               one.
////////////////////////////////////////////////////////////////////
void PartBundleNode::
steal_bundles(PartBundleNode *other) {
  if (other == this) {
    return;
  }

  Bundles::iterator bi;
  for (bi = other->_bundles.begin(); bi != other->_bundles.end(); ++bi) {
    PartBundleHandle *handle = (*bi);
    handle->get_bundle()->remove_node(other);
    add_bundle_handle(handle);
  }
  other->_bundles.clear();
}

////////////////////////////////////////////////////////////////////
//     Function: PartBundleNode::update_bundle
//       Access: Protected, Virtual
//  Description: Replaces the contents of the indicated
//               PartBundleHandle (presumably stored within this node)
//               with new_bundle.
////////////////////////////////////////////////////////////////////
void PartBundleNode::
update_bundle(PartBundleHandle *old_bundle_handle, PartBundle *new_bundle) {
  PartBundle *old_bundle = old_bundle_handle->get_bundle();
  old_bundle->remove_node(this);
  old_bundle_handle->set_bundle(new_bundle);
  new_bundle->add_node(this);
}

////////////////////////////////////////////////////////////////////
//     Function: PartBundleNode::write_datagram
//       Access: Public, Virtual
//  Description: Writes the contents of this object to the datagram
//               for shipping out to a Bam file.
////////////////////////////////////////////////////////////////////
void PartBundleNode::
write_datagram(BamWriter *manager, Datagram &dg) {
  PandaNode::write_datagram(manager, dg);

  dg.add_uint16(_bundles.size());
  Bundles::iterator bi;
  for (bi = _bundles.begin(); bi != _bundles.end(); ++bi) {
    manager->write_pointer(dg, (*bi)->get_bundle());
  }
}

////////////////////////////////////////////////////////////////////
//     Function: PartBundleNode::complete_pointers
//       Access: Public, Virtual
//  Description: Receives an array of pointers, one for each time
//               manager->read_pointer() was called in fillin().
//               Returns the number of pointers processed.
////////////////////////////////////////////////////////////////////
int PartBundleNode::
complete_pointers(TypedWritable **p_list, BamReader* manager) {
  int pi = PandaNode::complete_pointers(p_list, manager);

  Bundles::iterator bi;
  for (bi = _bundles.begin(); bi != _bundles.end(); ++bi) {
    PT(PartBundle) bundle = DCAST(PartBundle, p_list[pi++]);
    bundle->add_node(this);
    (*bi) = new PartBundleHandle(bundle);
  }

  return pi;
}

////////////////////////////////////////////////////////////////////
//     Function: PartBundleNode::fillin
//       Access: Protected
//  Description: This internal function is called by make_from_bam to
//               read in all of the relevant data from the BamFile for
//               the new PandaNode.
////////////////////////////////////////////////////////////////////
void PartBundleNode::
fillin(DatagramIterator &scan, BamReader* manager) {
  PandaNode::fillin(scan, manager);

  int num_bundles = 1;
  if (manager->get_file_minor_ver() >= 5) {
    num_bundles = scan.get_uint16();
  }

  nassertv(num_bundles >= 1);

  // Bundle 0.  We already have a slot for this one.
  manager->read_pointer(scan);

  // Remaining bundles.  Push a new slot for each one.
  for (int i = 1; i < num_bundles; ++i) {
    manager->read_pointer(scan);
    _bundles.push_back(NULL);
  }
}
