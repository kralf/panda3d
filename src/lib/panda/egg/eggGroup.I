// Filename: eggGroup.I
// Created by:  drose (16Jan99)
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
//     Function: EggGroup::get_group_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE EggGroup::GroupType EggGroup::
get_group_type() const {
  return (GroupType)(_flags & F_group_type);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::is_instance_type
//       Access: Published
//  Description: Returns true if this group is an instance type node;
//               i.e. it begins the root of a local coordinate space.
//               This is not related to instancing (multiple copies of
//               a node in a scene graph).
//
//               This also includes the case of the node including a
//               billboard flag without an explicit center, which
//               implicitly makes the node behave like an instance.
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
is_instance_type() const {
  return 
    (get_group_type() == GT_instance) ||
    (get_billboard_type() != BT_none && !has_billboard_center());
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_billboard_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_billboard_type(BillboardType type) {
  // Make sure the user didn't give us any stray bits.
  nassertv((type & ~F_billboard_type)==0);
  _flags = (_flags & ~F_billboard_type) | type;
  // This may change the transform space of this node.
  update_under(0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_billboard_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE EggGroup::BillboardType EggGroup::
get_billboard_type() const {
  return (BillboardType)(_flags & F_billboard_type);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_billboard_center
//       Access: Published
//  Description: Sets the point around which the billboard will
//               rotate, if this node contains a billboard
//               specification.
//
//               If a billboard type is given but no billboard_center
//               is specified, then the group node is treated as an
//               <Instance>, and the billboard rotates around the
//               origin.  If, however, a billboard_center is
//               specified, then the group node is *not* treated as an
//               <Instance>, and the billboard rotates around the
//               specified point.
//
//               The point is in the same coordinate system as the
//               vertices of this node: usually global, but possibly
//               local if there is an <Instance> somewhere above.
//               Specifically, this is the coordinate system defined
//               by get_vertex_frame().
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_billboard_center(const LPoint3d &billboard_center) {
  _billboard_center = billboard_center;
  _flags2 |= F2_billboard_center;
  // This may change the transform space of this node.
  update_under(0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_billboard_center
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_billboard_center() {
  _flags2 &= ~F2_billboard_center;
  // This may change the transform space of this node.
  update_under(0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::has_billboard_center
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
has_billboard_center() const {
  return (_flags2 & F2_billboard_center) != 0;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_billboard_center
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE const LPoint3d &EggGroup::
get_billboard_center() const {
  nassertr(has_billboard_center(), _billboard_center);
  return _billboard_center;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_cs_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_cs_type(CollisionSolidType type) {
  // Make sure the user didn't give us any stray bits.
  nassertv((type & ~F_cs_type)==0);
  _flags = (_flags & ~F_cs_type) | type;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_cs_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE EggGroup::CollisionSolidType EggGroup::
get_cs_type() const {
  return (CollisionSolidType)(_flags & F_cs_type);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_collision_name
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_collision_name(const string &collision_name) {
  _collision_name = collision_name;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_collision_name
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_collision_name() {
  _collision_name = "";
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::has_collision_name
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
has_collision_name() const {
  return !_collision_name.empty();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_collision_name
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE const string &EggGroup::
get_collision_name() const {
  return _collision_name;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_collide_flags
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_collide_flags(int flags) {
  // Make sure the user didn't give us any stray bits.
  nassertv((flags & ~F_collide_flags)==0);
  _flags = (_flags & ~F_collide_flags) | flags;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_collide_flags
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE EggGroup::CollideFlags EggGroup::
get_collide_flags() const {
  return (EggGroup::CollideFlags)(_flags & F_collide_flags);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_dcs_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_dcs_type(EggGroup::DCSType type) {
  // Make sure the user didn't give us any stray bits.
  nassertv((type & ~F2_dcs_type)==0);
  _flags2 = (_flags2 & ~F2_dcs_type) | type;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_dcs_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE EggGroup::DCSType EggGroup::
get_dcs_type() const {
  return (DCSType)(_flags2 & F2_dcs_type);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::has_dcs_type
//       Access: Published
//  Description: Returns true if the specified DCS type is not
//               DC_none and not DC_unspecified.
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
has_dcs_type() const {
  DCSType type = get_dcs_type();
  return (type != DC_none && type != DC_unspecified);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_dart_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_dart_type(EggGroup::DartType type) {
  // Make sure the user didn't give us any stray bits.
  nassertv((type & ~F_dart_type)==0);
  _flags = (_flags & ~F_dart_type) | type;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_dart_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE EggGroup::DartType EggGroup::
get_dart_type() const {
  return (DartType)(_flags & F_dart_type);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_switch_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_switch_flag(bool flag) {
  if (flag) {
    _flags |= F_switch_flag;
  } else {
    _flags &= ~F_switch_flag;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_switch_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
get_switch_flag() const {
  return ((_flags & F_switch_flag) != 0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_switch_fps
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_switch_fps(double fps) {
  _fps = fps;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_switch_fps
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE double EggGroup::
get_switch_fps() const {
  return _fps;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::add_object_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
add_object_type(const string &object_type) {
  _object_types.push_back(object_type);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_object_types
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_object_types() {
  _object_types.clear();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_num_object_types
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE int EggGroup::
get_num_object_types() const {
  return _object_types.size();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_object_type
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE string EggGroup::
get_object_type(int index) const {
  nassertr(index >= 0 && index < (int)_object_types.size(), string());
  return _object_types[index];
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_model_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_model_flag(bool flag) {
  if (flag) {
    _flags |= F_model_flag;
  } else {
    _flags &= ~F_model_flag;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_model_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
get_model_flag() const {
  return ((_flags & F_model_flag) != 0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_texlist_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_texlist_flag(bool flag) {
  if (flag) {
    _flags |= F_texlist_flag;
  } else {
    _flags &= ~F_texlist_flag;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_texlist_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
get_texlist_flag() const {
  return ((_flags & F_texlist_flag) != 0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_nofog_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_nofog_flag(bool flag) {
  if (flag) {
    _flags |= F_nofog_flag;
  } else {
    _flags &= ~F_nofog_flag;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_nofog_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
get_nofog_flag() const {
  return ((_flags & F_nofog_flag) != 0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_decal_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_decal_flag(bool flag) {
  if (flag) {
    _flags |= F_decal_flag;
  } else {
    _flags &= ~F_decal_flag;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_decal_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
get_decal_flag() const {
  return ((_flags & F_decal_flag) != 0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_direct_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_direct_flag(bool flag) {
  if (flag) {
    _flags |= F_direct_flag;
  } else {
    _flags &= ~F_direct_flag;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_direct_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
get_direct_flag() const {
  return ((_flags & F_direct_flag) != 0);
}


////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_portal_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_portal_flag(bool flag) {
  if (flag) {
    _flags2 |= F2_portal_flag;
  } else {
    _flags2 &= ~F2_portal_flag;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_portal_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
get_portal_flag() const {
  return ((_flags2 & F2_portal_flag) != 0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_polylight_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_polylight_flag(bool flag) {
  if (flag) {
    _flags2 |= F2_polylight_flag;
  } else {
    _flags2 &= ~F2_polylight_flag;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_polylight_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
get_polylight_flag() const {
  return ((_flags2 & F2_polylight_flag) != 0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_indexed_flag
//       Access: Published
//  Description: If this flag is true, geometry at this node and below
//               will be generated as indexed geometry.
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_indexed_flag(bool flag) {
  if (flag) {
    _flags2 |= F2_indexed_flag;
  } else {
    _flags2 &= ~F2_indexed_flag;
  }
  _flags2 |= F2_has_indexed_flag;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_indexed_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_indexed_flag() {
  _flags2 &= ~(F2_indexed_flag | F2_has_indexed_flag);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::has_indexed_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
has_indexed_flag() const {
  return (_flags2 & F2_has_indexed_flag) != 0;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_indexed_flag
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
get_indexed_flag() const {
  nassertr(has_indexed_flag(), false);
  return ((_flags2 & F2_indexed_flag) != 0);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_collide_mask(CollideMask mask) {
  _collide_mask = mask;
  _flags2 |= F2_collide_mask;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_collide_mask() {
  _flags2 &= ~F2_collide_mask;
  _collide_mask = CollideMask::all_off();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::has_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
has_collide_mask() const {
  return (_flags2 & F2_collide_mask) != 0;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE CollideMask EggGroup::
get_collide_mask() const {
  return _collide_mask;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_from_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_from_collide_mask(CollideMask mask) {
  _from_collide_mask = mask;
  _flags2 |= F2_from_collide_mask;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_from_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_from_collide_mask() {
  _flags2 &= ~F2_from_collide_mask;
  _from_collide_mask = CollideMask::all_off();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::has_from_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
has_from_collide_mask() const {
  return (_flags2 & F2_from_collide_mask) != 0;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_from_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE CollideMask EggGroup::
get_from_collide_mask() const {
  return _from_collide_mask;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_into_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_into_collide_mask(CollideMask mask) {
  _into_collide_mask = mask;
  _flags2 |= F2_into_collide_mask;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_into_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_into_collide_mask() {
  _flags2 &= ~F2_into_collide_mask;
  _into_collide_mask = CollideMask::all_off();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::has_into_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
has_into_collide_mask() const {
  return (_flags2 & F2_into_collide_mask) != 0;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_into_collide_mask
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE CollideMask EggGroup::
get_into_collide_mask() const {
  return _into_collide_mask;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_blend_mode
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_blend_mode(EggGroup::BlendMode blend_mode) {
  _blend_mode = blend_mode;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_blend_mode
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE EggGroup::BlendMode EggGroup::
get_blend_mode() const {
  return _blend_mode;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_blend_operand_a
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_blend_operand_a(EggGroup::BlendOperand blend_operand_a) {
  _blend_operand_a = blend_operand_a;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_blend_operand_a
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE EggGroup::BlendOperand EggGroup::
get_blend_operand_a() const {
  return _blend_operand_a;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_blend_operand_b
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_blend_operand_b(EggGroup::BlendOperand blend_operand_b) {
  _blend_operand_b = blend_operand_b;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_blend_operand_b
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE EggGroup::BlendOperand EggGroup::
get_blend_operand_b() const {
  return _blend_operand_b;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_blend_color
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_blend_color(const Colorf &blend_color) {
  _blend_color = blend_color;
  _flags2 |= F2_has_blend_color;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_blend_color
//       Access: Published
//  Description: Removes the blend color specification.
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_blend_color() {
  _blend_color = Colorf::zero();
  _flags2 &= ~F2_has_blend_color;
}
 
////////////////////////////////////////////////////////////////////
//     Function: EggGroup::has_blend_color
//       Access: Published
//  Description: Returns true if the blend color has been specified,
//               false otherwise.
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
has_blend_color() const {
  return (_flags2 & F2_has_blend_color) != 0;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_blend_color
//       Access: Published
//  Description: Returns the blend color if one has been specified, or
//               (0, 0, 0, 0) if one has not.
////////////////////////////////////////////////////////////////////
INLINE const Colorf &EggGroup::
get_blend_color() const {
  return _blend_color;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_lod
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_lod(const EggSwitchCondition &lod) {
  _lod = lod.make_copy();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_lod
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_lod() {
  _lod = NULL;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::has_lod
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
has_lod() const {
  return (_lod != (EggSwitchCondition *)NULL);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_lod
//       Access: Published
//  Description:
////////////////////////////////////////////////////////////////////
INLINE const EggSwitchCondition &EggGroup::
get_lod() const {
  return *_lod;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_tag
//       Access: Published
//  Description: Associates a user-defined value with a user-defined
//               key which is stored on the node.  This value has no
//               meaning to Panda; but it is stored indefinitely on
//               the node until it is requested again.  This value
//               will be copied to the PandaNode that is created for
//               this particular EggGroup if the egg file is loaded as
//               a scene.
//
//               Each unique key stores a different string value.
//               There is no effective limit on the number of
//               different keys that may be stored or on the length of
//               any one key's value.
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_tag(const string &key, const string &value) {
  _tag_data[key] = value;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_tag
//       Access: Published
//  Description: Retrieves the user-defined value that was previously
//               set on this node for the particular key, if any.  If
//               no value has been previously set, returns the empty
//               string.
////////////////////////////////////////////////////////////////////
INLINE string EggGroup::
get_tag(const string &key) const {
  TagData::const_iterator ti;
  ti = _tag_data.find(key);
  if (ti != _tag_data.end()) {
    return (*ti).second;
  }
  return string();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::has_tag
//       Access: Published
//  Description: Returns true if a value has been defined on this node
//               for the particular key (even if that value is the
//               empty string), or false if no value has been set.
////////////////////////////////////////////////////////////////////
INLINE bool EggGroup::
has_tag(const string &key) const {
  TagData::const_iterator ti;
  ti = _tag_data.find(key);
  return (ti != _tag_data.end());
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_tag
//       Access: Published
//  Description: Removes the value defined for this key on this
//               particular node.  After a call to clear_tag(),
//               has_tag() will return false for the indicated key.
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_tag(const string &key) {
  _tag_data.erase(key);
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::get_default_pose
//       Access: Published
//  Description: Returns a read-only accessor to the initial pose
//               transform.  This is the <DefaultPose> entry for a
//               Joint, and defines only the initial transform pose
//               for the unanimated joint; it has nothing to do with
//               the group's <Transform> entry, which defines the
//               (eventual) space of the group's vertices.
////////////////////////////////////////////////////////////////////
INLINE const EggTransform &EggGroup::
get_default_pose() const {
  return _default_pose;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::modify_default_pose
//       Access: Published
//  Description: Returns a writable accessor to the initial pose
//               transform.  This is the <DefaultPose> entry for a
//               Joint, and defines only the initial transform pose
//               for the unanimated joint; it has nothing to do with
//               the group's <Transform> entry, which defines the
//               (eventual) space of the group's vertices.
////////////////////////////////////////////////////////////////////
INLINE EggTransform &EggGroup::
modify_default_pose() {
  return _default_pose;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::set_default_pose
//       Access: Published
//  Description: Replaces the initial pose transform.  This is the
//               <DefaultPose> entry for a Joint, and defines only the
//               initial transform pose for the unanimated joint; it
//               has nothing to do with the group's <Transform> entry,
//               which defines the (eventual) space of the group's
//               vertices.
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
set_default_pose(const EggTransform &transform) {
  _default_pose = transform;
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::clear_default_pose
//       Access: Published
//  Description: Removes the initial pose transform.  See
//               set_default_pose().
////////////////////////////////////////////////////////////////////
INLINE void EggGroup::
clear_default_pose() {
  _default_pose.clear_transform();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::tag_begin
//       Access: Public
//  Description: Returns an iterator that can, in conjunction with
//               tag_end(), be used to traverse the entire set of
//               tag keys.  Each iterator returns a pair<string,
//               string>.
//
//               This interface is not safe to use outside of
//               PANDAEGG.DLL.
////////////////////////////////////////////////////////////////////
INLINE EggGroup::TagData::const_iterator EggGroup::
tag_begin() const {
  return _tag_data.begin();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::tag_end
//       Access: Public
//  Description: Returns an iterator that can, in conjunction with
//               tag_begin(), be used to traverse the entire set of
//               tag keys.  Each iterator returns a pair<string,
//               string>.
//
//               This interface is not safe to use outside of
//               PANDAEGG.DLL.
////////////////////////////////////////////////////////////////////
INLINE EggGroup::TagData::const_iterator EggGroup::
tag_end() const {
  return _tag_data.end();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::tag_size
//       Access: Published
//  Description: Returns the number of elements between tag_begin()
//               and tag_end().
//
//               This interface is not safe to use outside of
//               PANDAEGG.DLL.
////////////////////////////////////////////////////////////////////
INLINE EggGroup::TagData::size_type EggGroup::
tag_size() const {
  return _tag_data.size();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::vref_begin
//       Access: Public
//  Description: Returns an iterator that can, in conjunction with
//               vref_end(), be used to traverse the entire set of
//               referenced vertices.  Each iterator returns a
//               pair<PT(EggVertex), double>.
//
//               This interface is not safe to use outside of
//               PANDAEGG.DLL.
////////////////////////////////////////////////////////////////////
INLINE EggGroup::VertexRef::const_iterator EggGroup::
vref_begin() const {
  return _vref.begin();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::vref_end
//       Access: Public
//  Description: Returns an iterator that can, in conjunction with
//               vref_begin(), be used to traverse the entire set of
//               referenced vertices.  Each iterator returns a
//               pair<PT(EggVertex), double>.
//
//               This interface is not safe to use outside of
//               PANDAEGG.DLL.
////////////////////////////////////////////////////////////////////
INLINE EggGroup::VertexRef::const_iterator EggGroup::
vref_end() const {
  return _vref.end();
}

////////////////////////////////////////////////////////////////////
//     Function: EggGroup::vref_size
//       Access: Published
//  Description: Returns the number of elements between vref_begin()
//               and vref_end().
//
//               This interface is not safe to use outside of
//               PANDAEGG.DLL.
////////////////////////////////////////////////////////////////////
INLINE EggGroup::VertexRef::size_type EggGroup::
vref_size() const {
  return _vref.size();
}
