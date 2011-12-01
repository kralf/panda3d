#!BPY
# -*- coding: utf-8 -*-

""" Registration info for Blender menus:
Name: 'Chicken R91 (.egg)...'
Blender: 245
Group: 'Export'
Tip: 'Export to the Panda3D Egg format.'
"""
__author__ = "Daniel Amthauer, Simon Groenewolt, Tom SF Haines, Emanuele Bertoldi, Reinier de Blois"
__url__ = ("Chicken homepage, http://chicken-export.sf.net")
__email__="thaines:gmail*com"
__version__ = "R91"

__bpydoc__ = """
Chicken is an Egg exporter for Blender.<br>
For more information see the included HTML documentation, accessible through the
help button in the script's window.
"""

# chicken_exportR91.py
# Copyright (C) 2008  Daniel Amthauer, Simon Groenewolt, Tom SF Haines, Reinier de Blois
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

import Blender, os, sys

from Blender import Draw, BGL, Image, Modifier, Mesh, Types, Window, Text
from Blender import Material as BMaterial
from Blender import Texture as BTexture
from Blender.Mathutils import *
from Blender.Window import DrawProgressBar, Theme
from Blender.sys import makename

webbrowser = None
INTERFACE_ERROR = False
try:
  import chicken_interface
except ImportError:
  exc = sys.exc_info()[1]
  msg = exc.args[0]
  err_str = 'chicken_interface could not be imported. Chicken will not work without this module. This invariably means you have installed to the wrong directory, partially installed or otherwise failed to handle permissions when installing Chicken. Please read the installation guide, chicken_install.txt, and check all of these possibilities before posting to the forums.'
  err_str2 = 'The reported error was: '+msg
  if Blender.mode == 'background':
    print err_str
    print err_str2
  else:
    Draw.PupMenu('Chicken Error%s|%s|%s'%('%t', err_str, err_str2))
  INTERFACE_ERROR = True

if not INTERFACE_ERROR:
  from chicken_interface import *
  PATH = LoadPath()
  PATH_ERROR = CheckPath(PATH)

CHICKEN_LOGO = '/chicken/newchicken.png'
CHICKEN_DOC = '/chicken/doc.html'
MATERIALS, TEXTURES = None, None # globals for materials and textures
IDENTITY = Matrix() # 4x4 Identity matrix. Don't know if it's cheaper than making a new one every time, but I find it more readable
INITIAL = ["<CoordinateSystem> { Z-up }\n",
      '<Comment> { "Egg laid by Chicken for Blender, version %s" }\n'%__version__]

FORCE_BACKGROUND = False

# Make this True if Mix should map to Modulate.
MAP_MIX_TO_MODULATE = False

# optional features (depend on a recent CVS version of Blender, or experimental patches)
# set to True if you wish to test them
CURVE_SUPPORT = True # Was originally False due to patch submission delay - confirmed to work fine with Blender 2.46

# Used to limit the number of tangent warnings emitted, as otherwise they could swamp things...
TANGENT_PROBLEM = False

# If True shape key export is enabled...
DO_SHAPE_KEYS = True

# If true normal vectors are exported with the shape keys...
SHAPE_KEY_NORMALS = True



def eggSafeName(s):
  """Function that converts names into something suitable for the egg file format - simply puts " around names that contain spaces and prunes bad characters, replacing them with an underscore."""
  s = s.replace('"','_') # Sure there are more bad characters, but this will do for now.
  if ' ' in s:
    return '"' + s + '"'
  else:
    return s


def convertFileNameToPanda(filename):
  """Converts Blender filenames to Panda 3D filenames."""
  path =  filename.replace('//', './').replace('\\', '/')
  if os.name == 'nt' and path.find(':') != -1:
    path = '/'+ path[0].lower() + path[2:]
  return path


DELTA = 1e-6
def vectorEq(v1,v2):
  """Tests for vector equality."""
  return (abs(v1[0] - v2[0]) < DELTA) and (abs(v1[1] - v2[1]) < DELTA) and (abs(v1[2] - v2[2]) < DELTA)


def getRelativePath(path,relTo):
  """Returns path given relative to relTo, using .. if necesary to go back from relTo's position. Assumes that both paths end in filenames rather than directories."""
  relTo = convertFileNameToPanda(relTo)
  prefix = os.path.commonprefix([path,os.path.dirname(relTo)])
  prefixLen = len(prefix)-(prefix[-1]=="/")
  return "." + ("/%s"%os.pardir)*(relTo[prefixLen:].count("/")-1) + path[prefixLen:]



