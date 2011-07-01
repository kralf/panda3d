#!BPY

__author__ = "Daniel Amthauer"
__url__ = ("Chicken homepage, http://chicken-export.sf.net")
__email__="daniel*amthauer:gmail*com"
__version__ = "R91"

__bpydoc__ = """This script offers an interface to configure the necessary data for Chicken to function properly
"""

# Copyright (C) 2008  Daniel Amthauer
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

try:
	import chicken_interface
except ImportError:
	err_str = 'chicken_interface module not found. Chicken will not work without this module.'
	if Blender.mode == 'background':
		print err_str
	else:
		Draw.PupMenu('Chicken Error%s|%s'%('%t', err_str))
	raise ImportError(err_str)

import os
from chicken_interface import LoadPath, CheckPath, ButtonWrapper, EXPORTER_NAME

import Blender
from Blender import Draw, Window, BGL, Registry

class ConfigUI:
	def __init__(self):
		binPath = LoadPath()
		binAuto = int(binPath == '')
		if os.name == 'nt': binAuto = 0

		self.buttonFunc = {}

		self.bBinPathAuto = ButtonWrapper('Auto', 3, 'toggle', initial = binAuto)
		self.bBinPathManual = ButtonWrapper('Manual', 4, 'toggle', initial = int(not binAuto))
		def fBinToggle(evt):
			if evt is 4:
				self.bBinPathAuto.val = (self.bBinPathAuto.val+1)%2
			else:
				self.bBinPathManual.val = (self.bBinPathManual.val+1)%2
		self.buttonFunc[3] = self.buttonFunc[4] = fBinToggle

		self.bBinPath = ButtonWrapper('PandaBinPath:', 0, 'string', 'The path that contains panda tool binaries (e.g. pview)', binPath, length=300)
		self.bBinPathSel = ButtonWrapper('Select', 5, 'push')
		if os.name == 'nt' and not binPath:
			envpath = os.getenv('PATH')
			pathdirs = envpath.split(os.pathsep)
			candidates = filter(lambda x: x.lower().find('panda3d') != -1 and x.lower().find('bin') != -1, pathdirs)
			if candidates:
				self.bBinPath.val = candidates[0]
		

		self.bLaunch = ButtonWrapper('Launch Chicken', 6, 'push')
		def fLaunch(dummy):
			if self.error is False:
				print os.path.join(Blender.Get('scriptsdir'),EXPORTER_NAME)
				Blender.Run(os.path.join(Blender.Get('scriptsdir'),EXPORTER_NAME))
			else:
				if self.error is True:
					word = "corrected"
				elif self.error is None:
					word = "validated"
				Draw.PupMenu('Launch Error%s|Cannot launch until configuration is %s'%('%t',word))
		self.buttonFunc[6] = fLaunch

		self.bCheck = ButtonWrapper('Check Configuration', 7, 'push')
		def fCheck(dummy):
			self.msg = []
			if self.bBinPathAuto.val:
				bin = ''
			else:
				bin = self.bBinPath.val
			self.error = CheckPath(bin, self.msg)
			if self.error is False:
				d = {}
				if self.bBinPathManual.val:
					d['PandaBinPath'] = bin
				else:
					d['PandaBinPath'] = ''
				Registry.SetKey('Chicken', d, True)
			else:
				Draw.PupMenu('Configuration Errors%t|'+'|'.join(self.msg))
				print self.msg
		self.buttonFunc[7] = fCheck

		self.pathMap = {5:self.bBinPath}
		def fPathSelector(id):
			def updatePath(fn):
				n = fn.rfind(os.sep)
				fn = fn[0:n]
				if os.path.isdir(fn):
					self.pathMap[id].val = fn
			Window.FileSelector(updatePath,"Select Path",self.pathMap[id].val)
		self.buttonFunc[5] = fPathSelector

		self.error = None
		self.msg = []

		Draw.Register(self.draw, self.event, self.button)

	def draw(self):
		area = Window.GetAreaSize()
		w = area[0]; wPad = int(w*0.03)
		h = area[1]; hPad = int(h*0.03)
		BGL.glColor3f(0.3, 0.3, 0.3)
		BGL.glRectf(wPad-5, h-60, w-wPad+5, h-85)
		BGL.glColor3f(1.0,1.0,1.0)
		BGL.glRasterPos2i(wPad, h-75)
		Draw.Text('Chicken Configuration script', 'large')
		BGL.glRasterPos2i(wPad, h-100)
		Draw.Text('This script is launched the first time you run Chicken, or when a configuration error has been detected')

		BGL.glColor3f(0.5, 0.5, 0.5)
		BGL.glRectf(wPad, h-205, w-wPad, h-225)
		BGL.glColor3f(1.0,1.0,1.0)
		BGL.glRasterPos2i(wPad, h-220)
		Draw.Text('Binary Utilities - ')
		Draw.Text('if executables such as "pview" are on your PATH, you can leave this on Auto. Otherwise enter the folder manually')
		self.bBinPathAuto.update([wPad+5, h-250, w/2-wPad-5, 20])
		self.bBinPathManual.update([w/2, h-250, w/2-wPad-5, 20])

		if self.bBinPathManual.val:
			self.bBinPath.update([wPad+5, h-272, w-2*wPad-90, 20])
			self.bBinPathSel.update([w-wPad-85, h-272, 80, 20])
		self.bLaunch.update([wPad+5, h-330, 100, 20])
		self.bCheck.update([w-wPad-85, h-330, 80, 20])
		if self.error is not None:
			if self.error is True:
				BGL.glColor3f(1.0,0.0,0.0)
				BGL.glRasterPos2i(w-wPad-150, h-365)
				Draw.Text('Configuration error detected')
			else:
				BGL.glColor3f(0.0,0.0,0.0)
				BGL.glRasterPos2i(w-wPad-200, h-365)
				Draw.Text('Configuration checked and saved')


	def event(self, evt, val):
		pass
	def button(self, evt):
		if evt > 0:
			self.buttonFunc[evt](evt)
		Draw.Redraw()

c = ConfigUI()