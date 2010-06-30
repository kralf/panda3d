remake_add_executable(putil_bamRead putil_bam.cxx putil_bamRead.cxx
  LINK putil TESTING)
remake_add_executable(putil_bamWrite putil_bam.cxx putil_bamWrite.cxx
  LINK putil TESTING)
remake_add_executables(putil_filename.cxx putil_glob.cxx putil_linestream.cxx
  putil_uiqueIdAllocator.cxx LINK putil TESTING)
