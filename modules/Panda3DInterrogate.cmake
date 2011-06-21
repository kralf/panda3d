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

### \brief Panda3D Interrogate code generation macros
#   The Panda3D Interrogate module defines convenience macros for generating
#   the Panda3D Python bindings.

remake_set(PANDA3D_INTERROGATE_DIR Panda3DFiles/Panda3DInterrogate)

define_property(DIRECTORY PROPERTY PANDA3D_INTERROGATE_INCLUDE_DIRECTORIES
  INHERITED
  BRIEF_DOCS "List of Panda3D Interrogate include file directories."
  FULL_DOCS "This property specifies the list of directories given so"
    "far to the panda3d_interrogate_include() macro.")

### \brief Add Panda3D Interrogate sources for a target.
#   This macro specifies code generation rules for the Panda3D Interrogate
#   generator. It attempts to call remake_generate_custom() with the
#   appropriate arguments.
#   \required[value] target The name of the build target to add the
#     interrogated source code for.
#   \required[list] glob A list of glob expressions that are resolved
#     in order to find the input source files for Interrogate, defaulting
#     to *.h and *.cxx.
#   \optional[value] MODULE:module The name of the Panda3D module that
#     will be be passed to Interrogate, defaults to the target name.
#   \optional[list] EXCLUDE:glob An optional list of glob expressions
#     resolving to those files that shall be excluded from the Interrogate
#     sources.
macro(panda3d_interrogate panda3d_target)
  remake_arguments(PREFIX panda3d_ VAR MODULE LIST EXCLUDE ARGN globs ${ARGN})
  remake_set(panda3d_module SELF DEFAULT ${panda3d_target})
  remake_set(panda3d_globs SELF DEFAULT *.h *.cxx)

  string(TOUPPER ${panda3d_module} panda3d_building)
  remake_set(panda3d_args -fnames -string -refcount -assert -python-native
    -srcdir ${CMAKE_CURRENT_SOURCE_DIR})
  remake_set(panda3d_defs -Dvolatile -Dmutable -DCPPPARSER -D__STDC__=1
    -D__cplusplus -D__inline -D__const=const -DBUILDING_${panda3d_building})
  if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    remake_list_push(panda3d_defs -D_LP64)
  else(CMAKE_SIZEOF_VOID_P EQUAL 8)
    remake_list_push(panda3d_defs -D__i386__)
  endif(CMAKE_SIZEOF_VOID_P EQUAL 8)

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

  remake_file(panda3d_dir ${CMAKE_BINARY_DIR}/${PANDA3D_INTERROGATE_DIR})
  if(NOT EXISTS ${panda3d_dir})
    remake_file_mkdir(${panda3d_dir})
  endif(NOT EXISTS ${panda3d_dir})

  remake_generate_custom(Interrogate ${panda3d_target}
    interrogate ${panda3d_args} ${panda3d_defs}
      ${panda3d_include_flags} ${panda3d_interrogate_include_flags}
      -oc %SOURCES% -od ${panda3d_dir}/${panda3d_target}.in %INPUT%
    INPUT ${panda3d_input}
    SOURCES ${panda3d_target}_igate.cxx
    OTHERS ${panda3d_dir}/${panda3d_target}.in)
endmacro(panda3d_interrogate)

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
