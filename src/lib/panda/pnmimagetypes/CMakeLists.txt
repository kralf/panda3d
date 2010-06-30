remake_add_library(pnmimagetypes *.cxx
  LINK ${JPEG_LIBRARIES} ${PNG_LIBRARIES} ${TIFF_LIBRARIES})
remake_add_headers(*.h *.I *.T)
