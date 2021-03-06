// Filename: identityStream.cxx
// Created by:  drose (09Oct02)
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

#include "identityStream.h"

// This module is not compiled if OpenSSL is not available.
#ifdef HAVE_OPENSSL

#include "httpChannel.h"

////////////////////////////////////////////////////////////////////
//     Function: IIdentityStream::Destructor
//       Access: Published, Virtual
//  Description: 
////////////////////////////////////////////////////////////////////
IIdentityStream::
~IIdentityStream() {
  if (_channel != (HTTPChannel *)NULL) {
    _channel->body_stream_destructs(this);
    _channel = NULL;
  }
}

////////////////////////////////////////////////////////////////////
//     Function: IIdentityStream::is_closed
//       Access: Public, Virtual
//  Description: Returns true if the last eof condition was triggered
//               because the socket has genuinely closed, or false if
//               we can expect more data to come along shortly.
////////////////////////////////////////////////////////////////////
bool IIdentityStream::
is_closed() {
  if ((_buf._has_content_length && _buf._bytes_remaining == 0) || 
      _buf.is_closed()) {
    return true;
  }
  clear();
  return false;
}

////////////////////////////////////////////////////////////////////
//     Function: IIdentityStream::close
//       Access: Public, Virtual
//  Description: Resets the IdentityStream to empty, but does not actually
//               close the source BIO unless owns_source was true.
////////////////////////////////////////////////////////////////////
void IIdentityStream::
close() {
  _buf.close_read();
}

////////////////////////////////////////////////////////////////////
//     Function: IIdentityStream::get_read_state
//       Access: Public, Virtual
//  Description: Returns an enum indicating how we are coming along in
//               reading the document.
////////////////////////////////////////////////////////////////////
INLINE IIdentityStream::ReadState IIdentityStream::
get_read_state() {
  return _buf.get_read_state();
}

#endif  // HAVE_OPENSSL
