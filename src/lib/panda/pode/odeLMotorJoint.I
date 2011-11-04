// Filename: odeLMotorJoint.I
// Created by:  joswilso (27Dec06)
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


INLINE void OdeLMotorJoint::
set_num_axes(int num) {
  dJointSetLMotorNumAxes(_id, num);
}

INLINE void OdeLMotorJoint::
set_axis(int anum, int rel, dReal x, dReal y, dReal z) {
  dJointSetLMotorAxis(_id, anum, rel, x, y, z);
}

INLINE void OdeLMotorJoint::
set_axis(int anum, int rel, const LVecBase3f &axis) {
  dJointSetLMotorAxis(_id, anum, rel, axis[0], axis[1], axis[2]);
}

INLINE int OdeLMotorJoint::
get_num_axes() const {
  return dJointGetLMotorNumAxes(_id);
}

INLINE LVecBase3f OdeLMotorJoint::
get_axis(int anum) const {
  dVector3 result;
  dJointGetLMotorAxis(_id, anum, result);
  return LVecBase3f(result[0], result[1], result[2]);
}

INLINE void OdeLMotorJoint::
set_param_lo_stop(int axis, dReal val) {
  nassertv( _id != 0 );
  nassertv( 0 <= axis && axis <= 2 );
  if ( axis == 0 ) {
    dJointSetLMotorParam(_id, dParamLoStop, val);
  } else if ( axis == 1 ) {
    dJointSetLMotorParam(_id, dParamLoStop2, val);
  } else if ( axis == 2 ) {
    dJointSetLMotorParam(_id, dParamLoStop3, val);
  }
}

INLINE void OdeLMotorJoint::
set_param_hi_stop(int axis, dReal val) {
  nassertv( _id != 0 );
  nassertv( 0 <= axis && axis <= 2 );
  if ( axis == 0 ) {
    dJointSetLMotorParam(_id, dParamHiStop, val);
  } else if ( axis == 1 ) {
    dJointSetLMotorParam(_id, dParamHiStop2, val);
  } else if ( axis == 2 ) {
    dJointSetLMotorParam(_id, dParamHiStop3, val);
  }
}

INLINE void OdeLMotorJoint::
set_param_vel(int axis, dReal val) {
  nassertv( _id != 0 );
  nassertv( 0 <= axis && axis <= 2 );
  if ( axis == 0 ) {
    dJointSetLMotorParam(_id, dParamVel, val);
  } else if ( axis == 1 ) {
    dJointSetLMotorParam(_id, dParamVel2, val);
  } else if ( axis == 2 ) {
    dJointSetLMotorParam(_id, dParamVel3, val);
  }
}

INLINE void OdeLMotorJoint::
set_param_f_max(int axis, dReal val) {
  nassertv( _id != 0 );
  nassertv( 0 <= axis && axis <= 2 );
  if ( axis == 0 ) {
    dJointSetLMotorParam(_id, dParamFMax, val);
  } else if ( axis == 1 ) {
    dJointSetLMotorParam(_id, dParamFMax2, val);
  } else if ( axis == 2 ) {
    dJointSetLMotorParam(_id, dParamFMax3, val);
  }
}

INLINE void OdeLMotorJoint::
set_param_fudge_factor(int axis, dReal val) {
  nassertv( _id != 0 );
  nassertv( 0 <= axis && axis <= 2 );
  if ( axis == 0 ) {
    dJointSetLMotorParam(_id, dParamFudgeFactor, val);
  } else if ( axis == 1 ) {
    dJointSetLMotorParam(_id, dParamFudgeFactor2, val);
  } else if ( axis == 2 ) {
    dJointSetLMotorParam(_id, dParamFudgeFactor3, val);
  }
}

INLINE void OdeLMotorJoint::
set_param_bounce(int axis, dReal val) {
  nassertv( _id != 0 );
  nassertv( 0 <= axis && axis <= 2 );
  if ( axis == 0 ) {
    dJointSetLMotorParam(_id, dParamBounce, val);
  } else if ( axis == 1 ) {
    dJointSetLMotorParam(_id, dParamBounce2, val);
  } else if ( axis == 2 ) {
    dJointSetLMotorParam(_id, dParamBounce3, val);
  }
}

INLINE void OdeLMotorJoint::
set_param_CFM(int axis, dReal val) {
  nassertv( _id != 0 );
  nassertv( 0 <= axis && axis <= 2 );
  if ( axis == 0 ) {
    dJointSetLMotorParam(_id, dParamCFM, val);
  } else if ( axis == 1 ) {
    dJointSetLMotorParam(_id, dParamCFM2, val);
  } else if ( axis == 2 ) {
    dJointSetLMotorParam(_id, dParamCFM3, val);
  }
}

INLINE void OdeLMotorJoint::
set_param_stop_ERP(int axis, dReal val) {
  nassertv( _id != 0 );
  nassertv( 0 <= axis && axis <= 2 );
  if ( axis == 0 ) {
    dJointSetLMotorParam(_id, dParamStopERP, val);
  } else if ( axis == 1 ) {
    dJointSetLMotorParam(_id, dParamStopERP2, val);
  } else if ( axis == 2 ) {
    dJointSetLMotorParam(_id, dParamStopERP3, val);
  }
}

