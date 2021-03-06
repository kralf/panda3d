// Filename: config_fmodAudio.h
// Created by:  cort
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

#ifndef CONFIG_FMODAUDIO_H
#define CONFIG_FMODAUDIO_H

#include "pandabase.h"

#ifdef HAVE_FMODEX //[
#include "notifyCategoryProxy.h"
#include "dconfig.h"
#include "audioManager.h"

ConfigureDecl(config_fmodAudio, EXPCL_FMOD_AUDIO, EXPTP_FMOD_AUDIO);
NotifyCategoryDecl(fmodAudio, EXPCL_FMOD_AUDIO, EXPTP_FMOD_AUDIO);

extern EXPCL_FMOD_AUDIO void init_libFmodAudio();
extern "C" EXPCL_FMOD_AUDIO Create_AudioManager_proc *get_audio_manager_func_fmod_audio();

#endif //]

#endif // CONFIG_FMODAUDIO_H
