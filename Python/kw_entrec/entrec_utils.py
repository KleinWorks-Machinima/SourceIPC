#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
# 
#  Purpose: 
# 
#  Product Contributors: Barber
# 
#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\



import bpy
import mathutils
import enum
import math
import numpy
from pathlib import Path





class ENTREC_TYPES(enum.IntEnum):

    BASE_ENTITY   = 0xF00
    POINT_CAMERA  = 0xF01
    BASE_SKELETAL = 0xF02



class EntRecUtils():

    def __init__(self):
        self.lastInputTick  = 0
        self.lastOutputTick = 0


    def UpdateBaseEntity(self, entity_js, entityObject, tickCount: int):
        
        VEC_ORIGIN    = entity_js['VEC_ORIGIN']
        QANGLE_ANGLES = entity_js['QANGLE_ANGLES']
    
        VEC_ORIGIN    = str.strip(VEC_ORIGIN, '()').split(',')
        QANGLE_ANGLES = str.strip(QANGLE_ANGLES, '()').split(',')
    
        VEC_ORIGIN    = (float(VEC_ORIGIN[0]), float(VEC_ORIGIN[1]), float(VEC_ORIGIN[2]))
        QANGLE_ANGLES = (float(QANGLE_ANGLES[0]), float(QANGLE_ANGLES[1]), float(QANGLE_ANGLES[2]), float(QANGLE_ANGLES[3]))


        entityObject.keyframe_insert(data_path="location", frame=tickCount)

        entityObject.location[0] = HammerUnitToBlenderUnit(VEC_ORIGIN[0])
        entityObject.location[1] = HammerUnitToBlenderUnit(VEC_ORIGIN[1])
        entityObject.location[2] = HammerUnitToBlenderUnit(VEC_ORIGIN[2])

        entityObject.keyframe_insert(data_path="rotation_quaternion", frame=tickCount)

        if entityObject.rotation_mode != 'QUATERNION':
            entityObject.rotation_mode = 'QUATERNION'

        entityObject.rotation_quaternion.w = QANGLE_ANGLES[0]
        entityObject.rotation_quaternion.x = QANGLE_ANGLES[1]
        entityObject.rotation_quaternion.y = QANGLE_ANGLES[2]
        entityObject.rotation_quaternion.z = QANGLE_ANGLES[3]


    def UpdatePointCamera(self, entity_js, entityObject, tickCount: int):
        
        VEC_ORIGIN    = entity_js['VEC_ORIGIN']
        QANGLE_ANGLES = entity_js['QANGLE_ANGLES']
    
        VEC_ORIGIN    = str.strip(VEC_ORIGIN, '()').split(',')
        QANGLE_ANGLES = str.strip(QANGLE_ANGLES, '()').split(',')
    
        VEC_ORIGIN    = (float(VEC_ORIGIN[0]), float(VEC_ORIGIN[1]), float(VEC_ORIGIN[2]))
        x, y, z = (float(QANGLE_ANGLES[0]), float(QANGLE_ANGLES[1]), float(QANGLE_ANGLES[2]))

        x -= 90
        y -= 90

        x = math.radians(x)
        y = math.radians(y)
        z = math.radians(z)

        QANGLE_ANGLES = -x, z, y
        

        entityObject.keyframe_insert(data_path="location", frame=tickCount)

        entityObject.location[0] = HammerUnitToBlenderUnit(VEC_ORIGIN[0])
        entityObject.location[1] = HammerUnitToBlenderUnit(VEC_ORIGIN[1])
        entityObject.location[2] = HammerUnitToBlenderUnit(VEC_ORIGIN[2])

        entityObject.keyframe_insert(data_path="rotation_euler", frame=tickCount)

        if entityObject.rotation_mode != 'XYZ':
            entityObject.rotation_mode = 'XYZ'

        entityObject.rotation_euler.x = QANGLE_ANGLES[0]
        entityObject.rotation_euler.y = QANGLE_ANGLES[1]
        entityObject.rotation_euler.z = QANGLE_ANGLES[2]

        


    def UpdateBaseSkeletal(self, entity_js, entityObject, entBoneList, tickCount: int):

        for index, bone_js in enumerate(entity_js['bonedata']):
            entBone = entBoneList[index]
            print(f"bone #[{index}]: {entBone.name}")

            bone = entBone.proxy_bone


            BONE_POS = bone_js['POS']
            BONE_ROT = bone_js['ROT']

            BONE_POS = str.strip(BONE_POS, '()').split(',')
            BONE_ROT = str.strip(BONE_ROT, '()').split(',')

            BONE_POS = (float(BONE_POS[0]), float(BONE_POS[1]), float(BONE_POS[2]))
            BONE_ROT = (float(BONE_ROT[0]), float(BONE_ROT[1]), float(BONE_ROT[2]), float(BONE_ROT[3]))

            bone.keyframe_insert(data_path="location", frame=tickCount)

            bone.location[0] = HammerUnitToBlenderUnit(BONE_POS[0])
            bone.location[1] = HammerUnitToBlenderUnit(BONE_POS[1])
            bone.location[2] = HammerUnitToBlenderUnit(BONE_POS[2])

            bone.keyframe_insert(data_path="rotation_quaternion", frame=tickCount)

            if bone.rotation_mode != 'QUATERNION':
                bone.rotation_mode = 'QUATERNION'

            bone.rotation_quaternion.w = BONE_ROT[0]
            bone.rotation_quaternion.x = BONE_ROT[1]
            bone.rotation_quaternion.y = BONE_ROT[2]
            bone.rotation_quaternion.z = BONE_ROT[3]
























