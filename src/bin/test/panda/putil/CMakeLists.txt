remake_add_executable(putil_bamRead putil_bam.cxx putil_bam_read.cxx
  LINK panda TESTING)
remake_add_executable(putil_bamWrite putil_bam.cxx putil_bam_write.cxx
  LINK panda TESTING)
remake_add_executables(putil_filename.cxx putil_glob.cxx putil_line_stream.cxx
  putil_unique_id_alloc.cxx LINK panda TESTING)