class Exporter:
  '''Abstract base class for Gui and Background exporters'''
  def init(self, settings = None, progress_range=None, batchData=[]):
    '''Not a real constructor, just a place to put common intialization'''
    self.messages = []
    self.meshes = {'static':[],'armature':[]}
    self.error = False
    self.statusMsg = ''
    self.selection = None
    self.binPath = PATH
    # interpret progress range if any
    if type(progress_range) == type(str()):
      progress_range = map(float, progress_range.split(','))
      if len(progress_range) != 2:
        progress_range = (0.0, 1.0)
    elif progress_range is None:
      progress_range = (0.0, 1.0)
    self.prog_start = progress_range[0]
    self.prog_diff = progress_range[1]-progress_range[0]
    self.prog_end = progress_range[1]
    # begin load settings
    sDefault = settings is None # no user defined file or text to look in, therefore check defaults
    setting_txt = None
    if settings:
      settings_file = makename(settings, ext='.chicken')
    else:
      settings_file = makename(ext='.chicken')
    if os.path.isfile(settings_file):
      settings_file = open(settings_file, 'r')
      setting_txt = settings_file.read()
    else:
      if sDefault:
        settings = 'export.chicken'
      try:
        settings = Text.Get(settings)
      except NameError:
        pass
      else:
        setting_txt = '\n'.join(settings.asLines())

    if not setting_txt:
      print "Settings for export not found. Using defaults."

    # Default values for possible settings...
    d = {'filename': None,
        'sel':None,
        'anims':[],
        'tools':(False,False,False,False),
        'pzip':False,
        'optparms':'',
        'mextract':False,
        'animonly':False,
        'singlefile':True,
        'dotangents':True,
        'octreecollision':False,
        'forceRelTex':True,
        'forceBFace':True
        }
    tf = ['pzip', 'mextract', 'animonly', 'singlefile', 'dotangents',
      'octreecollision', 'forceRelTex', 'forceBFace']
    
    if setting_txt:
      try:
        exec setting_txt in d # This treats setting_txt as python code and runs it with d as its environment, so the assignments update d.
      except:
        print "Settings not valid. Exiting"
        return

    # Override data with batch (background mode) params...
    for k in batchData:
      d[k] = batchData[k]

    # Calculate a default filename...
    if d['filename']:
      self.filename = makename(d['filename'], ext='.egg')
    else:
      self.filename = makename(ext='.egg')
    
    # Transfer in the animations, considering that it could be in string format...
    if type(d['anims']) == type(str()):
      # Prepare each anim data, converting numeric elements (the last three of the sequence)...
      self.anims = []
      for elem in d['anims'].split(';'):
        se = elem.split(',')
        self.anims.append([se[0]] + [int(x) for x in se[1:]])
    else:
      self.anims = d['anims']

    # Handle if any of the true/false values are strings...
    for name in tf:
      if type(d[name]) == type(str()):
        if d[name]=='False':
          d[name] = False
        else:
          d[name] = True

    # Get and handle the selection - in background mode will be a string...
    o = Blender.Scene.GetCurrent().objects
    sel = d['sel']
    if type(sel) == type(str()):
      # Sel here must be a comma separated string...
      sel = set(sel.split(','))
      self.selection = filter(lambda x: x.name in sel, o)
    else:
      # Sel here must be a sequence...
      self.selection = filter(lambda x: x.sel, o)
      
    # Tool setup,...
    if len(d['tools'])==4:
      self.pview, self.egg2bam, self.optchar, self.octree = d['tools']
    elif len(d['tools'])==3:
      self.pview, self.egg2bam, self.optchar = d['tools']
      self.octree = False
    else:
      print 'Bad tool settings - using defaults'

    # Handle any replacement variables for the above list - used by background export mode...
    if d.has_key('pview'): self.pview = d['pview']!='False'
    if d.has_key('bam'): self.egg2bam = d['bam']!='False'
    if d.has_key('optchar'): self.optchar = d['optchar']!='False'
    if d.has_key('octree'): self.octree = d['octree']!='False'

    # Finally just extract the rest ready for use...
    self.optParms = d['optparms']
    self.pzip = d['pzip']
    self.mExtract = d['mextract']
    self.animOnly = d['animonly']
    self.singleFile = d['singlefile']
    self.doTangents = d['dotangents']
    self.octreeCollision = d['octreecollision']
    self.forceRelTex = d['forceRelTex']
    self.forceBFace = d['forceBFace']
    # End loading of settings

    self.success = False
    self.time = None
    self.normalMappedUVs = set([])

  def analyzeSelection(self):
    '''
    This method is called when updating the selection before exporting.
    It sets/updates variables that will be used upon export.
    '''
    self.success = False
    self.messages = []
    if self.selection:
      selection = self.selection
    else:
      selection = Blender.Object.GetSelected()
    self.lastSelected = selection
    # get all objects that are meshes, empties or curves
    objects = filter(lambda x: x.getType() in ('Mesh', 'Empty', 'Curve'), selection)
    if len(objects) == 0:
      self.messages.append(Message.no_selection)
    else:
      meshes = filter(lambda x: x.getType() == 'Mesh', objects)
      empties = filter(lambda x: x.getType() == 'Empty', objects)

      # Check for negative scales...
      for obj in objects:
        if len(filter(lambda x: x<0.0,obj.getSize()))!=0:
          self.messages.append(Message.neg_scale)

      self.invalidModifiers = []
      self.envelopesUsed = []
      def getArmatureName(x):
        armatureMod = None
        for mod in x.modifiers:
          if mod.type == Modifier.Type.ARMATURE:
            armatureMod = mod
          else:
            self.invalidModifiers.append(x.name)
        if armatureMod:
          arm = armatureMod[Modifier.Settings.OBJECT]
          envelope = armatureMod[Modifier.Settings.ENVELOPES]
          if envelope:
            self.envelopesUsed.append(x.name)
          if arm:
            return arm.name
          else:
            return None
        return None
      armatures = map(getArmatureName, meshes) # get armature name for every selected mesh
      if self.envelopesUsed:
        self.messages.append(Message(Message.envelope_str%(', '.join(self.envelopesUsed)), Message.Warning))
      del self.envelopesUsed
      armatureSet = set(armatures) # set of unique armature names, None is in it if there are meshes with no armature
      armatureSet.discard(None)
      self.numArmatures = len(armatureSet)
      if self.numArmatures > 1:
        self.messages.append(Message.multi_armature)
        self.anims = None
      try:armature = armatureSet.pop()
      except KeyError: armature = None

      # divide meshes into static and animated (for now only armature)
      static_meshes, armature_meshes = [], []
      self.invalidModifiers = set(self.invalidModifiers)
      anim_mod_names = []
      for i, m in enumerate(meshes):
        if armatures[i]:
          armature_meshes.append(m)
          if m.name in self.invalidModifiers:
            anim_mod_names.append(m.name)
        else: static_meshes.append(m)
      del self.invalidModifiers
      if anim_mod_names:
        self.messages.append(Message(Message.anim_mod_str%(', '.join(anim_mod_names)), Message.Warning))

      static_meshes.extend(empties) #put empties together with static meshes

      self.meshes = {'static':static_meshes,
               'armature':armature_meshes}
      if armature:
        self.armature = Blender.Object.Get(armature)
        try:
          self.srb = self.armature.getData().bones['SyntheticRootBone']
        except KeyError: self.srb = None

      if CURVE_SUPPORT:
        curves = filter(lambda x: x.getType() == 'Curve', objects)
        self.curves = []
        for c in curves:
          curve = c.getData()
          for i, curnurb in enumerate(curve):
            if curnurb.getType() == 4 and not curnurb.isCyclic():
              name = c.name
              if len(curve)>1: name += str(i)
              self.curves.append((name, curnurb, c))
            else:
              print 'Unsuported curve type - must be NURBS without cycles.'

    self.analyzeMessages()

  def doExport(self):
    '''
    This method does the bulk of the export process. It creates the
    internal data structures to represent what will be exported and
    accumulates their representations in a buffer which is then
    written to a file. It then invokes any additional Panda tools that
    were specified by the user via the GUI or Background interfaces.
    '''
    self.filename = makename(self.filename, ext = ".egg")
    self.success = False
    self.time = None
    time1 = Blender.sys.time()
    if self.error:
      return
    self.messages = []
    self.reportProgress(self.prog_start, 'Exporting.')
    objs = {}
    global MATERIALS, TEXTURES
    MATERIALS, TEXTURES = {}, {}
    character = None
    if len(self.meshes['armature']) > 0:
      character = Character(self.armature, self.meshes['armature'], self.mExtract and self.srb, self.animOnly, addTangents=self.doTangents)
    if not self.animOnly:
      statics = self.meshes['static']
      if len(statics) > 0:

        # Create list of objects, empties that are dupligroup's get turned into links, as external file references...
        groups = []
        for m in statics:
          if m.getType()=='Empty' and m.DupGroup!=None:
            groups.append(Link(mesh=m))
          else:
            groups.append(Group(mesh=m, addTangents=self.doTangents))

        # begin reconstruction of hierarchy
        def getParentIndex(x):
          try: return statics.index(x.parent)
          except ValueError: return -1
        parents = map(getParentIndex, statics)
        for i, p in enumerate(parents):
          if p != -1:
            # if this group's parent is also in the selection
            # switch its transform to local and append it to the
            # parent group's children
            child = groups[i]
            child.transform = statics[i].matrixLocal
            groups[p].children.append(child)
          else:
            objs[groups[i].name] = groups[i]
        # end

      # Write everything to the output buffer...
      buffer = INITIAL[:]
      for mat in MATERIALS.values():
        if mat.users > 0:
          mat.write(buffer)
          #print mat
      for tex in TEXTURES.values():
        if tex.users > 0:
          tex.write(buffer)
          #print tex
      if character:
        character.write(buffer)
        #print character
      for o in objs.values():
        o.write(buffer)
        #print o
      if CURVE_SUPPORT:
        for c in self.curves:
          NurbsCurve(*c).write(buffer)
      if character:
        self.reportProgress(self.prog_start+0.5*self.prog_diff, 'Exporting meshes...')
      else:
        self.reportProgress(self.prog_start+0.75*self.prog_diff, 'Exporting meshes...')

      try:
        out_file = open(self.filename,"w")
      except IOError:
        self.messages.append(Message.file_error)
        self.analyzeMessages()
        self.statusMsg += ' ...Could not export'
        self.reportProgress(1.0, '')
        return
      else:
        out_file.write('\n'.join(buffer))
        if self.singleFile and character:
          self.reportProgress(self.prog_start+0.75*self.prog_diff, 'Exporting meshes...')
          character.writeAnims("", self.anims, out_file)
        out_file.close()
    if character and not self.singleFile:
      self.reportProgress(self.prog_start+0.75*self.prog_diff, 'Exporting anims...')
      character.writeAnims(makename(self.filename, ext=''), self.anims)

    #begin calling of external Panda utils
    if self.pzip or self.egg2bam or self.optchar or self.pview or self.octree or (len(self.normalMappedUVs) > 0 and self.doTangents==False):
      plainName = makename(self.filename, ext='')
      bamName = makename(self.filename,".bam")
      if self.anims:
        animNames = map(lambda x: "%s-%s"%(plainName,x[0]), self.anims)
      else: animNames = []
      argsPzip = ['pzip']
      argsPview = ['pview','-c', '-l']
      argsOpt = ['egg-optchar']
      argsTrans = ['egg-trans']
      if self.optParms:
        argsOpt.extend(self.optParms.split(' '))
      else:
        argsOpt.append('-inplace')

      if self.egg2bam:
        pviewExt = '.bam'
      else:
        pviewExt = '.egg'
      if os.name != 'nt': #in systems that have spawnvp use it
        spawnfunc = os.spawnvp
        argsBam = ['egg2bam', '-o'+bamName, self.filename]
        argsOpt.append(self.filename)
        if animNames:
          argsPview.append('-a')
        argsPview.append(makename(self.filename, ext=pviewExt))
        if animNames:
          argsPview.append(makename(animNames[0], ext=pviewExt))
        if not self.singleFile:
          for n in animNames:
            argsOpt.append(makename(n,ext='.egg'))
        argsTrans.extend(['-o'+self.filename, self.filename])
        argsPzip.append(makename(self.filename, ext=pviewExt))
      else:
        spawnfunc = os.spawnv
        argsBam = ['egg2bam', '-o"%s"'%bamName, '"%s"'%self.filename]
        argsOpt.append('"%s"'%self.filename)
        if animNames:
          argsPview.append('-i -a')
        argsPview.append('"%s"'%makename(plainName,ext=pviewExt))
        if animNames:
          argsPview.append('"%s"'%makename(animNames[0], ext=pviewExt))
        if not self.singleFile:
          for n in animNames:
            argsOpt.append('"%s"'%makename(n,ext='.egg'))
        argsTrans.extend(['-o"%s"'%self.filename, '"%s"'%self.filename])
        argsPzip.append('"%s"'%makename(plainName,ext=pviewExt))

      if len(self.normalMappedUVs) > 0 and self.doTangents==False:
        argsTransUV = ' '.join(['-tbn %s'%name for name in self.normalMappedUVs])
        argsTrans[1:1] = argsTransUV.split(' ')
        try:
          call = os.path.join(self.binPath,'egg-trans')
          ret = spawnfunc(os.P_WAIT, call, argsTrans)
        except OSError:
            self.messages.append(Message.trans_nf)
        else:
          if ret != 0:
            self.messages.append(Message.trans_exec)

      if self.optchar:
        try:
          call = os.path.join(self.binPath,'egg-optchar')
          ret = spawnfunc(os.P_WAIT, call, argsOpt)
        except OSError:
            self.messages.append(Message.opt_nf)
        else:
          if ret != 0:
            self.messages.append(Message.opt_exec)

      if self.octree:
        try:
          call = os.path.join(self.binPath,'egg2bam')
          args = []
          if os.name!='nt':
            args.append('python')
          else:
            args.append('ppython')

          args.append(os.path.join(Blender.Get('scriptsdir'),'chicken_eggoctree.py'))

          if self.octreeCollision: args.append('-c')

          args.append('-o')
          args.append(self.filename)
          args.append(self.filename)

          if os.name=='nt': # It would appear that under windows you have to quote the arguments, even though they *should* be passed through direct.
            args = map(lambda x: '"'+x+'"',args)

          if os.name != 'nt':
            ret = os.spawnvp(os.P_WAIT,'python',args)
          else:
            ret = os.spawnv(os.P_WAIT,os.path.join(self.binPath,'../python/ppython'),args)
        except OSError:
          self.messages.append(Message.octree_nf)
        else:
          if ret != 0:
            self.messages.append(Message.octree_exec)

      if self.egg2bam:
        if not self.animOnly:
          try:
            call = os.path.join(self.binPath,'egg2bam')
            ret = spawnfunc(os.P_WAIT, call, argsBam)
            print 'performed call %s with return code %d'%(call, ret)
          except OSError:
            self.messages.append(Message.bam_nf)
          else:
            if ret != 0:
              self.messages.append(Message.bam_exec)
        for n in animNames:
          if os.name == 'nt':
            argsBam[1] = '-o"%s"'%makename(n, ext='.bam')
            argsBam[2] = '"%s"'%makename(n, ext='.egg')
          else:
            argsBam[1] = '-o'+makename(n, ext='.bam')
            argsBam[2] = makename(n, ext='.egg')
          try:
            call = os.path.join(self.binPath,'egg2bam')
            ret = spawnfunc(os.P_WAIT, call, argsBam)
            print 'performed call %s with return code %d'%(call, ret)
          except OSError:
            self.messages.append(Message.bam_nf)
          else:
            if ret != 0:
              self.messages.append(Message.bam_exec)

      if self.pzip:
        try:
          call = os.path.join(self.binPath, 'pzip')
          ret = spawnfunc(os.P_WAIT, call, argsPzip)
          print "performed call '%s' with return code %d" % (call, ret)
        except OSError:
          self.messages.append(Message.pz_nf)

      if self.pview:
        try:
          call = os.path.join(self.binPath,'pview')
          spawnfunc(os.P_NOWAIT, call, argsPview)
        except OSError:
          self.messages.append(Message.pv_nf)
    self.reportProgress(self.prog_end, 'Done')
    self.success = True
    self.time = Blender.sys.time() - time1
    self.analyzeMessages()

  def analyzeMessages(self):
    errors = 0
    warnings = 0
    for m in self.messages:
      if m.severity == Message.Error:
        errors += 1
      elif m.severity == Message.Warning:
        warnings += 1
    self.statusMsg = 'No apparent problems'
    self.error = errors > 0
    if errors or warnings:
      self.statusMsg = '%i Error(s), %i Warning(s) Found'%(errors,warnings)



