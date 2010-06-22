remake_add_executable(util_bamRead util_bam.cxx util_bamRead.cxx
  LINK util TESTING)
remake_add_executable(util_bamWrite util_bam.cxx util_bamWrite.cxx
  LINK util TESTING)
remake_add_executables(util_filename.cxx util_glob.cxx util_linestream.cxx
  util_uiqueIdAllocator.cxx LINK  util TESTING)
