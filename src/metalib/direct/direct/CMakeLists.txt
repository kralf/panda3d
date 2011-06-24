panda3d_interrogate_module(direct MODULE p3direct)

remake_add_library(direct *.cxx LINK dcbase dcparse deadrec distributed
  heapq http interval motiontrail showbase)
remake_add_headers(*.h *.I *.T)