class Gui(Exporter):
  '''
  This class encapsulates everything that involves interacting with
  the user through the Blender GUI
  '''
  animStart = 15 # the first event for animation delete buttons
  class AnimationRow:
    def __init__(self, name, fps, start, end):
      self.bName = ButtonWrapper('name: ', 0, 'string', 'The exported animation file will be named after this and the export file, so keep them unique', name, length=80)
      self.bFps = ButtonWrapper('fps:', 0, 'number', initial=fps, min=1, max=999)
      self.bStart = ButtonWrapper('start:', 0, 'number', initial=start, min=1, max=100000)
      self.bEnd = ButtonWrapper('end:', 0, 'number', initial=end, min=1, max=100000)
      self.bDelete = ButtonWrapper('Delete', 0, 'push')

    def update(self, i, w, wPad, top):
      self.bFps.update([wPad+5, top-1, 70, 20])
      self.bStart.update([wPad+75, top-1, 70, 20])
      self.bEnd.update([wPad+145, top-1, 70, 20])
      self.bName.update([wPad+215, top-1, w-2*wPad-270, 20])
      self.bDelete.evt = Gui.animStart+i
      self.bDelete.update([w-wPad-55, top-1, 50, 20])

    def getAnim(self):
      return [self.bName.val, self.bFps.val, self.bStart.val, self.bEnd.val]

  def __init__(self):
    self.init()
    self.selection = None
    self.reportProgress = DrawProgressBar
    self.page = 0
    self.vMsg = 'Version %s'%__version__
    self.vMsgW = Draw.GetStringWidth(self.vMsg)+5
    self.logo = None
    try: # try to load the logo from the datadir
      self.logo = Image.Load(Blender.Get("datadir")+CHICKEN_LOGO)
    except IOError:
      path = Blender.Get('udatadir')
      if path:
        try: # if that doesn't work, try the user data dir
          self.logo = Image.Load(path+CHICKEN_LOGO)
        except IOError: pass # give up

    self.buttonFuncs = {}

    self.bReport = ButtonWrapper('View Report Page', 9, 'push')
    def fReport(): self.page = (self.page+1)%2
    self.buttonFuncs[9] = fReport

    self.bUpdate = ButtonWrapper('Update Selection', 1, 'push', 'Re-scan Selected Objects')
    def analyzeAndLoad():
      self.analyzeSelection()
      self.loadState()
    self.buttonFuncs[1] = analyzeAndLoad

    self.bFile = ButtonWrapper('Export File: ', 0, 'string', initial=self.filename, length=300)
    self.bSFile = ButtonWrapper('Select', 3, 'push')
    def fSFile():
      def updateFile(fn):
        self.bFile.val = makename(fn, ext='.egg')
      Window.FileSelector(updateFile,"Select Export File",self.bFile.val)
    self.buttonFuncs[3] = fSFile

    self.bAddAnim = ButtonWrapper('Add Animation', 4, 'push')
    def fAddAnim():
      i = len(self.animationRows)+1
      rate = 24
      base = 0
      if len(self.animationRows)!=0:
        rate = self.animationRows[-1].bFps.val
        base = self.animationRows[-1].bEnd.val
      self.animationRows.append(Gui.AnimationRow('anim%i'%i, rate, base+1, base+rate))
    self.buttonFuncs[4] = fAddAnim

    self.bMExtraction = ButtonWrapper('Motion Extraction', 0, 'toggle', "The animation will be exported as if the SRB were the origin, and the displacements will be stored as the SRB's animation", self.mExtract)
    self.bAnimOnly = ButtonWrapper('Animation Only', 0, 'toggle', initial=self.animOnly)
    self.bSingleFile = ButtonWrapper('Single File', 0, 'toggle', initial=self.singleFile)
    self.bDoTangents = ButtonWrapper('Tangents & Binormals', 0, 'toggle', initial=self.doTangents)
    self.bQuit = ButtonWrapper('Quit', 6, 'push', 'Exit Chicken')
    self.bForceRelTex = ButtonWrapper('Force Relative Tex', 0, 'toggle',
      initial=self.forceRelTex)
    self.bForceBFace = ButtonWrapper('Force Two-Sided', 0, 'toggle',
      initial=self.forceBFace)
    self.bOctree = ButtonWrapper('Make Octree', 0, 'toggle',
      initial=self.octree)
    self.bOctreeCollision = ButtonWrapper('Collision Octree', 0, 'toggle',
      initial=self.octreeCollision)
    self.buttonFuncs[6] = Draw.Exit

    self.bHelp = ButtonWrapper('Help', 7, 'push', 'See the documentation for the script (opens in web browser)')
    def fHelp():
      try: # try to find documentation in data dir
        path = 'file:///'+Blender.Get("datadir").replace('\\', '/')+CHICKEN_DOC
        webbrowser.open(path)
      except OSError:
        try: # if not, try in user data dir
          path = 'file:///'+Blender.Get("udatadir").replace('\\', '/')+CHICKEN_DOC
          webbrowser.open(path)
        except:
          Draw.PupMenu("Error%t|Documentation couldn't be found") # give up
    self.buttonFuncs[7] = fHelp

    self.bPzip = ButtonWrapper('pzip', 0, 'toggle', 'Compress the .egg', self.pzip)
    self.bEgg2Bam = ButtonWrapper('egg2bam', 0, 'toggle', 'Export additional BAM files for all exported Eggs', self.egg2bam)
    self.bPview = ButtonWrapper('pview', 0, 'toggle', 'Preview exported Eggs. Only first animation will be shown.', self.pview)
    self.bEggOptchar = ButtonWrapper('egg-optchar', 0, 'toggle', 'Optimize an exported character and its animations', self.optchar)
    self.bOptParms = ButtonWrapper('Params:', 0, 'string', 'Parameters for optimization. If blank "-inplace" will be used.', self.optParms, length=80)
    self.bExport = ButtonWrapper('Export', 2, 'push', 'Export with current settings')

    def fExport():
      if self.error:
        Draw.PupMenu('There are errors that make exporting impossible|See the report page for details')
      else:
        self.saveState()
        self.singleFile = self.bSingleFile.val
        self.animOnly = self.bAnimOnly.val
        self.doTangents = self.bDoTangents.val
        self.pzip = self.bPzip.val
        self.egg2bam = self.bEgg2Bam.val
        self.pview = self.bPview.val
        self.optchar = self.bEggOptchar.val
        self.optParms = self.bOptParms.val
        self.filename = self.bFile.val
        self.mExtract = self.bMExtraction.val
        self.forceRelTex = self.bForceRelTex.val
        self.forceBFace = self.bForceBFace.val
        self.octree = self.bOctree.val
        self.octreeCollision = self.bOctreeCollision.val
        self.anims = [ar.getAnim() for ar in self.animationRows]
        self.doExport()
    self.buttonFuncs[2] = fExport

    self.bSaveSettings = ButtonWrapper('Save', 8, 'push', 'Save export settings')

    def fSaveSettings():
      txt = None
      try:
        txt = Text.Get('export.chicken')
      except NameError: pass
      else:
        txt.setName('export.chicken.old')
      txt = Text.New('export.chicken')
      selection = map(lambda x: x.name, self.lastSelected)
      tools = (self.bPview.val, self.bEgg2Bam.val, self.bEggOptchar.val, self.bOctree.val)
      txt.write(MakeSettings(self.bFile.val, selection, self.anims, tools,
        self.bOptParms.val, self.bMExtraction.val, self.bAnimOnly.val,
        self.bOctreeCollision.val, self.bDoTangents.val, self.bSingleFile.val,
        self.bForceRelTex.val, self.bForceBFace.val, self.bPzip.val))
    self.buttonFuncs[8] = fSaveSettings

    if self.anims is None:
      name = 'anim'
      fps = Blender.Scene.GetCurrent().getRenderingContext().framesPerSec()
      start = Blender.Get('staframe')
      end = Blender.Get('endframe')
      self.anims = [[name, fps, start, end]]
    self.animationRows = [Gui.AnimationRow(*a) for a in self.anims]

    Draw.Register(self.draw, self.event, self.button)
    Draw.Draw()
    self.analyzeSelection()

    self.loadState() # Will only overwrite the above setting of animationRows if there is something to overwrite with.

  def draw(self):
    ui = Theme.Get()[0].get(-1)
    col = ui.setting
    col = map(lambda x: (x+40)/255.0, col[0:3])
    area = Window.GetAreaSize()
    w = area[0]; wPad = int(w*0.03)
    h = area[1]; hPad = int(h*0.03)
    #Draw Header
    BGL.glColor3f(*col)
    BGL.glRectf(wPad, h-hPad-10, w-wPad, h-hPad-40)
    if self.logo:
      BGL.glEnable( BGL.GL_BLEND ) # Only needed for alpha blending images with background.
      BGL.glBlendFunc(BGL.GL_SRC_ALPHA, BGL.GL_ONE_MINUS_SRC_ALPHA)
      Draw.Image(self.logo, wPad, h-hPad-90)
      BGL.glDisable( BGL.GL_BLEND )
    BGL.glColor3f(0.0,0.0,0.0)
    BGL.glRasterPos2i(w-wPad-self.vMsgW, h-hPad-30)
    Draw.Text(self.vMsg)

    BGL.glColor3f(0.3, 0.3, 0.3)
    BGL.glRectf(wPad, h-90, w-wPad, h-110)
    BGL.glColor3f(1.0,1.0,1.0)
    BGL.glRasterPos2i(wPad, h-105)
    if self.page is 0:
      Draw.Text('Status: ')
      if self.error:
        BGL.glColor3f(0.9, 0.0, 0.0)
        BGL.glRasterPos2i(wPad+40, h-105)
      Draw.Text(self.statusMsg)
      if self.success:
        if self.error:
          var = 'with errors.'
        else:
          var = 'successfully!'
        Draw.Text(' ...Exported %s  Time:%.3f sec'%(var,self.time))
      BGL.glColor3f(1.0, 1.0, 1.0)
      self.bReport.name = 'View Report Page'
      self.bReport.update([w-wPad-210, h-110, 110, 20])
      self.bUpdate.update([w-wPad-100, h-110, 100, 20])
      self.bFile.update([wPad+5, h-140, w-2*wPad-90, 20])
      self.bSFile.update([w-wPad-85, h-140, 80, 20])
      if len(self.meshes['armature']) > 0:
        BGL.glColor3f(0.5, 0.5, 0.5)
        BGL.glRectf(wPad, h-150, w-wPad, h-170)
        BGL.glColor3f(1.0,1.0,1.0)
        BGL.glRasterPos2i(wPad, h-165)
        Draw.Text('Animations:')
        top = h-200
        for i, r in enumerate(self.animationRows):
          r.update(i, w, wPad, top)
          top -= 22
        self.bAddAnim.update([wPad+20, top-1, 100, 20])
        if self.srb:
          self.bMExtraction.update([w-wPad-500, top-1, 110, 20])
        
        self.bDoTangents.update([w-wPad-390, top-1, 150, 20])
        self.bSingleFile.update([w-wPad-230, top-1, 100, 20])
        self.bAnimOnly.update([w-wPad-120, top-1, 100, 20])
        self.bForceRelTex.update([w-560, top-1, 150, 20])
        self.bForceBFace.update([w-700, top-1, 120, 20])
      else:
        self.bDoTangents.update([w-170, h-201, 150, 20])
        self.bOctree.update([w-494, h-201, 150, 20])
        self.bOctreeCollision.update([w-340, h-201, 150, 20])
        self.bForceRelTex.update([w-664, h-201, 150, 20])
        self.bForceBFace.update([w-804, h-201, 120, 20])

      self.bQuit.update([wPad, hPad, 40, 30])
      self.bHelp.update([wPad+45, hPad, 40, 30])
      BGL.glColor3f(1.0,1.0,1.0)
      BGL.glRasterPos2i(wPad+95, hPad+10)
      Draw.Text('Call:')
      self.bEgg2Bam.update([wPad+130, hPad+5, 60, 20])
      self.bPview.update([wPad+190, hPad+5, 40, 20])
      self.bPzip.update([wPad+230, hPad+5, 60, 20])
      if len(self.meshes['armature']) > 0:
        self.bEggOptchar.update([wPad+290, hPad+5, 80, 20])
        self.bOptParms.update([wPad+370, hPad+5, w-2*wPad-480, 20])
      if MakeSettings:
        self.bExport.update([w-wPad-85, hPad, 40, 30])
        self.bSaveSettings.update([w-wPad-40, hPad, 40, 30])
      else:
        self.bExport.update([w-wPad-85, hPad, 40, 30])

    elif self.page is 1:
      BGL.glRasterPos2i(wPad+5, h-105)
      Draw.Text('Report Page')
      self.bReport.name = 'Go Back'
      self.bReport.update([w-wPad-80, h-110, 80, 20])
      top = 125
      for m in self.messages:
        if m.severity == Message.Error:
          BGL.glColor3f(0.9, 0.0, 0.0)
        elif m.severity == Message.Warning:
          BGL.glColor3f(0.9, 0.45, 0.0)
        else:
          BGL.glColor3f(1.0, 1.0, 1.0)
        BGL.glRectf(wPad+5, h-top+15, w-wPad-5, h-top-5)
        BGL.glColor3f(0.0, 0.0, 0.0)
        BGL.glRasterPos2i(wPad+10, h-top)
        Draw.Text(m.message)
        top += 20

  def event(self, evt, val):
    if evt == Draw.ESCKEY or evt == Draw.QKEY:
      self.saveState()
      Draw.Exit()
    return

  def button(self, evt):
    if evt >= Gui.animStart:
      i = evt-Gui.animStart
      self.animationRows.pop(i)
    elif evt > 0:
      self.buttonFuncs[evt]()
    Draw.Redraw()

  def saveState(self):
    """Saves the animation list to a property in each animated mesh selected. Stores it as a string for ease of processing by fleshies."""
    data = []
    for row in self.animationRows:
      data.append((row.bName.val,row.bFps.val,row.bStart.val,row.bEnd.val))

    data = map(lambda x: x[0]+','+str(x[1])+','+str(x[2])+','+str(x[3]),data)
    if len(data)>1:
      data = reduce(lambda x,y:x+';'+y,data)
    elif len(data)==1:
      data = data[0]
    else:
      data = None

    for mesh in self.meshes['armature']:
      if data:
        mesh.properties['chicken_ani'] = data
      elif 'chicken_ani' in mesh.properties:
        del mesh.properties['chicken_ani']

  def loadState(self):
    """Loads the animation list as saved from above. Does nothing if theres nothing to load."""
    try:
      for mesh in self.meshes['armature']:
        if mesh.properties.has_key('chicken_ani'):
          data = mesh.properties['chicken_ani'].split(';')
          self.animationRows = []
          for d in data:
            item = d.rsplit(',',3)
            self.animationRows.append(Gui.AnimationRow(item[0],int(item[1]),int(item[2]),int(item[3])))
          break
    except Exception, e:
      print e



