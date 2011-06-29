############################################################################
#    Copyright (C) 2009 by Ralf 'Decan' Kaestner                           #
#    ralf.kaestner@gmail.com                                               #
#                                                                          #
#    This program is free software; you can redistribute it and#or modify  #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

include(ReMakeGenerate)

remake_minimum_required(VERSION 0.3)

### \brief Panda3D code generation macros
#   The Panda3D module defines convenience macros for generating the Panda3D
#   Python bindings.

remake_set(PANDA3D_INTERROGATE_DIR
  ${CMAKE_BINARY_DIR}/Panda3DFiles/Panda3DInterrogate)
remake_set(PANDA3D_MODULE_DIR ${CMAKE_BINARY_DIR}/Panda3DFiles/Panda3DModules)

define_property(DIRECTORY PROPERTY PANDA3D_INTERROGATE_INCLUDE_DIRECTORIES
  INHERITED
  BRIEF_DOCS "List of Panda3D Interrogate include file directories."
  FULL_DOCS "This property specifies the list of directories given so"
    "far to the panda3d_interrogate_include() macro.")

### \brief Generate Panda3D Interrogate sources from a target.
#   This macro specifies code generation rules for the Panda3D Interrogate
#   generator. It attempts to call remake_generate_custom() with the
#   appropriate arguments.
#   \required[value] target The name of the build target to generate the
#     interrogated source code from.
#   \required[list] glob A list of glob expressions that are resolved
#     in order to find the input source files for Interrogate, defaulting
#     to *.h and *.cxx.
#   \optional[value] COMMAND:command The generator command that will be
#     passed to remake_generate_custom() to generate the Interrogate
#     sources, defaulting to interrogate.
#   \optional[value] MODULE:module The name of the Panda3D module that
#     will be be passed to Interrogate, defaults to the target name.
#   \optional[list] EXCLUDE:glob An optional list of glob expressions
#     resolving to those files that shall be excluded from the Interrogate
#     sources.
macro(panda3d_interrogate panda3d_target)
  remake_arguments(PREFIX panda3d_ VAR COMMAND VAR MODULE LIST EXCLUDE
    ARGN globs ${ARGN})
  remake_set(panda3d_module SELF DEFAULT ${panda3d_target})
  remake_set(panda3d_command SELF DEFAULT interrogate)
  remake_set(panda3d_globs SELF DEFAULT *.h *.cxx)

  string(TOUPPER ${panda3d_module} panda3d_building)
  remake_set(panda3d_args -fnames -string -refcount -assert -python-native
    -srcdir ${CMAKE_CURRENT_SOURCE_DIR} -module ${panda3d_module} -library
    ${panda3d_target})
  remake_set(panda3d_defs -Dvolatile -Dmutable -DCPPPARSER -D__STDC__=1
    -D__cplusplus -D__inline -D__const=const -DBUILDING_${panda3d_building})
  if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    remake_list_push(panda3d_defs -D_LP64)
  else(CMAKE_SIZEOF_VOID_P EQUAL 8)
    remake_list_push(panda3d_defs -D__i386__)
  endif(CMAKE_SIZEOF_VOID_P EQUAL 8)
  if(CMAKE_BUILD_TYPE)
    string(TOUPPER "CMAKE_CXX_FLAGS_${CMAKE_BUILD_TYPE}" panda3d_build_flags)
    string(REPLACE " -" ";-" panda3d_flags "${${panda3d_build_flags}}")
    foreach(panda3d_flag ${panda3d_flags})
      if(panda3d_flag MATCHES ^-D)
        remake_list_push(panda3d_defs ${panda3d_flag})
      endif(panda3d_flag MATCHES ^-D)
    endforeach(panda3d_flag)
  endif(CMAKE_BUILD_TYPE)

  remake_set(panda3d_include_flags)
  remake_set(panda3d_interrogate_include_flags)

  get_property(panda3d_interrogate_include_dirs DIRECTORY PROPERTY
    PANDA3D_INTERROGATE_INCLUDE_DIRECTORIES)
  foreach(panda3d_interrogate_include_dir ${panda3d_interrogate_include_dirs})
    remake_list_push(panda3d_include_flags
      "-I${panda3d_interrogate_include_dir}")
    remake_list_push(panda3d_interrogate_include_flags
      "-S${panda3d_interrogate_include_dir}")
  endforeach(panda3d_interrogate_include_dir)

  get_property(panda3d_include_dirs DIRECTORY PROPERTY INCLUDE_DIRECTORIES)
  foreach(panda3d_include_dir ${panda3d_include_dirs})
    remake_list_push(panda3d_include_flags "-I${panda3d_include_dir}")
  endforeach(panda3d_include_dir)

  remake_file_glob(panda3d_input ${panda3d_globs} EXCLUDE ${panda3d_exclude})
  list(SORT panda3d_input)

  remake_file(panda3d_dir
    ${PANDA3D_INTERROGATE_DIR}/${panda3d_module}/${panda3d_target})
  if(NOT EXISTS ${panda3d_dir})
    remake_file_mkdir(${panda3d_dir})
  endif(NOT EXISTS ${panda3d_dir})
  remake_file(panda3d_file ${panda3d_dir}/command)
  remake_file_create(${panda3d_file})
  remake_file_write(${panda3d_file} ${panda3d_command})
  remake_file(panda3d_file ${panda3d_dir}/arguments)
  remake_file_create(${panda3d_file})
  remake_file_write(${panda3d_file} ${panda3d_args} ${panda3d_defs}
    ${panda3d_include_flags} ${panda3d_interrogate_include_flags})
  remake_file(panda3d_file ${panda3d_dir}/input)
  remake_file_create(${panda3d_file})
  remake_file_write(${panda3d_file} ${panda3d_input})
