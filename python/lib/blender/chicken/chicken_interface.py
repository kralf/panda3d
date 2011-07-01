# -*- coding: utf-8 -*-
# this file goes in the bpymodules directory
'''
This module allows a Blender script to run the Chicken Exporter on the current selection
Use the Invoke function to do this
'''
try:
	from pprint import pformat
except ImportError:
	raise Exception("The Chicken interface requires a full Python installation. Cannot continue - you need to install a 2.x version of Python for Blender to use. Obtain from python.org. This is documented in the installation guide, chicken_install.txt - please read this and attempt to fix before asking in the forums.")


import Blender, os, sys
from Blender import Text, Draw, Registry
from Blender.sys import makename


KEY = 'CHICKEN_FORCE_BACKGROUND'
RANGE_KEY = 'CHICKEN_RANGE'
SETTINGS_KEY = 'CHICKEN_SETTINGS'
MESSAGE_KEY = 'CHICKEN_MESSAGES'

EXPORTER_NAME = 'chicken_exportR91.py' # version of the exporter that came bundled with this module


def Invoke(exporter=EXPORTER_NAME, use_stored=False, progress_range=None,
		filename = None, selection = None, anims = None, tools = None,
			optparms = None, mextract = False, animonly = False):
	'''
	Invokes Chicken exporter in Forced Background mode
	@param exporter: Specific filename for Chicken, defaults to the version that came with this module
	@param use_stored: Boolean that indicates whether to use stored parameters for export.
	@param progress_range: sequence of 2 floats that defines the range of progress this represents of the total operation
	@param filename: The destination filename. Defaults to working filename
	@param selection: A list of strings containing the names of the selected objects. Defaults to current selection
	@param anims: A list of 4-lists containing [animation-name, fps, start, end]
	@param tools: A 3-tuple containing booleans that indicate whether to invoke pview, egg2bam, and egg-optchar in that order.
	@param optparms: Optional parameters for egg-optchar. Defaults to '-inplace'
	@param mextract: Boolean that indicates whether to attempt motion extraction. Default is False.
	@param animonly: Boolean that indicates that only animation should be exported.
	@return: False if exporter not found, a tuple of the form (pre-export messages, post-export messages)
		if succesful (True is returned if messages were unattainable).
	'''
	result = True
	os.environ[KEY] = 'yes' # arbitrary value, chicken only cares that it is set
	if progress_range and len(progress_range) == 2:
		os.environ[RANGE_KEY] = '%f,%f'%tuple(progress_range)
	if not use_stored:
		# make settings
		settings = Text.New('interface.chicken')
		os.environ[SETTINGS_KEY] = settings.getName()
		settings.write(MakeSettings(filename, selection, anims, tools, optparms, mextract, animonly))
	try:
		Blender.Run(os.path.join(Blender.Get('scriptsdir'),exporter))
	except AttributeError:
		result = False
	if result:
		try:
			msg_txt = Text.Get(os.getenv(MESSAGE_KEY))
		except: pass
		else:
			try:
				msg_str = '\n'.join(msg_txt.asLines())
				import cPickle
				result = cPickle.loads(msg_str)
			except: print sys.exc_info()
			Text.unlink(msg_txt)
	if not use_stored:
		# delete temp settings
		Text.unlink(settings)
		del os.environ[SETTINGS_KEY]
	del os.environ[KEY]
	if os.environ.has_key(MESSAGE_KEY):
		del os.environ[MESSAGE_KEY]
	if os.environ.has_key(RANGE_KEY):
		del os.environ[RANGE_KEY]
	return result

def MakeSettings(filename = None, selection = None, anims = None, tools = None,
                 optparms = None, mextract = False, animonly = False,
                 octreeCollision = None, doTangents = None, singleFile = None,
                 forceRelTex = None, forceBFace = None, pzip = False):
  '''
  This function returns a string that contains settings in a valid format for Chicken to read
  '''
  result = []
  if filename:
    result.append('filename = '+pformat(filename))
  if selection:
    result.append('sel = '+pformat(selection))
  if anims:
    result.append('anims = '+pformat(anims))
  if tools:
    result.append('tools = '+pformat(tools))
  if optparms:
    result.append('optparms = '+pformat(optparms))
  if mextract:
    result.append('mextract = '+pformat(mextract))
  if animonly:
    result.append('animonly = '+pformat(animonly))
  if octreeCollision!=None:
    result.append('octreecollision = '+pformat(octreeCollision))
  if doTangents!=None:
    result.append('dotangents = '+pformat(doTangents))
  if singleFile!=None:
    result.append('singlefile = '+pformat(singleFile))
  if forceRelTex!=None:
    result.append('forceRelTex = '+pformat(forceRelTex))
  if forceBFace!=None:
    result.append('forceBFace = '+pformat(forceBFace))
  if pzip!=None:
    result.append('pzip = '+pformat(pzip))
  return '\n'.join(result)