class Background(Exporter):
  '''
  This class encapsulates the things involved in user interaction through
  Blender's background mode or through chicken's interface Invoke function
  (when called from other scripts)
  '''
  def __init__(self):
    global exporter
    exporter = self
    
    if FORCE_BACKGROUND:
      print "Entering Chicken Forced Background mode. If you didn't call \
Chicken through the invocation function please unset the \
CHICKEN_FORCE_BACKGROUND environment variable"

    s = dict([(k.split('chicken_')[1], os.environ[k]) for k in os.environ.keys() if k.startswith('chicken_')])
    print s
    self.init(settings = os.getenv(SETTINGS_KEY), progress_range=os.getenv(RANGE_KEY), batchData=s)

    if FORCE_BACKGROUND:
      if Blender.mode == 'interactive':
        self.reportProgress = DrawProgressBar
      msg_txt = Text.New('messages.chicken')
      os.environ[MESSAGE_KEY] = msg_txt.getName()

    self.analyzeSelection()
    if FORCE_BACKGROUND:
      pre = [self.messages[:]]
    else:
      print "Pre-Export messages:"
      print self.statusMsg
      for m in self.messages:
        print m

    self.doExport()
    if self.success and not FORCE_BACKGROUND:
      print 'Success! Total Export time (including invocations): %.3f seconds'%self.time
      print 'Geometry: %s'%self.filename
      if len(self.anims) > 0:
        anim_names = ' '.join([a[0] for a in self.anims])
        print 'Animations: %s'%anim_names

    if FORCE_BACKGROUND:
      pre.extend([self.messages])
      try:
        import cPickle
        msg_txt.write(cPickle.dumps(tuple(pre), protocol=0))
      except:
        pass
    else:
      print 'Post-Export messages:'
      print self.statusMsg
      for m in self.messages:
        print m
  def reportProgress(self, prog, msg):
    print 'Exporting... %.2f percent done'%(prog*100)



class Material:
  def __init__(self, mat, group):
    self.name = mat.name
    self.users = 0
    factor = mat.spec/2.0
    self.diff = (mat.R, mat.G, mat.B)
    self.spec = (mat.specR*factor, mat.specG*factor, mat.specB*factor)
    self.shine = mat.hard/4.0
    self.vlight = mat.mode & BMaterial.Modes.VCOL_LIGHT
    self.vpaint = mat.mode & BMaterial.Modes.VCOL_PAINT
    self.shadeless = mat.mode & BMaterial.Modes.SHADELESS # Not sure how this is actually used - just removes the material from the geometry it is applied to. Seems silly.
    self.ztransp = mat.getMode() & BMaterial.Modes["ZTRANSP"]
    self.texface = mat.getMode() & BMaterial.Modes["TEXFACE"]
    self.textures = []
    # process textures

    if group.mesh:
      uvnames = group.mesh.getUVLayerNames()
      if len(uvnames) > 0:
        textures = [] #textures that use UVs
        texgenTextures = [] #here we'll store the MTex of textures that don't use UVs
        texcount = 0
        for mtexno, mtex in enumerate(mat.getTextures()):
          if (mtexno in mat.enabledTextures) and type(mtex) == Types.MTexType and mtex.tex.getType() == 'Image':
            if mtex.texco == BTexture.TexCo.UV:
              if mtex.uvlayer in uvnames: uv = mtex.uvlayer
              else: uv = uvnames[0] # if the UVLayer isn't valid for this mesh use the first
              list = textures
            else:
              uv = None
              list = texgenTextures

            if mtex.mtCol == 1 or mtex.mtNor == 1 or mtex.mtSpec == 1 or mtex.mtEmit == 1 or mtex.mtDisp == 1 or mtex.stencil:
              if mtex.mtNor == 1 and not mat.mode & BMaterial.Modes.NMAP_TS:
                exporter.messages.append(Message('Material %s is not using tangent space normal maps. Appearance will differ from Blender.'%self.name, Message.Warning))
              list.append([mtex,None,uv])
              texcount += 1
            elif mtex.mtAlpha == 1:
              appended = False
              for texSpec in reversed(list):
                if texSpec[0].mtCol == 1 and texSpec[2] == uv:
                  appended = True
                  texSpec[1] = mtex #place as alpha texture of last color texture on this UVlayer
                  break
              if not appended:
                list.append([mtex, None, uv]) #place as its own texture

        mtexPrior = None
        for i,texSpec in enumerate(textures):
          try:
            filename = texSpec[0].tex.getImage().getFilename()
          except:
            raise Exception('Could not get image filename for texture. Chicken only supports textures stored in external files. This error happens if the texture is either procedural (In which case bake it.), or packed (In which case unpack it and save it to an external file.).')
          name = self.name + '_' + str(i).zfill(2) + '_' + texSpec[0].tex.getName()
          pTex = Texture(name, filename, texSpec[2], texSpec[0], mtexPrior, mat = self)
          mtexPrior = pTex
          TEXTURES[name] = pTex
          self.textures.append(name)
          if texSpec[1]:
            aFilename = None
            aImage = texSpec[1].tex.getImage()
            if texSpec[1] is not texSpec[0] and aImage:
              aFilename = aImage.getFilename()
            pTex.setAlphaChannel(aFilename)

        #TODO: process texgenTextures

  def getRef(self):
    for tex in self.textures:
      TEXTURES[tex].users += 1
    return self.textures

  def __repr__(self):
    return '[Material %s, users:%i]'%(self.name, self.users)

  def write(self, buffer):
    ln =  ['<Material> %s {'%eggSafeName(self.name)]
    if not self.vpaint:
      ln += ['  <Scalar> diffr {%s}\n  <Scalar> diffg {%s}\n  <Scalar> diffb {%s}'%self.diff]
    ln += ['  <Scalar> specr {%s}\n  <Scalar> specg {%s}\n  <Scalar> specb {%s}'%self.spec]
    ln += ['  <Scalar> shininess {%s}'%self.shine]
    ln += ['}']
    buffer.extend(ln)



