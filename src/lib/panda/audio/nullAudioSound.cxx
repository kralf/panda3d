// Filename: nullAudioSound.cxx
// Created by:  skyler (June 6, 2001)
// Prior system by: cary
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

#include "nullAudioSound.h"

TypeHandle NullAudioSound::_type_handle;

namespace {
  static const string blank="";
  //  static float no_attributes [] = {0.0f,0.0f,0.0f, 0.0f,0.0f,0.0f};
}

////////////////////////////////////////////////////////////////////
//     Function: 
//       Access: 
//  Description: All of these functions are just stubs.
////////////////////////////////////////////////////////////////////
NullAudioSound::NullAudioSound() {
  // Intentionally blank.
}

NullAudioSound::~NullAudioSound() {
  // Intentionally blank.
}
  
void NullAudioSound::play() {
  // Intentionally blank.
}

void NullAudioSound::stop() {
  // Intentionally blank.
}
  
void NullAudioSound::set_loop(bool) {
  // Intentionally blank.
}

bool NullAudioSound::get_loop() const {
  return false; 
}
  
void NullAudioSound::set_loop_count(unsigned long) {
  // Intentionally blank.
}

unsigned long NullAudioSound::get_loop_count() const {
  return 0; 
}
  
void NullAudioSound::set_time(float) {
  // Intentionally blank.
}

float NullAudioSound::get_time() const {
  return 0; 
}

void NullAudioSound::set_volume(float) {
  // Intentionally blank.
}

float NullAudioSound::get_volume() const {
  return 0; 
}

void NullAudioSound::set_balance(float) {
  // Intentionally blank.
}

float NullAudioSound::get_balance() const {
  return 0; 
}

void NullAudioSound::set_play_rate(float) {
  // Intentionally blank.
}

float NullAudioSound::get_play_rate() const {
  return 0; 
}

void NullAudioSound::set_active(bool) {
  // Intentionally blank.
}

bool NullAudioSound::get_active() const {
  return false; 
}

void NullAudioSound::set_finished_event(const string& event) {
  // Intentionally blank.
}

const string& NullAudioSound::get_finished_event() const {
  return blank;
}

const string& NullAudioSound::get_name() const {
  return blank;
}

float NullAudioSound::length() const {
  return 0;
}

void NullAudioSound::set_3d_attributes(float px, float py, float pz, float vx, float vy, float vz) {
  // Intentionally blank.
}

void NullAudioSound::get_3d_attributes(float *px, float *py, float *pz, float *vx, float *vy, float *vz) {
  // Intentionally blank.
}

void NullAudioSound::set_3d_min_distance(float dist) {
  // Intentionally blank.
}

float NullAudioSound::get_3d_min_distance() const {
  // Intentionally blank.
  return 0.0f;
}

void NullAudioSound::set_3d_max_distance(float dist) {
  // Intentionally blank.
}

float NullAudioSound::get_3d_max_distance() const {
  // Intentionally blank.
  return 0.0f;
}

AudioSound::SoundStatus NullAudioSound::status() const {
  return AudioSound::READY; 
}