INLINE void OdeLMotorJoint::
set_param_stop_CFM(int axis, dReal val) {
  nassertv( _id != 0 );
  nassertv( 0 <= axis && axis <= 2 );
  if ( axis == 0 ) {
    dJointSetLMotorParam(_id, dParamStopCFM, val);
  } else if ( axis == 1 ) {
    dJointSetLMotorParam(_id, dParamStopCFM2, val);
  } else if ( axis == 2 ) {
    dJointSetLMotorParam(_id, dParamStopCFM3, val);
  }
}

INLINE dReal OdeLMotorJoint::
get_param_lo_stop(int axis) const {
  nassertr( _id != 0, 0 );
  nassertr( 0 <= axis && axis <= 2, 0 );
  if ( axis == 0 ) {
    return dJointGetLMotorParam(_id, dParamLoStop);
  } else if ( axis == 1 ) {
    return dJointGetLMotorParam(_id, dParamLoStop2);
  } else if ( axis == 2 ) {
    return dJointGetLMotorParam(_id, dParamLoStop3);
  }
  return 0;
}

INLINE dReal OdeLMotorJoint::
get_param_hi_stop(int axis) const {
  nassertr( _id != 0, 0 );
  nassertr( 0 <= axis && axis <= 2, 0 );
  if ( axis == 0 ) {
    return dJointGetLMotorParam(_id, dParamHiStop);
  } else if ( axis == 1 ) {
    return dJointGetLMotorParam(_id, dParamHiStop2);
  } else if ( axis == 2 ) {
    return dJointGetLMotorParam(_id, dParamHiStop3);
  }
  return 0;
}

INLINE dReal OdeLMotorJoint::
get_param_vel(int axis) const {
  nassertr( _id != 0, 0 );
  nassertr( 0 <= axis && axis <= 2, 0 );
  if ( axis == 0 ) {
    return dJointGetLMotorParam(_id, dParamVel);
  } else if ( axis == 1 ) {
    return dJointGetLMotorParam(_id, dParamVel2);
  } else if ( axis == 2 ) {
    return dJointGetLMotorParam(_id, dParamVel3);
  }
  return 0;
}

INLINE dReal OdeLMotorJoint::
get_param_f_max(int axis) const {
  nassertr( _id != 0, 0 );
  nassertr( 0 <= axis && axis <= 2, 0 );
  if ( axis == 0 ) {
    return dJointGetLMotorParam(_id, dParamFMax);
  } else if ( axis == 1 ) {
    return dJointGetLMotorParam(_id, dParamFMax2);
  } else if ( axis == 2 ) {
    return dJointGetLMotorParam(_id, dParamFMax3);
  }
  return 0;
}

INLINE dReal OdeLMotorJoint::
get_param_fudge_factor(int axis) const {
  nassertr( _id != 0, 0 );
  nassertr( 0 <= axis && axis <= 2, 0 );
  if ( axis == 0 ) {
    return dJointGetLMotorParam(_id, dParamFudgeFactor);
  } else if ( axis == 1 ) {
    return dJointGetLMotorParam(_id, dParamFudgeFactor2);
  } else if ( axis == 2 ) {
    return dJointGetLMotorParam(_id, dParamFudgeFactor3);
  }
  return 0;
}

INLINE dReal OdeLMotorJoint::
get_param_bounce(int axis) const {
  nassertr( _id != 0, 0 );
  nassertr( 0 <= axis && axis <= 2, 0 );
  if ( axis == 0 ) {
    return dJointGetLMotorParam(_id, dParamBounce);
  } else if ( axis == 1 ) {
    return dJointGetLMotorParam(_id, dParamBounce2);
  } else if ( axis == 2 ) {
    return dJointGetLMotorParam(_id, dParamBounce3);
  }
  return 0;
}

INLINE dReal OdeLMotorJoint::
get_param_CFM(int axis) const {
  nassertr( _id != 0, 0 );
  nassertr( 0 <= axis && axis <= 2, 0 );
  if ( axis == 0 ) {
    return dJointGetLMotorParam(_id, dParamCFM);
  } else if ( axis == 1 ) {
    return dJointGetLMotorParam(_id, dParamCFM2);
  } else if ( axis == 2 ) {
    return dJointGetLMotorParam(_id, dParamCFM3);
  }
  return 0;
}

INLINE dReal OdeLMotorJoint::
get_param_stop_ERP(int axis) const {
  nassertr( _id != 0, 0 );
  nassertr( 0 <= axis && axis <= 2, 0 );
  if ( axis == 0 ) {
    return dJointGetLMotorParam(_id, dParamStopERP);
  } else if ( axis == 1 ) {
    return dJointGetLMotorParam(_id, dParamStopERP2);
  } else if ( axis == 2 ) {
    return dJointGetLMotorParam(_id, dParamStopERP3);
  }
  return 0;
}

INLINE dReal OdeLMotorJoint::
get_param_stop_CFM(int axis) const {
  nassertr( _id != 0, 0 );
  nassertr( 0 <= axis && axis <= 2, 0 );
  if ( axis == 0 ) {
    return dJointGetLMotorParam(_id, dParamStopCFM);
  } else if ( axis == 1 ) {
    return dJointGetLMotorParam(_id, dParamStopCFM2);
  } else if ( axis == 2 ) {
    return dJointGetLMotorParam(_id, dParamStopCFM3);
  }
  return 0;
}