class Texture:
  def __init__(self, name, filename, uvname=None, mtex=None, mtexPrior=None, mat=None):
    self.name = name
    self.users = 0
    self.filename = convertFileNameToPanda(filename)
    self.hasAlpha = mtex and mtex.mtAlpha != 0
    # hasMappedAlpha is True when it really has alpha mapped to it.
    # Sounds the same as hasAlpha, but it's *not*.
    self.hasMappedAlpha = self.hasAlpha
    self.alphaFileName = None
    self.uvname = uvname
    self.envtype = 'modulate'
    self.negrgb = False
    self.negalpha = mtex and mtex.mtAlpha < 0
    if mat != None:
      self.ztransp = mat.ztransp
      self.texface = mat.texface
    else:
      self.ztransp = False
      self.texface = False
      exporter.messages.append(Message("Blender texture %s has no material - it will have been assigned via the uv system. Whilst unusual this is not necessarily a problem."%name, Message.Warning))
    self.mipmap = True
    self.offset = (0, 0, 0)
    self.scale = (1, 1, 1)
    self.filter = 'linear'
    self.wrap = {'u': 'repeat', 'v': 'repeat', 'w': 'repeat'}
    self.prevTex = mtexPrior
    self.affectsDiffuse = True
    self.stencil = mtex and mtex.stencil
    self.postStencil = mtexPrior and mtexPrior.stencil

    # Hack to force the first texture in a stencil to use replace rather than modulate - bug in Panda breaks things otherwise...
    if self.stencil and self.prevTex.prevTex==None:
      self.prevTex.envtype = 'replace'

    # If we are forcing texture filepaths to be relative do so, otherwise detect if there are any that are not and emit a warning...
    if (len(self.filename)>0) and (self.filename[0]=='/'):
      if exporter.forceRelTex:
        self.filename = getRelativePath(self.filename,exporter.filename)
      else:
        exporter.messages.append(Message("Blender Texture %s has an absolute filename."%mtex.tex.name, Message.Warning))

    if mtex:
      # Change the env type based on the drop down mixing mode selector - only a few are supported of course, but better than none...
      if mtex.blendmode==BTexture.BlendModes.MIX:
        if MAP_MIX_TO_MODULATE:
          self.envtype = 'modulate'
        else:
          # We only mix if their is already a texture we can mix with - check the chain of previous textures for a 'standard' texture - if there isn't one set the mode to modulate instead...
          foundDiffuse = False
          targ = self.prevTex
          while targ!=None:
            if targ.affectsDiffuse:
              foundDiffuse = True
              break
            targ = targ.prevTex

          if foundDiffuse:
            self.envtype = 'mix'
          else:
            self.envtype = 'modulate'
      elif mtex.blendmode==BTexture.BlendModes.MULTIPLY:
        self.envtype = 'modulate'
      elif mtex.blendmode==BTexture.BlendModes.ADD:
        self.envtype = 'add'
      elif mtex.blendmode==BTexture.BlendModes.SCREEN:
        self.envtype = 'decal'

      # Detect if its a usable normal map...
      if mtex.mtNor != 0 and uvname:
        if mtex.tex.imageFlags & BTexture.ImageFlags.NORMALMAP:
          self.envtype = 'normal'
          self.affectsDiffuse = False
          exporter.normalMappedUVs.add(uvname)
        else:
          exporter.messages.append(Message('Exporting a parallax map - this feature is only supported in Panda 1.7.0 and above.', Message.Warning))
          self.envtype = 'height'
          self.affectsDiffuse = False
        if mtex.neg ^ bool(mtex.mtNor < 0):
          # Actually, for parallax maps this will be supported later, by inverting the parallax scale.
          exporter.messages.append(Message('Inverted normalmaps are not supported yet.', Message.Warning))

      # Detect if it is a specularity map...
      if mtex.mtSpec != 0 and uvname:
        self.envtype = 'gloss'
        self.affectsDiffuse = False
        if mtex.neg ^ bool(mtex.mtSpec < 0):
          exporter.messages.append(Message('Inverted specular maps are not supported yet.', Message.Warning))

      # Detect if its a glow map...
      if mtex.mtEmit != 0 and uvname:
        self.envtype = 'glow'
        self.affectsDiffuse = False
        if mtex.neg ^ bool(mtex.mtEmit < 0):
          exporter.messages.append(Message('Inverted glow maps are not supported yet.', Message.Warning))

      # Extract the mipping options from the texture...
      self.mipmap = (BTexture.ImageFlags.MIPMAP & mtex.tex.imageFlags)
      if not (BTexture.ImageFlags.INTERPOL & mtex.tex.imageFlags):
        self.filter = 'nearest'
      if self.mipmap:
        self.filter = self.filter + '_mipmap_' + self.filter

      # Extract the wrapping mode...
      wrap_mode = mtex.tex.extend
      if wrap_mode == (BTexture.ExtendModes.EXTEND):
        self.wrap['u'] = self.wrap['v'] = self.wrap['w'] = 'clamp'
      elif wrap_mode in [BTexture.ExtendModes.CLIP, BTexture.ExtendModes.CLIPCUBE]:
        self.wrap['u'] = self.wrap['v'] = self.wrap['w'] = 'border_color'
      tflags = mtex.tex.flags
      umir = BTexture.Flags.REPEAT_XMIR & tflags
      vmir = BTexture.Flags.REPEAT_YMIR & tflags
      if umir or vmir:
          # When we select "mir" option for a texture component in Blender,
          # the other one is extended (clamp). I know: it's not logical...
          self.wrap['u'] = self.wrap['v'] = self.wrap['w'] = 'clamp'
          if umir:
              self.wrap['u'] = 'mirror'
          if vmir:
              self.wrap['v'] = 'mirror'
      
      # Load in data for TexMatrix
      self.offset = tuple([float(o) for o in mtex.ofs])
      self.scale = tuple([float(o) for o in mtex.size])
      # We need to transform them a bit because Blender resizes textures differently.
      self.offset = tuple([self.offset[o] / self.scale[o] + 0.5 * (self.scale[0] / abs(self.scale[0])) * abs(1 - (1 / self.scale[o])) for o in [0, 1, 2]])
      if BTexture.Flags.FLIPBLEND & tflags:
        exporter.messages.append(Message('FLIPBLEND functionality is not supported yet.', Message.Warning))

      # Not sure if mtex.neg is supposed to affect alpha as well.
      # I've experimented a bit with it in Blender and it *seems* not.
      self.negrgb = mtex.neg
      self.negalpha = bool(BTexture.Flags.NEGALPHA & tflags)

  def setAlphaChannel(self, alphaFileName = None):
    self.hasAlpha = True
    if alphaFileName:
      self.alphaFileName = convertFileNameToPanda(alphaFileName)

  def __repr__(self):
    return '[Texture %s, users:%i, fn:%s, a:%s]'%(self.name, self.users, self.filename, str(self.hasAlpha))

  def write(self, buffer):
    ln = ['<Texture> %s {'%eggSafeName(self.name),'  "%s"'%self.filename]

    if self.uvname and self.uvname!='UVTex':
      ln.append('  <Scalar> uv-name { %s }'%self.uvname)

    if self.hasAlpha and not self.stencil:
      if self.alphaFileName:
        ln.append('  <Scalar> alpha-file { "%s" }'%self.alphaFileName)
      ln.append('  <Scalar> format { RGBA }')
      # If TexFace is enabled, it is set per polygon.
      if not self.texface:
        if self.ztransp:
          ln.append('  <Scalar> alpha { DUAL }')
        else:
          # I'm not sure about this, but I just left it
          # for the sake of backward compatibility.
          ln.append('  <Scalar> alpha { BLEND_NO_OCCLUDE }')
          ln.append('  <Scalar> draw_order { 10000 }')

    if self.stencil:
      self.envtype = 'replace'
    else:
      ln.append('  <Scalar> saved-result { 1 }')

    if self.postStencil:
      ln.append('  <Scalar> combine-rgb { INTERPOLATE }')
      ln.append('  <Scalar> combine-rgb-source0 { TEXTURE }')
      if self.negrgb:
        ln.append('  <Scalar> combine-rgb-operand0 { ONE-MINUS-SRC-COLOR }')
      else:
        ln.append('  <Scalar> combine-rgb-operand0 { SRC-COLOR }')
      ln.append('  <Scalar> combine-rgb-source1 { LAST_SAVED_RESULT }')
      ln.append('  <Scalar> combine-rgb-operand1 { SRC-COLOR }')
      ln.append('  <Scalar> combine-rgb-source2 { PREVIOUS }')
      ln.append('  <Scalar> combine-rgb-operand2 { SRC-COLOR }')
      ln.append('  <Scalar> combine-alpha { REPLACE }')
      ln.append('  <Scalar> combine-alpha-source0 { CONSTANT }')
      ln.append('  <Scalar> combine-alpha-operand0 { SRC-ALPHA }')

    elif (self.negrgb or self.negalpha) and self.envtype.lower() == 'replace':
      ln.append('  <Scalar> combine-rgb { REPLACE }')
      if self.negrgb:
        ln.append('  <Scalar> combine-rgb-operand0 { ONE-MINUS-SRC-COLOR }')
      else:
        ln.append('  <Scalar> combine-rgb-operand0 { SRC-COLOR }')

      if self.negalpha:
        ln.append('  <Scalar> combine-alpha-operand0 { ONE-MINUS-SRC-ALPHA }')
      else:
        ln.append('  <Scalar> combine-alpha-operand0 { SRC-ALPHA }')

    elif self.envtype.lower() == 'mix':
      # Implement our own version of Mix / Decal using combine modes.
      ln.append('  <Scalar> combine-rgb { INTERPOLATE }')
      ln.append('  <Scalar> combine-rgb-source1 { PREVIOUS }')
      ln.append('  <Scalar> combine-rgb-operand1 { SRC-COLOR }')
      ln.append('  <Scalar> combine-rgb-source2 { TEXTURE }')
      ln.append('  <Scalar> combine-rgb-operand2 { SRC-ALPHA }')
      ln.append('  <Scalar> combine-rgb-source0 { TEXTURE }')
      if self.negrgb:
        ln.append('  <Scalar> combine-rgb-operand0 { ONE-MINUS-SRC-COLOR }')
      else:
        ln.append('  <Scalar> combine-rgb-operand0 { SRC-COLOR }')

      ln.append('  <Scalar> combine-alpha { ADD }')
      ln.append('  <Scalar> combine-alpha-source1 { PREVIOUS }')
      ln.append('  <Scalar> combine-alpha-operand1 { SRC-ALPHA }')
      ln.append('  <Scalar> combine-alpha-source0 { TEXTURE }')
      if self.negalpha:
        ln.append('  <Scalar> combine-alpha-operand0 { ONE-MINUS-SRC-ALPHA }')
      else:
        ln.append('  <Scalar> combine-alpha-operand0 { SRC-ALPHA }')

    elif (self.negrgb or self.negalpha) and self.envtype.lower() in ['modulate', 'add', 'subtract']:
      # This maps usual modes to combine modes, because we can invert stuff there.
      ln.append('  <Scalar> combine-rgb { %s }'%self.envtype.upper())
      ln.append('  <Scalar> combine-alpha { %s }'%self.envtype.upper())
      ln.append('  <Scalar> combine-rgb-source0 { PREVIOUS }')
      ln.append('  <Scalar> combine-rgb-operand0 { SRC-COLOR }')
      ln.append('  <Scalar> combine-alpha-source0 { PREVIOUS }')
      ln.append('  <Scalar> combine-alpha-operand0 { SRC-ALPHA }')
      if self.envtype.lower() != 'replace':
        ln.append('  <Scalar> combine-rgb-source1 { TEXTURE }')
        ln.append('  <Scalar> combine-alpha-source1 { TEXTURE }')

      if self.negrgb:
        ln.append('  <Scalar> combine-rgb-operand1 { ONE-MINUS-SRC-COLOR }')
      else:
        ln.append('  <Scalar> combine-rgb-operand1 { SRC-COLOR }')

      if self.negalpha:
        ln.append('  <Scalar> combine-alpha-operand1 { ONE-MINUS-SRC-ALPHA }')
      else:
        ln.append('  <Scalar> combine-alpha-operand1 { SRC-ALPHA }')

    else:
      # Just use the usual envtype now - no need for something special.
      ln.append('  <Scalar> envtype { %s }'%self.envtype.upper())

    filter_name = self.filter.upper()
    ln.append('  <Scalar> minfilter { %s }'%filter_name)
    ln.append('  <Scalar> magfilter { %s }'%filter_name)

    wrapu = self.wrap['u'].upper()
    wrapv = self.wrap['v'].upper()
    wrapw = self.wrap['w'].upper()
    if (wrapu == wrapv) and (wrapu == wrapw):
      ln.append('  <Scalar> wrap { %s }'%wrapu)
    else:
      ln.append('  <Scalar> wrapu { %s }'%wrapu)
      ln.append('  <Scalar> wrapv { %s }'%wrapv)
      ln.append('  <Scalar> wrapw { %s }'%wrapw)

    if self.offset != (0, 0, 0) or self.scale != (1, 1, 1):
      ln.append('  <Transform> {')
      if self.offset:
        ln.append('    <Translate> { %s }'%(' '.join([str(v) for v in self.offset])))
      if self.scale:
        ln.append('    <Scale> { %s }'%(' '.join([str(v) for v in self.scale])))
      ln.append('  }')

    ln.append('}')
    buffer.extend(ln)



