// Filename: nullAudioManager.h
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

#ifndef __NULL_AUDIO_MANAGER_H__
#define __NULL_AUDIO_MANAGER_H__

#include "audioManager.h"
#include "nullAudioSound.h"

class EXPCL_PANDA_AUDIO NullAudioManager : public AudioManager {
  // All of these methods are stubbed out to some degree.
  // If you're looking for a starting place for a new AudioManager,
  // please consider looking at the milesAudioManager.
  
public:
  NullAudioManager();
  virtual ~NullAudioManager();
  
  virtual bool is_valid();
  
  virtual PT(AudioSound) get_sound(const string&, bool positional = false, int mode=SM_heuristic);
  virtual PT(AudioSound) get_sound(MovieAudio *sound, bool positional = false, int mode=SM_heuristic);
  virtual void uncache_sound(const string&);
  virtual void clear_cache();
  virtual void set_cache_limit(unsigned int);
  virtual unsigned int get_cache_limit() const;

  virtual void set_volume(float);
  virtual float get_volume() const;

  virtual void set_play_rate(float);
  virtual float get_play_rate() const;
  
  virtual void set_active(bool);
  virtual bool get_active() const;

  virtual void set_concurrent_sound_limit(unsigned int limit);
  virtual unsigned int get_concurrent_sound_limit() const;

  virtual void reduce_sounds_playing_to(unsigned int count);

  virtual void stop_all_sounds();

  virtual void audio_3d_set_listener_attributes(float px, float py, float pz,
                                                float vx, float vy, float vz,
                                                float fx, float fy, float fz,
                                                float ux, float uy, float uz);
  virtual void audio_3d_get_listener_attributes(float *px, float *py, float *pz,
                                                float *vx, float *vy, float *vz,
                                                float *fx, float *fy, float *fz,
                                                float *ux, float *uy, float *uz);
  
  virtual void audio_3d_set_distance_factor(float factor);
  virtual float audio_3d_get_distance_factor() const;

  virtual void audio_3d_set_doppler_factor(float factor);
  virtual float audio_3d_get_doppler_factor() const;

  virtual void audio_3d_set_drop_off_factor(float factor);
  virtual float audio_3d_get_drop_off_factor() const;


public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    AudioManager::init_type();
    register_type(_type_handle, "NullAudioManager",
                  AudioManager::get_class_type());
  }
  virtual TypeHandle get_type() const {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() {init_type(); return get_class_type();}

private:
  static TypeHandle _type_handle;
};

#endif /* __NULL_AUDIO_MANAGER_H__ */
