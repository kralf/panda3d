// Filename: subStream.I
// Created by:  drose (02Aug02)
//
////////////////////////////////////////////////////////////////////
//
// PANDA 3D SOFTWARE
// Copyright (c) Carnegie Mellon University.  All rights reserved.
//
// All use of this software is subject to the terms of the revised BSD
// license.  You should have received a copy of this license along
// with this source code in a file named "LICENSE."
//
////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////
//     Function: ISubStream::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE ISubStream::
ISubStream() : istream(&_buf) {
}

////////////////////////////////////////////////////////////////////
//     Function: ISubStream::Constructor
//       Access: Public
//  Description:
////////////////////////////////////////////////////////////////////
INLINE ISubStream::
ISubStream(IStreamWrapper *source, streampos start, streampos end) : istream(&_buf) {
  open(source, start, end);
}

////////////////////////////////////////////////////////////////////
//     Function: ISubStream::open
//       Access: Public
//  Description: Starts the SubStream reading from the indicated
//               source, with the first character being the character
//               at position "start" within the source, for end -
//               start total characters.  The character at "end"
//               within the source will never be read; this will
//               appear to be EOF.
//
//               If end is zero, it indicates that the ISubStream will
//               continue until the end of the source stream.
////////////////////////////////////////////////////////////////////
INLINE ISubStream &ISubStream::
open(IStreamWrapper *source, streampos start, streampos end) {
  clear((ios_iostate)0);
  _buf.open(source, start, end);
  return *this;
}

////////////////////////////////////////////////////////////////////
//     Function: ISubStream::close
//       Access: Public
//  Description: Resets the SubStream to empty, but does not actually
//               close the source istream.
////////////////////////////////////////////////////////////////////
INLINE ISubStream &ISubStream::
close() {
  _buf.close();
  return *this;
}