class Group:
  def __init__(self, name = '', mesh = None, anim = False, addTangents = False):
    self.children = []
    self.polys = []
    self.verts = []
    self.bverts2mverts = None
    self.anim = anim
    self.tags = {}
    self.objectType = None
    self.collide = None
    self.forceEmpty = False # If True then any static geometry is ignored - it becomes an empty. (Child objects will still be exported as normal however.)
    self.switchCond = None

    self.blendmode = None
    self.blendopA = None
    self.blendopB = None
    self.blendcolor = [None, None, None, None]

    self.scroll_u = None
    self.scroll_v = None
    self.scroll_r = None

    if not mesh:
      self.name = name
      self.transform = None
    else:
      self.name = mesh.name
      # grab and interpret properties
      props = mesh.getAllProperties()
      for p in props:
        name = p.getName()
        data = str(p.getData())
        self.tags[name] = data
      if 'ObjectType' in self.tags:
        self.objectType = self.tags.pop('ObjectType')
        
      if 'Collide' in self.tags:
        self.collide = self.tags.pop('Collide')
        
      if 'ForceEmpty' in self.tags:
        self.tags.pop('ForceEmpty')
        self.forceEmpty = True
      
      if 'SwitchCondition' in self.tags:
        self.switchCond = self.tags.pop('SwitchCondition')
        
        
      if 'blend' in self.tags:
        self.blendmode = self.tags.pop('blend')
      if 'blendop-a' in self.tags:
        self.blendopA = self.tags.pop('blendop-a')
      if 'blendop-b' in self.tags:
        self.blendopB = self.tags.pop('blendop-b')
        
      if 'blendr' in self.tags:
        self.blendcolor[0] = self.tags.pop('blendr')
      if 'blendg' in self.tags:
        self.blendcolor[1] = self.tags.pop('blendg')
      if 'blendb' in self.tags:
        self.blendcolor[2] = self.tags.pop('blendb')
      if 'blenda' in self.tags:
        self.blendcolor[3] = self.tags.pop('blenda')

      if 'scroll_u' in self.tags:
        self.scroll_u = self.tags.pop('scroll_u')
      if 'scroll_v' in self.tags:
        self.scroll_v = self.tags.pop('scroll_v')
      if 'scroll_r' in self.tags:
        self.scroll_r = self.tags.pop('scroll_r')

      self.transform = mesh.matrix

      if mesh.getType() == 'Empty' or self.forceEmpty: #empties get tags and the transform
        if not self.objectType:
          self.objectType = 'model' #prevent flattening of empties unless otherwise specified
        return


      # Go through the modifiers of the object and disable those we don't want...
      foundArm = False
      modRestore = []
      for mod in mesh.modifiers:
        if foundArm or (mod.type == Modifier.Type.ARMATURE):
          foundArm = True
          modRestore.append((mod,mod[Modifier.Settings.RENDER]))
          mod[Modifier.Settings.RENDER] = False
      
      # Make a transformed/simplified mesh copy to speed up verts, this is also wqhere modifiers are applied...
      scn = Blender.Scene.GetCurrent()
      self.tmesh = Mesh.New()
      self.tmesh.getFromObject(mesh,0,1) # Implicitly applies modifiers.
      self.tmesh.transform(mesh.matrix)
      tempObj = scn.objects.new(self.tmesh)
      
      self.mesh = mesh.getData(mesh=1)

      # Restore the modifier settings...
      for mod,setting in modRestore:
        mod[Modifier.Settings.RENDER] = setting
      
      
      # Calculate the tangents if desired...
      if addTangents and (len(self.tmesh.getUVLayerNames())!=0):
        tangents = []
        for uvLayer in self.tmesh.getUVLayerNames():
          self.tmesh.activeUVLayer = uvLayer
          tangents.append(self.tmesh.getTangents())
      else:
        tangents = None

      # If needed generate the ShapeKey object for this mesh...
      if DO_SHAPE_KEYS and (self.mesh.key!=None) and (len(self.mesh.key.blocks)!=0):
        print 'Shapekeys detected'
        self.shapeKeys = ShapeKeys(self.mesh, mesh.matrix)

      # Assorted stuff...
      hasUV, hasVCol = self.mesh.faceUV, self.mesh.vertexColors
      mats = self.mesh.materials
      if anim:
        self.transform = None
        self.bverts2mverts = {}

      # Process materials that haven't been processed yet...
      for mat in mats:
        if mat and mat.name not in MATERIALS:
          MATERIALS[mat.name] = Material(mat, self)

      if len(mats) <= 1:
        for i,face in enumerate(self.tmesh.faces):
          self.polys.append(Polygon(face, i, self, hasUV, hasVCol, mats, tangents))
      else: # Group by material indices if there's more than one
        def mon(i):
          if mats[i]!=None: name = mats[i].name
          else: name = ''
          return self.name + '_' + str(i).zfill(2) + '_' + name
        self.children = [Group(mon(i)) for i in xrange(len(mats))]
        for i,face in enumerate(self.tmesh.faces):
          p = Polygon(face, i, self, hasUV, hasVCol, mats, tangents)
          self.children[face.mat].polys.append(p)
        # filter those unused
        self.children = filter(lambda c: len(c.polys) > 0, self.children)

      # Remove tempory transformed mesh...
      scn.objects.unlink(tempObj)
      del self.tmesh

  def __repr__(self, padding = ''):
    ln = [padding+'[Group %s, polys:%i, verts:%i]'%(self.name, len(self.polys), len(self.verts))]
    padding += ' '
    ln.extend([c.__repr__(padding) for c in self.children])
    return '\n'.join(ln)

  def write(self, buffer, padding = ''):
    buffer.append('%s<Group> %s {'%(padding, eggSafeName(self.name)))
    self.writeInner(buffer, padding)
    buffer.append('%s}'%(padding))

  def writeInner(self, buffer, padding = ''): # separated for Character reuse
    self.writeTransform(buffer, padding)
    padding2 = padding+'  '
    for k,v in self.tags.iteritems():
      buffer.append('%s<Tag> %s { %s }'%(padding2, k, v))
    if self.objectType:
      buffer.append('%s<ObjectType> { %s }'%(padding2, self.objectType))
    if self.collide:
      buffer.append('%s<Collide> { %s }'%(padding2, self.collide))
      
    if self.blendmode:
      buffer.append('%s<Scalar> blend { %s }'%(padding2, self.blendmode))
    if self.blendopA:
      buffer.append('%s<Scalar> blendop-a { %s }'%(padding2, self.blendopA))
    if self.blendopB:
      buffer.append('%s<Scalar> blendop-b { %s }'%(padding2, self.blendopB))

    if self.blendcolor[0]:
      buffer.append('%s<Scalar> blendr { %s }'%(padding2, self.blendcolor[0]))
    if self.blendcolor[1]:
      buffer.append('%s<Scalar> blendg { %s }'%(padding2, self.blendcolor[1]))
    if self.blendcolor[2]:
      buffer.append('%s<Scalar> blendb { %s }'%(padding2, self.blendcolor[2]))
    if self.blendcolor[3]:
      buffer.append('%s<Scalar> blenda { %s }'%(padding2, self.blendcolor[3]))

    if self.scroll_u:
      buffer.append('%s<Scalar> scroll_u { %s }'%(padding2, self.scroll_u))
    if self.scroll_v:
      buffer.append('%s<Scalar> scroll_v { %s }'%(padding2, self.scroll_v))
    if self.scroll_r:
      buffer.append('%s<Scalar> scroll_r { %s }'%(padding2, self.scroll_r))

    if self.switchCond:
      buffer.append('%s<SwitchCondition> {'%padding2)
      buffer.append('%s  <Distance> {'%padding2)
      buffer.append('%s    %s <Vertex> { 0.0 0.0 0.0 }'%(padding2,self.switchCond))
      buffer.append('%s  }'%padding2)
      buffer.append('%s}'%padding2)

    if not self.forceEmpty:
      if len(self.verts) > 0:
        buffer.append('%s<VertexPool> %s {'%(padding2, eggSafeName(self.name)))
        padding3 = padding2+'  '
        for v in self.verts:
          v.write(buffer, padding3)
        buffer.append('%s}'%(padding2))
      for p in self.polys:
        p.write(buffer, padding2)

    for c in self.children:
      c.write(buffer, padding2)

  def writeTransform(self, buffer, padding): # separated for Joint reuse
    if self.transform and self.transform != IDENTITY:
      m = self.transform
      buffer.append('%s  <Transform> {'%padding)
      buffer.append('%s    <Matrix4> {'%padding)
      buffer.append('%s      %f %f %f %f'%(padding, m[0][0], m[0][1], m[0][2], m[0][3]))
      buffer.append('%s      %f %f %f %f'%(padding, m[1][0], m[1][1], m[1][2], m[1][3]))
      buffer.append('%s      %f %f %f %f'%(padding, m[2][0], m[2][1], m[2][2], m[2][3]))
      buffer.append('%s      %f %f %f %f'%(padding, m[3][0], m[3][1], m[3][2], m[3][3]))
      buffer.append('%s    }'%padding)
      buffer.append('%s  }'%padding)



class Character(Group):
  def __init__(self, armature, meshes, srb, animOnly = False, addTangents = False):
    '''
    Constructor
    @param armature: The Armature object that defines this character
    @param meshes: A list of Mesh objects that define the geometry for this character
    @param animOnly: Flag that indicates whether this character is being generated solely for exporting animation
    '''
    Group.__init__(self, armature.name,addTangents = addTangents)
    self.armature = armature
    arm_mat = armature.matrix
    self.mat = arm_mat
    if not animOnly:
      self.children = [Group(mesh=m, anim = True,addTangents = addTangents) for m in meshes]
    arm_data = armature.getData()
    bones = arm_data.bones.values()
    self.bones = arm_data.bones
    self.boneNames = arm_data.bones.keys()
    if srb:
      srbIndex = self.boneNames.index('SyntheticRootBone') # get the index where I'll find the bone and name
      self.boneNames.pop(srbIndex) # pop the name
      srbBone = bones.pop(srbIndex) # pop the bone so we don't treat it like the other joints
      self.srb = Joint(srbBone, arm_mat, animOnly) # make the joint and store it separately
    else: self.srb = None
    #begin reconstruction of hierarchy
    parents = map(lambda x: x.parent, bones)
    jointList = [Joint(bone, arm_mat, animOnly) for bone in bones]
    joints = dict([(j.origName, j) for j in jointList])
    roots = []
    self.roots = roots
    for i, p in enumerate(parents):
        if p:
          joints[p.name].children.append(jointList[i])
        else:
          roots.append(jointList[i])
    #end
    
    # Assigning weight references - store in each joint which vertices use it...
    if not animOnly:
      for c in self.children:
        cmesh = c.mesh
        cname = c.name
        mapping = c.bverts2mverts
        for i in xrange(len(cmesh.verts)):
          inf = cmesh.getVertexInfluences(i)
##          if len(inf) > 4: print 'trouble' # maybe do something about that
          for w in inf:
            try:
              joint = joints[w[0]]
              key = (w[1], cname)
              indices = joint.weights.get(key, None)
              if not indices:
                indices = []
                joint.weights[key] = indices
              indices.extend(mapping[i])
            except KeyError: pass # ignore vertex groups that aren't for bones
    #end

  def __repr__(self, padding = ''):
    ln = [padding+'[Character %s, polys:%i, verts:%i]'%(self.name, len(self.polys), len(self.verts))]
    padding += ' '
    ln.extend([c.__repr__(padding) for c in self.children])
    ln.extend([j.__repr__(padding) for j in self.roots])
    return '\n'.join(ln)

  def write(self, buffer, padding = ''):
    buffer.append('%s<Group> %s {'%(padding, eggSafeName(self.name)))
    buffer.append('%s  <DART> { 1 }'%padding)
    self.writeInner(buffer, padding) # separated so the Character class can reuse this part
    padding2 = padding + '  '
    for j in self.roots:
      j.write(buffer,padding2)
    if self.srb:
      self.srb.write(buffer, padding2)
    buffer.append('%s}'%(padding))

  def writeAnims(self, charfilename, anims, out_file=None):
    '''
    Writes animations specified in a list into separate files whose filenames are based on the one passed in
    @param charfilename: The filename to which the character was exported
    @param anims: List of animation specifications, which should be tuples of the form (name, fps, startframe, endframe)
    '''
    if len(anims) == 0:
      return
    framelims = []
    # calculate total range for all anims
    for a in anims:
      framelims.extend([a[2],a[3]])
    minframe = min(framelims)
    maxframe = max(framelims)
    # collect local posematrices for every frame and bone in that range
    bones = self.bones
    boneNames = self.boneNames
    armature = self.armature
    mat = self.mat
    poses = [[]for name in boneNames] # lists of local posematrices for every bone
    if self.srb:
      srb = self.srb
      srbDeltas = []
    else: srb = None
    srbIMatPrev = IDENTITY
    oldframe = Blender.Get('curframe')
    ###### adding stuff to get access to the currentFrame
    scn = Blender.Scene.GetCurrent()
    context = scn.getRenderingContext()
    ###### done with preparing change frames
    for f in xrange(minframe,maxframe+1):
      context.currentFrame(f)
      scn.update(1)
      pbones = armature.getPose().bones
      if srb:
        srbMat = Matrix(pbones['SyntheticRootBone'].poseMatrix)
        srbDeltas.append(srbMat * srbIMatPrev)
        srbIMatPrev = srbMat.invert() # if there is no srb this will always be just identity
      for i, name in enumerate(boneNames):
        pbone = pbones[name]
        parent = bones[name].parent
        if parent:
          imat = (pbones[parent.name].poseMatrix*mat*srbIMatPrev).invert()
          poses[i].append(pbone.poseMatrix*mat*srbIMatPrev * imat)
        else:
          poses[i].append(pbone.poseMatrix*mat*srbIMatPrev)
    Blender.Set('curframe', oldframe)
    poses = dict([(name, poses[i]) for i, name in enumerate(boneNames)]) # convert poses to a dictionary like this (bonename:[posematrices])
    if srb:
      poses['SyntheticRootBone'] = srbDeltas
    # begin export of animations
    for a in anims:
      if a[2] > a[3]:
        r = range(a[2]-minframe, a[3]-minframe-1, -1)
      else:
        r = range(a[2]-minframe, a[3]-minframe+1)
      if out_file is None:
        buffer = INITIAL[:]
      else:
        buffer = ["",]
      buffer.append('<Table> {')
      if out_file is None: # If files are seperate it must be the name of the group it applies to, else the name of the animation.
        buffer.append('  <Bundle> %s {'%eggSafeName(self.name))
      else:
        buffer.append('  <Bundle> %s {'%eggSafeName(a[0]))
      buffer.append('    <Table> "<skeleton>" {')
      padding = '      '
      for j in self.roots:
        j.writeAnim(a[1], r, poses, buffer, padding)
      if srb:
        self.srb.writeAnim(a[1], r, poses, buffer, padding)
      buffer.append('    }')
      buffer.append('  }')
      buffer.append('}')
      if out_file is None:
        fn = '%s-%s'%(charfilename, a[0].replace('.', '_'))
        out_file = open(makename(fn, '.egg'),"w")
        out_file.write('\n'.join(buffer))
        out_file.close()
        out_file = None
      else:
        out_file.write('\n'.join(buffer))



