#!/usr/bin/python3
import sys
import math
import numpy as np

height = 95
l_2 = 200
l_3 = 200
r_offset = 27.5
z_offset = 124.

def Radius_ang(angle_2, angle_3):
    return (l_2 * math.cos(math.radians(angle_2)) - l_3*math.cos(math.radians(angle_2 + angle_3)) + r_offset)
    
def pdevRadius_ang2(angle_2, angle_3):
    return ( - l_2 * math.cos(math.radians(angle_2)) + l_3 * math.cos(math.radians(angle_2 + angle_3)))

def pdevRadius_ang3(angle_2, angle_3):
    return (l_3 * math.sin(math.radians(angle_2 + angle_3)))

class GahakuKinematics:
    def coordinatesFromAngles(self, bodyAngle, shoulderAngle, elbowAngle, handAngle):
        radius = Radius_ang(shoulderAngle, elbowAngle)
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

    def check_for_limits_is_valid(self, bodyAngle, shoulderAngle, elbowAngle):
        ret = True
        if (0 > shoulderAngle > 103):
            print('Shoulder angle out of range')
            ret = False

        if (25 > elbowAngle > 215):
            print('Elbow angle out of range')
            ret = False
        return ret

    def Jacobian_matrix(self, bodyAngle, shoulderAngle, elbowAngle):
        jacobian_matrix = np.zeros((3,3), dtype=float)
        
        radius = Radius_ang(shoulderAngle, elbowAngle)
        dr_dAng2 = pdevRadius_ang2(shoulderAngle, elbowAngle)
        dr_dAng3 = pdevRadius_ang3(shoulderAngle, elbowAngle)

        jacobian_matrix[0, 0] = - radius * math.sin(math.radians(bodyAngle))
        jacobian_matrix[0, 1] = dr_dAng2 * math.cos(math.radians(bodyAngle))
        jacobian_matrix[0, 2] = dr_dAng3 * math.cos(math.radians(bodyAngle))

        jacobian_matrix[1, 0] = radius * math.cos(math.radians(bodyAngle))
        jacobian_matrix[1, 1] = dr_dAng2 * math.sin(math.radians(bodyAngle))
        jacobian_matrix[1, 2] = dr_dAng3 * math.sin(math.radians(bodyAngle))
        
        jacobian_matrix[2, 1] = l_2 * math.cos(math.radians(shoulderAngle)) - l_3 * math.cos(math.radians(shoulderAngle + elbowAngle)) 
        jacobian_matrix[2, 2] = -l_3 * math.cos(math.radians(shoulderAngle + elbowAngle))

        return jacobian_matrix