endmacro(panda3d_interrogate)

### \brief Add Panda3D Interrogate module sources for a target.
#   This macro specifies code generation rules for the Panda3D Interrogate
#   module generator. It attempts to call remake_generate_custom() with the
#   appropriate arguments.
#   \required[value] target The name of the build target to add the
#     interrogated module source code for.
#   \optional[value] COMMAND:command The generator command that will be
#     passed to remake_generate_custom() to generate the Interrogate module
#     sources, defaulting to interrogate_module.
#   \optional[value] MODULE:module The name of the Panda3D module that
#     will be be passed to Interrogate, defaults to the target name.
macro(panda3d_interrogate_module panda3d_target)
  remake_arguments(PREFIX panda3d_ VAR COMMAND VAR MODULE ${ARGN})
  remake_set(panda3d_command SELF DEFAULT interrogate_module)
  remake_set(panda3d_module SELF DEFAULT ${panda3d_target})

  remake_file(panda3d_dir ${PANDA3D_MODULE_DIR}/${panda3d_module})
  if(NOT EXISTS ${panda3d_dir})
    remake_file_mkdir(${panda3d_dir})
  endif(NOT EXISTS ${panda3d_dir})
  remake_file(panda3d_file ${panda3d_dir}/target)
  remake_file_create(${panda3d_file})
  remake_file_write(${panda3d_file} ${panda3d_target})
  remake_file(panda3d_file ${panda3d_dir}/directory)
  remake_file_create(${panda3d_file})
  remake_file_write(${panda3d_file} ${CMAKE_CURRENT_BINARY_DIR})

  remake_file(panda3d_dir ${PANDA3D_INTERROGATE_DIR}/${panda3d_module})
  remake_file_glob(panda3d_dirs ${panda3d_dir}/* DIRECTORIES)

  remake_unset(panda3d_inputs panda3d_sources)
  foreach(panda3d_dir ${panda3d_dirs})
    get_filename_component(panda3d_igate_target ${panda3d_dir} NAME)
    remake_file_read(panda3d_cmd ${panda3d_dir}/command)
    remake_file_read(panda3d_args ${panda3d_dir}/arguments)
    remake_file_read(panda3d_input ${panda3d_dir}/input)
    remake_set(panda3d_source
      ${CMAKE_CURRENT_BINARY_DIR}/${panda3d_igate_target}_igate.cxx)
    remake_set(panda3d_other
      ${CMAKE_CURRENT_BINARY_DIR}/${panda3d_igate_target}.in)

    remake_generate_custom(Interrogate
      ${panda3d_cmd} ${panda3d_args} -oc %SOURCES% -od %OTHERS% %INPUT%
      INPUT ${panda3d_input}
      SOURCES ${panda3d_source}
      OTHERS ${panda3d_other})

    remake_list_push(panda3d_inputs ${panda3d_other})
    remake_list_push(panda3d_sources ${panda3d_source})
  endforeach(panda3d_dir)

  remake_set(panda3d_args -q -python-native -module ${panda3d_module}
    -library ${panda3d_target})
  remake_generate_custom("Interrogate module"
    ${panda3d_command} ${panda3d_args} -oc %SOURCES% %INPUT%
    TARGET ${panda3d_target}
    INPUT ${panda3d_inputs} GENERATED
    SOURCES ${panda3d_target}_module.cxx)
  remake_target_add_sources(${panda3d_target} ${panda3d_sources})
  set_source_files_properties(${panda3d_sources} PROPERTIES GENERATED ON)
endmacro(panda3d_interrogate_module)

### \brief Define a Python package for the Panda3D modules.
#   This macro defines a Python package to contain generated Panda3D Python
#   modules. It attempts to call remake_generate_custom() and
#   remake_python_package() with the appropriate arguments.
#   \optional[value] NAME:name The optional name of the Python package to
#     be defined, defaults to the package name conversion of
#     ${REMAKE_COMPONENT}-${REMAKE_PYTHON_COMPONENT_SUFFIX}.
#   \optional[value] COMMAND:command The generator command that will be
#     passed to remake_generate_custom() to generate the Python module
#     sources, defaulting to gen_pycode.
#   \optional[list] PATH:dir An optional list of path names that will be
#     prepended to the PYTHONPATH environment variable.
macro(panda3d_python_package)
  remake_arguments(PREFIX panda3d_ VAR COMMAND VAR NAME LIST PATH ${ARGN})
  remake_set(panda3d_command SELF DEFAULT gen_pycode)
  remake_component_name(panda3d_default_component ${REMAKE_COMPONENT}
    ${REMAKE_PYTHON_COMPONENT_SUFFIX})
  remake_python_package_name(panda3d_default_name ${panda3d_default_component})
  remake_set(panda3d_name SELF DEFAULT ${panda3d_default_name})
  remake_set(panda3d_paths ${panda3d_path})

  remake_set(panda3d_others ${CMAKE_CURRENT_BINARY_DIR}/__init__.py
    ${CMAKE_CURRENT_BINARY_DIR}/Modules.py)
  remake_python_package(NAME ${panda3d_name}
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    ${panda3d_others} GENERATED)

  remake_unset(panda3d_targets)
  remake_file_glob(panda3d_dirs ${PANDA3D_MODULE_DIR}/* DIRECTORIES)
  foreach(panda3d_dir ${panda3d_dirs})
    remake_file(panda3d_file ${panda3d_dir}/target)
    remake_file_read(panda3d_target ${panda3d_file})
    remake_file(panda3d_file ${panda3d_dir}/directory)
    remake_file_read(panda3d_module_path ${panda3d_file})

    remake_list_push(panda3d_targets ${panda3d_target})
    remake_list_push(panda3d_paths ${panda3d_module_path})
    remake_list_push(panda3d_sources
      ${CMAKE_CURRENT_BINARY_DIR}/${panda3d_target}_module.py)
  endforeach(panda3d_dir)

  string(REPLACE ";" ":" panda3d_python_path "${panda3d_paths}")
  remake_generate_custom("Python module"
    PYTHONPATH=${panda3d_python_path} python ${panda3d_command} -q -r %INPUT%
    INPUT ${panda3d_targets} GENERATED
    SOURCES ${panda3d_sources}
    OTHERS ${panda3d_others})
  remake_python_add_modules(PACKAGE ${panda3d_name}
    ${panda3d_sources} GENERATED)
endmacro(panda3d_python_package)

### \brief Add directories to the Interrogate include path of Panda3D.
#   This macro adds a list of directories to the include path of Panda3D's
#   Interrogate. The include paths are stored as directory property and
#   will later be collected during a call to panda3d_interrogate().
#   \optional[list] glob An optional list of glob expressions that are
#     resolved in order to find the directories to be added to the
#     Interrogate include path, defaults to the current directory.
macro(panda3d_interrogate_include)
  remake_arguments(PREFIX panda3d_ ARGN globs ${ARGN})
  remake_set(panda3d_globs SELF DEFAULT ${CMAKE_CURRENT_SOURCE_DIR})

  remake_file_glob(panda3d_dirs DIRECTORIES ${panda3d_globs})
  get_property(panda3d_system_include_dirs DIRECTORY PROPERTY
    PANDA3D_INTERROGATE_INCLUDE_DIRECTORIES)
  set_property(DIRECTORY PROPERTY PANDA3D_INTERROGATE_INCLUDE_DIRECTORIES
    ${panda3d_system_include_dirs} ${panda3d_dirs})
endmacro(panda3d_interrogate_include)
