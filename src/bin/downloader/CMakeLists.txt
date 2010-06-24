remake_include(
  ../../lib/dtool/*
  ../../lib/panda/*
  ../../lib/downloader
)

remake_add_executables(*.cxx LINK downloader TESTING)
