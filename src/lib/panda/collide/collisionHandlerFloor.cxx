// Filename: collisionHandlerFloor.cxx
// Created by:  drose (16Mar02)
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

#include "collisionHandlerFloor.h"
#include "collisionNode.h"
#include "collisionEntry.h"
#include "config_collide.h"

#include "clockObject.h"

TypeHandle CollisionHandlerFloor::_type_handle;

////////////////////////////////////////////////////////////////////
//     Function: CollisionHandlerFloor::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
CollisionHandlerFloor::
CollisionHandlerFloor() {
  _offset = 0.0f;
  _reach = 1.0f;
  _max_velocity = 0.0f;
}

////////////////////////////////////////////////////////////////////
//     Function: CollisionHandlerFloor::Destructor
//       Access: Public, Virtual
//  Description:
////////////////////////////////////////////////////////////////////
CollisionHandlerFloor::
~CollisionHandlerFloor() {
}

////////////////////////////////////////////////////////////////////
//     Function: CollisionHandlerGravity::set_highest_collision
//       Access: Protected
//  Description: 
//               
//               
//
//               
//               
//               
////////////////////////////////////////////////////////////////////
float CollisionHandlerFloor::
set_highest_collision(const NodePath &target_node_path, const NodePath &from_node_path, const Entries &entries) {
  // Get the maximum height for all collisions with this node.
  // This is really the distance to-the-ground, so it will
  // be negative when the avatar is above the ground.
  // Larger values (less negative) are higher elevation (assuming
  // the avatar is right-side-up (or the ray is plumb)).
  bool got_max = false;
  bool got_min = false;
  float max_height = 0.0f;
  float min_height = 0.0f;
  CollisionEntry *highest = NULL;
  CollisionEntry *lowest = NULL;

  Entries::const_iterator ei;
  for (ei = entries.begin(); ei != entries.end(); ++ei) {
    CollisionEntry *entry = (*ei);
    nassertr(entry != (CollisionEntry *)NULL, 0.0f);
    nassertr(from_node_path == entry->get_from_node_path(), 0.0f);

    if (entry->has_surface_point()) {
      LPoint3f point = entry->get_surface_point(target_node_path);
      if (collide_cat.is_debug()) {
        collide_cat.debug()
          << "Intersection point detected at " << point << "\n";
      }

      float height = point[2];
      if (height < _offset + _reach &&
         (!got_max || height > max_height)) {
        got_max = true;
        max_height = height;
        highest = entry;
      }
      if (!got_min || height < min_height) {
        got_min = true;
        min_height = height;
        lowest = entry;
      }
    }
  }
  if (!got_max && got_min) {
    // We've fallen through the world, but we're also under some walkable
    // geometry.
    // Move us up to the lowest surface:
    got_max = true;
    max_height = min_height;
    highest = lowest;
  }
  //#*#_has_contact = got_max;

  #if 0
    cout<<"\ncolliding with:\n";
    for (Colliding::const_iterator i = _current_colliding.begin(); i != _current_colliding.end(); ++i) {
      (**i).write(cout, 2);
    }
    cout<<"\nhighest:\n";
    highest->write(cout, 2);
    cout<<endl;
  #endif
  #if 1
  // We only collide with things we are impacting with.
  // Remove the collisions:
  _current_colliding.clear();
  // Add only the one that we're impacting with:
  add_entry(highest);
  #endif
  
  return max_height;
}

////////////////////////////////////////////////////////////////////
//     Function: CollisionHandlerFloor::handle_entries
//       Access: Protected, Virtual
//  Description: Called by the parent class after all collisions have
//               been detected, this manages the various collisions
//               and moves around the nodes as necessary.
//
//               The return value is normally true, but it may be
//               false to indicate the CollisionTraverser should
//               disable this handler from being called in the future.
////////////////////////////////////////////////////////////////////
bool CollisionHandlerFloor::
handle_entries() {
  bool okflag = true;

  // Reset the set of things our parent class CollisionHandlerEvent
  // recorded a collision with.  We'll only consider ourselves
  // collided with the topmost object for each from_entry.
  _current_colliding.clear();

  FromEntries::const_iterator fi;
  for (fi = _from_entries.begin(); fi != _from_entries.end(); ++fi) {
    const NodePath &from_node_path = (*fi).first;
    const Entries &entries = (*fi).second;

    Colliders::iterator ci;
    ci = _colliders.find(from_node_path);
    if (ci == _colliders.end()) {
      // Hmm, someone added a CollisionNode to a traverser and gave
      // it this CollisionHandler pointer--but they didn't tell us
      // about the node.
      collide_cat.error()
        << get_type() << " doesn't know about "
        << from_node_path << ", disabling.\n";
      okflag = false;
    } else {
      ColliderDef &def = (*ci).second;
      {
        #if 0
        // Get the maximum height for all collisions with this node.
        bool got_max = false;
        float max_height = 0.0f;
        CollisionEntry *max_entry = NULL;
        
        Entries::const_iterator ei;
        for (ei = entries.begin(); ei != entries.end(); ++ei) {
          CollisionEntry *entry = (*ei);
          nassertr(entry != (CollisionEntry *)NULL, false);
          nassertr(from_node_path == entry->get_from_node_path(), false);
          
          if (entry->has_surface_point()) {
            LPoint3f point = entry->get_surface_point(def._target);
            if (collide_cat.is_debug()) {
              collide_cat.debug()
                << "Intersection point detected at " << point << "\n";
            }
            
            float height = point[2];
            if (!got_max || height > max_height) {
              got_max = true;
              max_height = height;
              max_entry = entry;
            }
          }
        }

        // Record a collision with the topmost element for the
        // CollisionHandlerEvent base class.
        _current_colliding.insert(max_entry);

        // Now set our height accordingly.
        float adjust = max_height + _offset;
        #else
        float max_height = set_highest_collision(def._target, from_node_path, entries);

        // Now set our height accordingly.
        float adjust = max_height + _offset;        
        #endif
        if (!IS_THRESHOLD_ZERO(adjust, 0.001)) {
          if (collide_cat.is_debug()) {
            collide_cat.debug()
              << "Adjusting height by " << adjust << "\n";
          }
          
          if (adjust < 0.0f && _max_velocity != 0.0f) {
            float max_adjust =
              _max_velocity * ClockObject::get_global_clock()->get_dt();
            adjust = max(adjust, -max_adjust);
          }

          CPT(TransformState) trans = def._target.get_transform();
          LVecBase3f pos = trans->get_pos();
          pos[2] += adjust;
          def._target.set_transform(trans->set_pos(pos));
          def.updated_transform();

          apply_linear_force(def, LVector3f(0.0f, 0.0f, adjust));
        } else {
          if (collide_cat.is_spam()) {
            collide_cat.spam()
              << "Leaving height unchanged.\n";
          }
        }
      }
    }
  }

  return okflag;
}

////////////////////////////////////////////////////////////////////
//     Function: CollisionHandlerFloor::apply_linear_force
//       Access: Protected, Virtual
//  Description: 
////////////////////////////////////////////////////////////////////
void CollisionHandlerFloor::
apply_linear_force(ColliderDef &def, const LVector3f &force) {
}