"""
def EntRecUpdateBaseEntity(entity_js, entityObject, tickCount: int, receivedFrames: dict, parsedFrames: dict):

    VEC_ORIGIN, QANGLE_ANGLES = ParseSourceVectors(entity_js, receivedFrames, parsedFrames, tickCount)

    entityObject.keyframe_insert(data_path="location", frame=tickCount)

    entityObject.location[0] = HammerUnitToBlenderUnit(VEC_ORIGIN[0])
    entityObject.location[1] = HammerUnitToBlenderUnit(VEC_ORIGIN[1])
    entityObject.location[2] = HammerUnitToBlenderUnit(VEC_ORIGIN[2])

    entityObject.keyframe_insert(data_path="rotation_euler", frame=tickCount)

    entityObject.rotation_euler.x = QANGLE_ANGLES[0]
    entityObject.rotation_euler.y = QANGLE_ANGLES[1]
    entityObject.rotation_euler.z = QANGLE_ANGLES[2]




def EntRecUpdatePointCamera(entity_js, entityObject, tickCount: int, receivedFrames: dict, parsedFrames: dict):

    CAM_POS, CAM_ANG = ParseSourceVectors(entity_js, receivedFrames, parsedFrames, tickCount)

    entityObject.keyframe_insert(data_path="location", frame=tickCount)

    entityObject.location[0] = HammerUnitToBlenderUnit(CAM_POS[0])
    entityObject.location[1] = HammerUnitToBlenderUnit(CAM_POS[1])
    entityObject.location[2] = HammerUnitToBlenderUnit(CAM_POS[2])

    entityObject.keyframe_insert(data_path="rotation_euler", frame=tickCount)

    entityObject.rotation_euler.x = CAM_ANG[0]
    entityObject.rotation_euler.y = CAM_ANG[1]
    entityObject.rotation_euler.z = CAM_ANG[2]




def EntRecUpdateBaseSkeletal(entity_js, entityObject, tickCount: int, receivedFrames: dict, parsedFrames: dict):
    pass
"""







def HammerUnitToBlenderUnit(hammerUnit):
    
    blenderUnit = hammerUnit * 0.05245901639

    return blenderUnit









    


