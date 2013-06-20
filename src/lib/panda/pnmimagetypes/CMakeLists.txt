remake_add_library(pnmimagetypes *.cxx
  LINK ${JPEG_LIBRARY} ${PNG_LIBRARY} ${TIFF_LIBRARY})
remake_add_headers(*.h *.I *.T)