class Link(Group):
  """An object that links to another file rather than containing the geometry in this file."""
  def __init__(self, mesh):
    Group.__init__(self, mesh=mesh)
    self.dupgrp = mesh.DupGroup

  def __repr__(self, padding = ''):
    ln = [padding+'[Link %s]'%(self.name)]
    padding += ' '
    ln.extend([c.__repr__(padding) for c in self.children])
    return '\n'.join(ln)

  def write(self, buffer, padding = ''):
    if self.forceEmpty:
      Group.write(self,buffer,padding)
      return

    buffer.append('%s<Instance> %s {'% (padding,eggSafeName(self.name)))
    self.writeInner(buffer, padding)

    filename = None
    if self.tags.has_key('filename'): # Try the empty for a filename.
      filename = str(self.tags['filename'])

    if filename==None:
      for obj in list(self.dupgrp.objects): # Try the duplicated objects for a filename.
        props = obj.getAllProperties()
        for p in props:
          if 'filename'==p.getName():
            filename = str(p.getData())
            break
        if filename:
          break

    if filename==None:
      if self.dupgrp.lib is not None:
        filename = self.dupgrp.lib.replace('.blend', '') # Get the name from the file.
      else:
        filename = eggSafeName(self.dupgrp.name) # Get the name from the group.

    buffer.append('%s  <File> { %s }' % (padding,convertFileNameToPanda(filename)))
    buffer.append('%s}'%(padding))



class Vertex:
  def __init__(self, vert, index, color=None, normal=False, multiuv=None, tangents=None, faceNormal=None, shapeKeysDict=None):
    self.index = index
    self.coords = vert.co
    self.color = color
    self.shapeKeysDict = shapeKeysDict
    self.vindex = vert.index
    if normal: self.normal = vert.no
    else: self.normal = None
    
    if multiuv:
      if tangents:
        self.doTangent = True
        if not self.normal: # We need a normal to cross with for flat shaded faces to get the bi-tangent.
          self.faceNormal = faceNormal
        mesh, face_i, vert_i = multiuv
        def getMultiTangentUV(name,tans):
          mesh.activeUVLayer = name
          uv = mesh.faces[face_i].uv[vert_i]
          tangent = tans[face_i][vert_i]
          return (name, uv, tangent)
        self.uv = map(getMultiTangentUV, mesh.getUVLayerNames(), tangents)
      else:
        self.doTangent = False
        mesh, face_i, vert_i = multiuv
        def getMultiUV(name):
          mesh.activeUVLayer = name
          uv = mesh.faces[face_i].uv[vert_i]
          return (name, uv)
        self.uv = map(getMultiUV, mesh.getUVLayerNames())
    else:
      self.uv = None

  def write(self, buffer, padding = ''):
    padding2 = padding+'  '
    coord_str = ' '.join(map(str, self.coords)) # This way it supports arbitrary number of coords, for NURBS
    ln = ['%s<Vertex> %i {'%(padding, self.index),
        '%s%s'%(padding2, coord_str)]
        
    if self.uv:
      if self.doTangent==False:
        for name, uv in self.uv:
          if name=='UVTex': name = ''
          ln.append('%s<UV> %s { %f %f }'%(padding2, eggSafeName(name), uv[0], uv[1]))
      else:
        for name, uv, tangent in self.uv:
          if name=='UVTex': name = ''

          # This code detects and handles bad tangents - prints a warning, with duplicate avoidance, and sets it to a fallback value...
          # (Note that I'm using the fact that these should be normalised and that comparisons with nan always return false - de-morgan does not apply here.)
          problem = reduce(lambda a,b: a or b,map(lambda i: not ((tangent[i]>-1.1) and (tangent[i]<1.1)) ,xrange(3)))

          if not problem:
            if self.normal:
              bin = -CrossVecs(self.normal,tangent)
            else:
              bin = -CrossVecs(self.faceNormal,tangent)
          else:
            # Make tangent a direction that is not a multiple of the normal, use this to select an arbitrary tangent/bi-normal that is at least perpendicular to the normal....
            if self.normal:
              tangent[0] = -self.normal[1]
              tangent[1] = self.normal[2]
              tangent[2] = self.normal[0]
              bin = -CrossVecs(self.normal,tangent)
              bin.normalize()
              tangent = CrossVecs(self.normal,bin)
            else:
              tangent[0] = -self.faceNormal[1]
              tangent[1] = self.faceNormal[2]
              tangent[2] = self.faceNormal[0]
              bin = -CrossVecs(self.faceNormal,tangent)
              bin.normalize()
              tangent = CrossVecs(self.faceNormal,bin)

            # Indicate that we have a problem...
            global TANGENT_PROBLEM
            if not TANGENT_PROBLEM:
              TANGENT_PROBLEM = True
              exporter.messages.append(Message('Bad tangent/binormals detected - exported geometry has either degenerate faces or, more typically, face vertices that share uv coordinates.', Message.Warning))
          
          ln.append('%s<UV> %s {'%(padding2, eggSafeName(name)))
          ln.append('%s  %f %f'%(padding2,uv[0],uv[1]))
          ln.append('%s  <Tangent> { %f %f %f }'%(padding2,tangent[0],tangent[1],tangent[2]))
          ln.append('%s  <Binormal> { %f %f %f }'%(padding2,bin[0],bin[1],bin[2]))
          ln.append('%s}'%(padding2,))
          
    if self.normal:
      if self.shapeKeysDict!=None and SHAPE_KEY_NORMALS:
        ln.append('%s<Normal> { %f %f %f'%(padding2, self.normal[0], self.normal[1], self.normal[2]))
        nx,ny,nz = self.normal[0],self.normal[1],self.normal[2]
        for shapeKeyName,shapeKeyInfo in self.shapeKeysDict.iteritems():
          for info in shapeKeyInfo.vertexInfo:
            index,co,no = info
            if index == self.vindex:
              if not vectorEq(self.normal, no):
                x,y,z = no
                ln.append('%s <DNormal> %s { %f %f %f }'% (padding2, shapeKeyName, x-nx, y-ny, z-nz))
              break
        ln.append('%s}' % padding2)
      else:
        ln.append('%s<Normal> { %f %f %f }'%(padding2, self.normal[0], self.normal[1], self.normal[2]))

    if self.shapeKeysDict!=None:
      bx, by, bz = self.coords.x, self.coords.y, self.coords.z
      for shapeKeyName,shapeKeyInfo in self.shapeKeysDict.iteritems():
        for info in shapeKeyInfo.vertexInfo:
          index,co,no = info
          if index == self.vindex:
            if not vectorEq(self.coords, co):
              x,y,z = co
              ln.append('%s<Dxyz> %s { %f %f %f }'% (padding2, shapeKeyName, x-bx, y-by, z-bz))
            break

    if self.color:
      col = self.color
      col = [col.r, col.g, col.b, col.a]
      col = ' '.join(map(lambda x: str(x/255.0), col))
      ln.append('%s<RGBA> { %s }'%(padding2, col))
      
    ln.append(padding+'}')
    buffer.extend(ln)



class Polygon:
  def __init__(self, face, faceindex, group, hasUV, hasVCol, materials, tangents):
    '''
    Constructor
    @param face: The face on which to base this polygon
    @param group: The group that contains the vertex pool for this face
    @param hasUV: indicates whether the mesh has face UV coordinates
    @param hasVCol: indicates whether the mesh has vertex colors
    @param materials: list of the mesh's materials
    @param tangents: list of results of the mesh.getTangents() function for each uv layer, in the order of mesh.getUVLayerNames().
    '''
    self.matRef = None
    self.texRef = []
    mat = None
    if len(materials) > 0:
      try: mat = MATERIALS[materials[face.mat].name]
      except AttributeError: pass
      except KeyError: pass
      else:
        if not mat.shadeless:
          self.matRef = mat.name # store material reference
          mat.users += 1
        self.texRef.extend(mat.getRef()) # store texture reference
    if not mat or len(mat.textures) is 0: # if we don't have a material or it has no textures, use image textures
      for uvLayer in group.tmesh.getUVLayerNames():
        group.tmesh.activeUVLayer = uvLayer
        if hasUV and face.mode & Mesh.FaceModes.TEX and face.image and face.image.name not in self.texRef:
          # create texture for face image if it doesn't exist
          if face.image.name not in TEXTURES:
            tex = Texture(face.image.name, face.image.filename, uvLayer, mat = mat)
            TEXTURES[face.image.name] = tex
          else:
            tex = TEXTURES[face.image.name]
          tex.users += 1
          self.texRef.append(tex.name)
    self.ref = group.name # store group name for vertex pool reference
    self.bface = (hasUV and face.mode & Mesh.FaceModes.TWOSIDE) or \
      exporter.forceBFace
    
    # If the material has TexFace, set the transparency modes on the face.
    self.alphamode = None
    if hasUV and mat != None and mat.texface:
      # The hasattr is to protect pre-2.49 versions of Blender.
      if hasattr(Mesh.FaceTranspModes, "CLIP") and face.transp == Mesh.FaceTranspModes.CLIP:
        self.alphamode = "BINARY"
      elif face.transp == Mesh.FaceTranspModes.ALPHA and mat.ztransp:
        self.alphamode = "DUAL"
      elif face.transp == Mesh.FaceTranspModes.ALPHA:
        self.alphamode = "ON"
      elif face.transp == Mesh.FaceTranspModes.SOLID:
        self.alphamode = "OFF"
      else:
        exporter.messages.append(Message("TexFace transparency modes ADD and SUB are not yet supported.", Message.Warning))
    
    # If we have flat shading, use polygon normals.
    if face.smooth: self.normal = None
    else: self.normal = face.no

    # See if this face has shape key information, and if so store it...
    if hasattr(group, "shapeKeys"):
      self.shapeKeysDict = group.shapeKeys.retrieveAllShapeKeysInfoForFace(face)
    else:
      self.shapeKeysDict = None

    # Iterate face vertices and create the relevant Vertex objects...
    i = len(group.verts)
    self.indices = range(i, i+len(face.v))
    smooth = face.smooth
    mapping = group.bverts2mverts
    for i in xrange(len(face.v)):
      params = {'vert':face.v[i], 'index':self.indices[i], 'tangents':tangents, 'faceNormal':self.normal, 'shapeKeysDict':self.shapeKeysDict}
      if hasUV:
        params['multiuv'] = (group.tmesh, faceindex, i)
      if hasVCol: # or (mat and mat.vlight):
        params['color'] = face.col[i]
      if smooth:
        params['normal'] = True

      mvert = Vertex(**params)
      group.verts.append(mvert)
      if mapping is not None:
        bvert = mapping.get(face.v[i].index, None)
        if not bvert:
          bvert = []
          mapping[face.v[i].index] = bvert
        bvert.append(self.indices[i])

  def write(self, buffer, padding = ''):
    padding2 = padding+'  '
    ln = [padding+'<Polygon> {']
    
    for tex in self.texRef:
      ln.append('%s<TRef> { %s }'%(padding2, eggSafeName(tex)))
      
    if self.matRef:
      ln.append('%s<MRef> { %s }'%(padding2, eggSafeName(self.matRef)))
      
    if self.bface:
      ln.append('%s<BFace> { 1 }'%(padding2))
      
    if self.normal:
      ln.append('%s<Normal> { %f %f %f'%(padding2, self.normal[0], self.normal[1], self.normal[2]))
      
      if self.shapeKeysDict:
        for shapeKeyName,shapeKeyInfo in self.shapeKeysDict.iteritems():
          no = shapeKeyInfo.faceNormal
          ln.append('%s <DNormal> %s { %f %f %f }'%(padding2,shapeKeyName, no[0]-self.normal[0], no[0]-self.normal[1], no[0]-self.normal[2]))
    
      ln.append('%s}' % padding2)
      
    if self.alphamode:
      ln.append('%s<Scalar> alpha { %s }'%(padding2, self.alphamode))
      
    ln.append('%s<VertexRef> { %s <Ref> { %s } }'%(padding2, ' '.join(map(str, self.indices)), eggSafeName(self.ref)))
    ln.append(padding+'}')
    buffer.extend(ln)



