from contracts import contract
from geometry import SE3_from_rotation_translation, rotation_from_quaternion
import numpy as np
import warnings


__all__ = ['rotation_from_ROS_quaternion', 'pose_from_ROS_transform', 'pose_from_ROS_pose']


@contract(returns='SO3')
def rotation_from_ROS_quaternion(r):
    x, y, z, w = r.x, r.y, r.z, r.w
    # my convention: w + ix + ...
    q = np.array([w, x, y, z])
    return rotation_from_quaternion(q)


@contract(returns='SE3')
def pose_from_ROS_transform(transform):
    tx = transform.translation.x
    ty = transform.translation.y
    tz = transform.translation.z
    R = rotation_from_ROS_quaternion(transform.rotation)
    t = np.array([tx, ty, tz])
    pose = SE3_from_rotation_translation(R, t)
    return pose


@contract(returns='SE3')
def pose_from_ROS_pose(pose):
    warnings.warn('untested function pose_from_ROS_pose()')
    tx = pose.position.x
    ty = pose.position.y
    tz = pose.position.z
    R = rotation_from_ROS_quaternion(pose.orientation)
    t = np.array([tx, ty, tz])
    pose = SE3_from_rotation_translation(R, t)
    return pose


def pose_diffentiate():
    pass
# logmap
    