def LoadPath():
	R = Registry.GetKey('Chicken', True)
	error = True
	if R:
		try:
			binPath = R['PandaBinPath']
		except KeyError: pass
		else:
			error = False

	if error:
		binPath = ''
	return binPath


def CheckPath(bin, msg = None):
	error = False
	utils = ['egg2bam', 'egg-optchar', 'pview']
	if os.name == 'nt':
		utils = map(lambda x: x+'.exe', utils)
	if bin == '':
		utils[2] = 'pview -h' # so it doesn't open a window
		for u in utils:
			ret = os.system(u)
			if ret is not 0 and ret is not 256:
				error = True
				if msg is not None:
					msg.append('"%s" returned %d. Perhaps your PATH environment variable is not properly set'%(u,ret))
				break
	else:
		for u in utils:
			file = os.path.join(bin, u)
			if not os.path.isfile(file):
				error = True
				if msg is not None:
					msg.append('"%s" was not found on the provided binary path.'%u)
				break
	return error


class ButtonWrapper:
	'''
	This class wraps most of the complexity with drawing buttons
	'''
	DrawFunctions = {'toggle': Draw.Toggle, 'push':Draw.PushButton, 'number':Draw.Number, 'string':Draw.String }
	def __init__(self, name, evt, type, tooltip = '', initial=0, min=0, max=0, length=0):
		self.name = name
		self.evt = evt
		self.type = type
		self.tooltip = tooltip
		self.func = ButtonWrapper.DrawFunctions[type]
		self.button = Draw.Create(initial)
		if type == 'number':
			self.min = min
			self.max = max
		elif type == 'string':
			self.length = length
	def update(self, rect):
		parms = [self.name, self.evt]+rect
		if self.type != 'push':
			parms += [self.button.val]
		if self.type == 'number':
			parms += [self.min, self.max]
		elif self.type == 'string':
			parms += [self.length]
		if self.tooltip:
			parms += [self.tooltip]
		self.button = self.func(*parms)
	def __getattr__(self, attr):
		return getattr(self.button, attr)
	def __setattr__(self, attr, val):
		if attr == 'val':
			self.button.val = val
		else:
			self.__dict__[attr] = val




class Message:
	'''
	This class represents a message and its severity. Used in Chicken for
	warnings and errors, and returned by the Invoke function after a
	succesful invoke.
	'''
	# severity
	Error = 2
	Warning = 1
	Info = 0

	nf_err = 'The %s utility was not found'
	exec_err = 'The %s utility reported errors. Check the console for details'
	envelope_str = 'The following objects use Envelopes in their Armature \
modifier: %s. The effects of Envelopes are not exported.'
	anim_mod_str = 'The following objects have Armature modifiers but also contain other modifiers: %s. The effects of these modifiers cannot be exported'

	def __init__(self, message, severity):
		self.message = message
		self.severity = severity
	def __repr__(self):
		if self.severity == Message.Error:
			sev_str = 'Error'
		elif self.severity == Message.Warning:
			sev_str = 'Warning'
		else:
			sev_str = 'Info'
		return '%s: %s'%(sev_str, self.message)
# message instances
Message.multi_armature = Message('Only one armature may be exported at a time', Message.Error)

Message.no_selection = Message('No objects selected', Message.Error)
Message.neg_scale = Message('Object with negative scale - will not display correctly in Panda.', Message.Warning)

Message.file_error = Message('The target export file could not be opened. You may lack write permissions on it.', Message.Error)

Message.bam_nf = Message(Message.nf_err%'egg2bam', Message.Error)
Message.bam_exec = Message(Message.exec_err%'egg2bam', Message.Error)

Message.opt_nf = Message(Message.nf_err%'egg-optchar', Message.Error)
Message.opt_exec = Message(Message.exec_err%'egg-optchar', Message.Error)

Message.octree_nf = Message(Message.nf_err%'eggoctree', Message.Error)
Message.octree_exec = Message(Message.exec_err%'eggoctree', Message.Error)

Message.pv_nf = Message(Message.nf_err%'pview', Message.Error)
Message.pz_nf = Message(Message.nf_err%'pzip', Message.Error)

Message.trans_nf = Message(Message.nf_err%'egg-trans', Message.Error)
Message.trans_exec = Message(Message.exec_err%'egg-trans', Message.Error)