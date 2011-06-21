// Filename: interrogate.cxx
// Created by:  drose (31Jul00)
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

#include "interrogate.h"

CPPParser parser;

Filename output_code_filename;
Filename output_data_filename;
string output_data_basename;

bool output_module_specific = false;
bool output_function_pointers = false;
bool output_function_names = false;
bool convert_strings = false;
bool manage_reference_counts = false;
bool watch_asserts = false;
bool true_wrapper_names = false;
bool build_c_wrappers = false;
bool build_python_wrappers = false;
bool build_python_obj_wrappers = false;
bool build_python_native = false;
bool track_interpreter = false;
bool save_unique_names = false;
bool no_database = false;
bool generate_spam = false;
bool left_inheritance_requires_upcast = true;

CPPVisibility min_vis = V_published;
string library_name;
string module_name;
