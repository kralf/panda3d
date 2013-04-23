// Filename: odeGeom.cxx
// Created by:  joswilso (27Dec06)
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

#include "config_ode.h"
#include "odeGeom.h"
#include "odeBoxGeom.h"
#include "odeCylinderGeom.h"
#include "odeCappedCylinderGeom.h"
#include "odePlaneGeom.h"
#include "odeRayGeom.h"
#include "odeSphereGeom.h"
#include "odeTriMeshGeom.h"
#include "odeSimpleSpace.h"
#include "odeHashSpace.h"
#include "odeQuadTreeSpace.h"
#include "odeContact.h"

#ifdef HAVE_PYTHON
  #include "py_panda.h"
  #include "typedReferenceCount.h"
  #ifndef CPPPARSER
  #ifdef __GNUC__
    extern EXPCL_PANDAODE Dtool_PyTypedObject Dtool_OdeContact __attribute__((weak));
  #else
    extern EXPCL_PANDAODE Dtool_PyTypedObject Dtool_OdeContact;
  #endif  // __GNUC__
  #endif  // CPPPARSER
#endif

//OdeGeom::GeomSurfaceMap OdeGeom::_geom_surface_map;
//OdeGeom::GeomCollideIdMap OdeGeom::_geom_collide_id_map;
TypeHandle OdeGeom::_type_handle;

OdeGeom::
OdeGeom(dGeomID id) :
#ifdef HAVE_PYTHON
  _python_callback(NULL),
#endif
  _id(id) {
  odegeom_cat.debug() << get_type() << "(" << _id << ")\n";
}

OdeGeom::
~OdeGeom() {
  odegeom_cat.debug() << "~" << get_type() << "(" << _id << ")\n";
  /*  
  GeomSurfaceMap::iterator iter = _geom_surface_map.find(this->get_id());
  if (iter != _geom_surface_map.end()) {
    _geom_surface_map.erase(iter);
  }
      
  GeomCollideIdMap::iterator iter2 = _geom_collide_id_map.find(this->get_id());
  if (iter2 != _geom_collide_id_map.end()) {
    _geom_collide_id_map.erase(iter2);
  }
  */
}

/*
int OdeGeom::
get_surface_type() 
{
  return get_space().get_surface_type(this->get_id());
}

int OdeGeom::
get_collide_id() 
{
  return get_space().get_collide_id(this->get_id());
}

void OdeGeom::
set_surface_type(int surface_type) 
{
    get_space().set_surface_type(surface_type, this->get_id());
}

int OdeGeom::
set_collide_id(int collide_id) 
{
    return get_space().set_collide_id(collide_id, this->get_id());
}


int OdeGeom::
test_collide_id(int collide_id) 
{
    
    odegeom_cat.debug() << "test_collide_id start" << "\n";
    int first = get_space().set_collide_id(collide_id, this->get_id());
    odegeom_cat.debug() << "returns" << first << "\n";
    odegeom_cat.debug() << "test_collide_id middle" << "\n";
    int test = get_space().get_collide_id(this->get_id());
    odegeom_cat.debug() << "test_collide_id stop" << "\n";
    return test;
}
*/

void OdeGeom::
destroy() {
  if (get_class() == OdeTriMeshGeom::get_geom_class()) {
    OdeTriMeshData::unlink_data(_id);
  }
  dGeomDestroy(_id);
}

OdeSpace OdeGeom::
get_space() const {
  return OdeSpace(dGeomGetSpace(_id));
}


void OdeGeom::
write(ostream &out, unsigned int indent) const {
  #ifndef NDEBUG //[
  out.width(indent); 
  out << get_type() << "(id = " << _id << ")";
  #endif //] NDEBUG
}

OdeBoxGeom OdeGeom::
convert_to_box() const {
  nassertr(_id != 0, OdeBoxGeom((dGeomID)0));
  nassertr(get_class() == GC_box, OdeBoxGeom((dGeomID)0));
  return OdeBoxGeom(_id);
}

OdeCappedCylinderGeom OdeGeom::
convert_to_capped_cylinder() const {
  nassertr(_id != 0, OdeCappedCylinderGeom((dGeomID)0));
  nassertr(get_class() == GC_capped_cylinder, OdeCappedCylinderGeom((dGeomID)0));
  return OdeCappedCylinderGeom(_id);
}

/*
OdeConvexGeom OdeGeom::
convert_to_convex() const {
  nassertr(_id != 0, OdeConvexGeom((dGeomID)0));
  nassertr(get_class() == GC_convex, OdeConvexGeom((dGeomID)0));
  return OdeConvexGeom(_id);
}
*/