class Joint(Group):
  def __init__(self, bone, mat, animOnly, isSrb = False):
    '''
    Constructor
    @param bone: The bone on which to base this joint
    @param mat: The containing Armature's world transform
    @param animOnly: A flag that indicates whether this bone is being generated solely for exporting animation
    '''
    Group.__init__(self,bone.name)
    self.origName = bone.name # original name with possible spaces, used for looking up pose data
    del self.bverts2mverts
    if not animOnly:
      if not bone.parent:
        self.transform = bone.matrix['ARMATURESPACE'] * mat
      else:
        imat = bone.parent.matrix['ARMATURESPACE'] * mat
        imat.invert()
        self.transform = bone.matrix['ARMATURESPACE'] * mat * imat
      self.weights = {} #dictionary of weights [(weight, poolname):[indices]]

  def __repr__(self, padding = ''):
    ln = [padding+'[Joint %s]'%(self.name)]
    padding += ' '
    ln.extend([c.__repr__(padding) for c in self.children])
    return '\n'.join(ln)

  def write(self, buffer, padding = ''):
    buffer.append('%s<Joint> %s {'%(padding, eggSafeName(self.name)))
    self.writeTransform(buffer, padding)
    for k, v in self.weights.iteritems():
      buffer.append('%s  <VertexRef> {'%padding)
      buffer.append('%s    %s'%(padding, ' '.join(map(str,v))))
      buffer.append('%s    <Scalar> membership { %f }'%(padding, k[0]))
      buffer.append('%s    <Ref> { %s }'%(padding, k[1]))
      buffer.append('%s  }'%padding)
    padding2 = padding + '  '
    for c in self.children:
      c.write(buffer, padding2)
    buffer.append('%s}'%(padding))

  def writeAnim(self, fps, aRange, poses, buffer, padding):
    buffer.append('%s<Table> %s {'%(padding, eggSafeName(self.name)))
    buffer.append('%s  <Xfm$Anim> xform {'%padding)
    buffer.append('%s    <Scalar> fps { %i }'%(padding,fps))
    buffer.append('%s    <Scalar> order { sprht }'%padding)
    buffer.append('%s    <Scalar> contents { ijkprhxyz }'%padding)
    buffer.append('%s    <V> {'%padding)
    mats = poses[self.origName]
    for f in aRange:
      mat = mats[f]
      vals = list(mat.scalePart())
      vals.extend(list(mat.toEuler()))
      vals.extend(list(mat.translationPart()))
      vals = map(str, vals) #convert all to strings
      buffer.append('%s      %s'%(padding, ' '.join(vals)))
    buffer.append('%s    }'%padding)
    buffer.append('%s  }'%padding)
    padding2 = padding + '  '
    for c in self.children:
      c.writeAnim(fps, aRange, poses, buffer, padding2)
    buffer.append('%s}'%(padding))



class NurbsCurve(Group):
  def __init__(self, name, curnurb, obj):
    Group.__init__(self, name)
    knots = curnurb.knotsU
    self.order = len(knots)-curnurb.points
    self.knots = ' '.join(map(str, knots))
    self.indices = ' '.join(map(str, range(curnurb.points)))
    
    class DummyVert(Vertex):
      def __init__(self, nurbpoint, index):
        self.coords = nurbpoint
        self.index = index
        self.uv = None
        self.color = None
        self.normal = None
        self.shapeKeysDict = None

    toWorld = obj.matrix
    self.verts = []
    for i, p in enumerate(curnurb):
      ip = Vector(p[0:4]) * toWorld
      self.verts.append(DummyVert(ip, i))

  def write(self, buffer):
    buffer.append('<Group> %s {'%eggSafeName(self.name))
    self.writeInner(buffer)
    buffer.append('  <NURBSCurve> {')
    buffer.append('    <Order> { %i }'%self.order)
    buffer.append('    <Knots> { %s }'%self.knots)
    buffer.append('    <VertexRef> { %s  <Ref> { %s }}'%(self.indices,eggSafeName(self.name)))
    buffer.append('  }')
    buffer.append('}')



class ShapeKeys:
  """Shape key information for a mesh - only construct if the mesh actually has such information (i.e. mesh.key!=None and len(mesh.key.blocks)!=0)."""
  def __init__(self, mesh, matrix):
    """Builds a dictionary, indexable by vertex number, for the passed in mesh, that consists of the transformed vertices from every shape key relevent to the indexed vertex. Also requires the matrix to transform from object space to world space."""
    self.shapeKeyDict = {}
    bKey = mesh.key
    self.mesh = mesh
    self.basicKey = bKey.blocks[0].data
    lData = len(self.basicKey)

    # Loop shape keys...
    for i in range(1,len(bKey.blocks)):
      #print "Shape Key: %d : %s : length %d : pos %f : vgroup %s" % (i, bKey.blocks[i].name, lData, bKey.blocks[i].pos, bKey.blocks[i].vgroup)
      # Handle vertex groups...
      if bKey.blocks[i].vgroup!="":
        vertices = mesh.getVertsFromGroup(bKey.blocks[i].vgroup)
        vertices = set(vertices)
      else:
        vertices = None

      # Get the name and the list of transformed vertices...
      shapeKeyName = eggSafeName(bKey.blocks[i].name)
      shapeBlockData = bKey.blocks[i].data
      
      # Loop through all vertices to find and store the modified once only...
      for j in range(lData):
        if vertices==None or (j in vertices):
          if not vectorEq(shapeBlockData[j], self.basicKey[j]):
            # Transform the vector to world space...
            pt = Vector(shapeBlockData[j])
            pt.resize4D()
            pt = pt * matrix
            pt.resize3D()

            # Store...
            info = (shapeKeyName, (pt.x, pt.y, pt.z))
            if j in self.shapeKeyDict:
              self.shapeKeyDict[j].append(info)
            else:
              self.shapeKeyDict[j] = [info]

  def getRelatedShapeKeys(self, face):
    """Returns the names of all the shape keys that affect the given face."""
    result = set()
    for i in xrange(len(face.v)):
      index = face.v[i].index
      if index in self.shapeKeyDict:
        infolist = self.shapeKeyDict[index]
        for info in infolist:
          shapeKeyName,xyz = info
          result.add(shapeKeyName)
    return result

  def setVertexForFace(self, shapeKeyName, face):
    """Changes the vertices of the given face to be the vertices of the named shape key."""
    for i in xrange(len(face.v)):
      vertex = face.v[i]
      index = vertex.index
      if index in self.shapeKeyDict:
        infolist = self.shapeKeyDict[index]
        for info in infolist:
          name,xyz = info
          if name == shapeKeyName:
            vertex.co[0] = xyz[0]
            vertex.co[1] = xyz[1]
            vertex.co[2] = xyz[2]
            break

  def backupVertex(self, face):
    """Helper method - given a face returns an object that represents the current state of the vertices associated with the face."""
    backup = set()
    for i in xrange(len(face.v)):
      vertex = face.v[i]
      backup.add((vertex, (vertex.co[0], vertex.co[1], vertex.co[2])))
    return backup
    
  def restoreVertex(self, backup):
    """Helper method - restores the vertices of the given backup."""
    for vertex, xyz in backup:
      vertex.co[0] = xyz[0]
      vertex.co[1] = xyz[1]
      vertex.co[2] = xyz[2]

  def retrieveAllShapeKeysInfoForFace(self, face):
    """Returns a dictionary indexed by shape key name of ShapeKeyInfo objects for the given face, or None if the face is untouched by shape keys."""
    shapeKeyNames = self.getRelatedShapeKeys(face)
    if len(shapeKeyNames) > 0:
      # Make backup...
      backup = self.backupVertex(face)

      # Iterate all relevant shape keys and apply then store the affect...
      result = {}
      for shapeKeyName in shapeKeyNames:
        self.setVertexForFace(shapeKeyName , face)
        if SHAPE_KEY_NORMALS:
          self.mesh.calcNormals()
        result[shapeKeyName] = ShapeKeyInfo(face)
          
        # Restore from the backup...
        self.restoreVertex(backup)
        if SHAPE_KEY_NORMALS:
          self.mesh.calcNormals()

      # Return the result...
      return result
    else:
      return None




class ShapeKeyInfo:
  """The state of a face with a specific shape key applied - its normal and the normals of its vertices along with positions."""
  def __init__(self, face):
    self.faceNormal = (face.no[0],face.no[1],face.no[2])
    self.vertexInfo = []
    for i in xrange(len(face.v)):
      vertex = face.v[i]
      self.vertexInfo.append(
        (vertex.index, (vertex.co[0],vertex.co[1], vertex.co[2]),
        (vertex.no[0],vertex.no[1], vertex.no[2])))



### Runtime entry point
if not INTERFACE_ERROR:
  FORCE_BACKGROUND = os.getenv(KEY)
  if Blender.mode == 'background' or FORCE_BACKGROUND:
    if PATH_ERROR:
      print "There is an error in Chicken's configuration. Please run from GUI to access the configuration script"
    else:
      exporter = Background()
  elif not PATH_ERROR:
    import webbrowser
    exporter = Gui()
  else:
    scr = os.path.join(Blender.Get('datadir'),'chicken/chicken_config.py')
    print 'Configuring chicken, script is', scr
    Blender.Run(scr)
