#!/usr/bin/python3
import sys
import math

height = 95
l_2 = 200
l_3 = 200
r_offset = 27.5
z_offset = 124.

class GahakuKinematics:
    def __init__(self, debug=False):
        self._debugOn = debug

    def _debug(self, *args):
        if self._debugOn:
            for arg in args:
                sys.stdout.write(str(arg))
                sys.stdout.write(' ')
            print('')

    def coordinatesFromAngles(self, bodyAngle, shoulderAngle, elbowAngle, handAngle):
        radius = l_2*math.cos(math.radians(shoulderAngle)) - l_3*math.cos(math.radians(shoulderAngle + elbowAngle)) + r_offset
        x = radius*math.cos(math.radians(bodyAngle))
        y = radius*math.sin(math.radians(bodyAngle))
        z = height + l_2*math.sin(math.radians(shoulderAngle)) - l_3*math.sin(math.radians(shoulderAngle + elbowAngle)) - z_offset

        return (x, y, z)

    def InverceKinematics(self, x, y, z):
        radius = math.sqrt(pow(x,2) + pow(y,2)) - r_offset
        act_z = z + z_offset - height
        l_4 = math.sqrt(pow(radius,2) + pow(act_z,2)) 
        k = math.sqrt(pow(pow(l_2,2) + pow(l_3,2) + pow(l_4,2), 2) - 2*(pow(l_2,4) + pow(l_3,4) + pow(l_4,4)))
     
        bodyAngle = math.degrees(math.atan2(y, x)) 
        shoulderAngle = math.degrees(math.atan2(act_z, radius) + math.atan2(k, pow(l_2,2) + pow(l_4,2) - pow(l_3,2)))
        elbowAngle = math.degrees(math.atan2(k, pow(l_2,2) + pow(l_3,2) - pow(l_4,2)))
        handAngle = 270 - shoulderAngle - elbowAngle

        return (bodyAngle, shoulderAngle, elbowAngle, handAngle)

    def get_distance_from_origin_cartesian_point_3D(self, x, y, z):
        distanceToEndPoint = math.sqrt(pow(x,2) + pow(y,2) + pow(z,2))
        return distanceToEndPoint

    def check_for_limits_is_valid(self, bodyAngle, shoulderAngle, elbowAngle):
        ret = True
        if (0 > shoulderAngle > 103):
            print('Shoulder angle out of range')
            ret = False

        if (25 > elbowAngle > 215):
            print('Elbow angle out of range')
            ret = False

        return ret