OdeCylinderGeom OdeGeom::
convert_to_cylinder() const {
  nassertr(_id != 0, OdeCylinderGeom((dGeomID)0));
  nassertr(get_class() == GC_cylinder, OdeCylinderGeom((dGeomID)0));
  return OdeCylinderGeom(_id);
}

/*
OdeHeightfieldGeom OdeGeom::
convert_to_heightfield() const {
  nassertr(_id != 0, OdeHeightfieldGeom((dGeomID)0));
  nassertr(get_class() == GC_heightfield, OdeHeightfieldGeom((dGeomID)0));
  return OdeHeightfieldGeom(_id);
}
*/

OdePlaneGeom OdeGeom::
convert_to_plane() const {
  nassertr(_id != 0, OdePlaneGeom((dGeomID)0));
  nassertr(get_class() == GC_plane, OdePlaneGeom((dGeomID)0));
  return OdePlaneGeom(_id);
}

OdeRayGeom OdeGeom::
convert_to_ray() const {
  nassertr(_id != 0, OdeRayGeom((dGeomID)0));
  nassertr(get_class() == GC_ray, OdeRayGeom((dGeomID)0));
  return OdeRayGeom(_id);
}

OdeSphereGeom OdeGeom::
convert_to_sphere() const {
  nassertr(_id != 0, OdeSphereGeom((dGeomID)0));
  nassertr(get_class() == GC_sphere, OdeSphereGeom((dGeomID)0));
  return OdeSphereGeom(_id);
}

OdeTriMeshGeom OdeGeom::
convert_to_tri_mesh() const {
  nassertr(_id != 0, OdeTriMeshGeom((dGeomID)0));
  nassertr(get_class() == GC_tri_mesh, OdeTriMeshGeom((dGeomID)0));
  return OdeTriMeshGeom(_id);
}

OdeSimpleSpace OdeGeom::
convert_to_simple_space() const {
  nassertr(_id != 0, OdeSimpleSpace((dSpaceID)0));
  nassertr(get_class() == GC_simple_space, OdeSimpleSpace((dSpaceID)0));
  return OdeSimpleSpace((dSpaceID)_id);
}

OdeHashSpace OdeGeom::
convert_to_hash_space() const {
  nassertr(_id != 0, OdeHashSpace((dSpaceID)0));
  nassertr(get_class() == GC_hash_space, OdeHashSpace((dSpaceID)0));
  return OdeHashSpace((dSpaceID)_id);
}

OdeQuadTreeSpace OdeGeom::
convert_to_quad_tree_space() const {
  nassertr(_id != 0, OdeQuadTreeSpace((dSpaceID)0));
  nassertr(get_class() == GC_quad_tree_space, OdeQuadTreeSpace((dSpaceID)0));
  return OdeQuadTreeSpace((dSpaceID)_id);
}

#ifdef HAVE_PYTHON
int OdeGeom::
collide(PyObject* callback) {
  nassertr(callback != NULL, -1);
  if (_python_callback)
    Py_XDECREF(_python_callback);
  if (!PyCallable_Check(callback)) {
    PyErr_Format(PyExc_TypeError, "'%s' object is not callable",
      callback->ob_type->tp_name);
    _python_callback = NULL;
    dGeomSetData(_id, _python_callback);
    return -1;
  } else if (_id == NULL) {
    PyErr_Format(PyExc_TypeError, "OdeGeom is not valid!");
    _python_callback = NULL;
    return -1;
  } else {
    Py_XINCREF(callback);
    _python_callback = (PyObject*) callback;
    dGeomSetData(_id, _python_callback);
    return 0;
  }
}

void OdeGeom::
callback(dGeomID id, dContact& contact) {
  PyObject* callback = (PyObject*) dGeomGetData(id);
  if (callback) {
    OdeContact *c1 = new OdeContact(contact);
    PyObject *p1 = DTool_CreatePyInstanceTyped(c1, Dtool_OdeContact, true,
      false, c1->get_type_index());
    PyObject* result = PyEval_CallFunction(callback, "(O)", p1);
    if (!result) {
      odegeom_cat.error() <<
        "An error occurred while calling python function!\n";
      PyErr_Print();
    } else {
      Py_DECREF(result);
    }
    contact = *c1->get_contact_ptr();
    Py_XDECREF(p1);
  }
}
#endif

OdeGeom::
operator bool () const {
  return (_id != NULL);
}

