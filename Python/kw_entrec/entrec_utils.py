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
import subprocess
from pathlib import Path





class ENTREC_TYPES(enum.IntEnum):

    BASE_ENTITY   = 0xF00
    POINT_CAMERA  = 0xF01
    BASE_SKELETAL = 0xF02


class ENTREC_EVENT(enum.IntEnum):

	ENT_CREATED    = 0xE01
	ENT_BROKEN     = 0xE02
	ENT_DELETED    = 0xE03

	EFFECT_CREATED = 0xE04

	SOUND_CREATED  = 0xE05



class EntRecUtils():

    def __init__(self):
        self.cl_lastInputTick  = 0
        self.cl_lastOutputTick = 0
        self.sv_lastInputTick  = 0
        self.sv_lastOutputTick = 0

        self.first_engine_tick = 0


    def UpdateBaseEntity(self, ent_data, entityObject, tickCount: int):

        vecOrigin  = ent_data.ent_pos['0']
        quatAngles = ent_data.ent_rot['0']

        entityObject.location[0] = HammerUnitToBlenderUnit(vecOrigin.x)
        entityObject.location[1] = HammerUnitToBlenderUnit(vecOrigin.y)
        entityObject.location[2] = HammerUnitToBlenderUnit(vecOrigin.z)

        if entityObject.rotation_mode != 'QUATERNION':
            entityObject.rotation_mode = 'QUATERNION'

        entityObject.rotation_quaternion.w = quatAngles.w
        entityObject.rotation_quaternion.x = quatAngles.x
        entityObject.rotation_quaternion.y = quatAngles.y
        entityObject.rotation_quaternion.z = quatAngles.z

        entityObject.keyframe_insert(data_path="location", frame=tickCount)
        entityObject.keyframe_insert(data_path="rotation_quaternion", frame=tickCount)


    def UpdatePointCamera(self, ent_data, entityObject, tickCount: int):
        
        vecOrigin   = ent_data.ent_pos['0']
        quatAngles  = ent_data.ent_rot['0']
        eulerAngles = mathutils.Euler()

        eulerAngles.x = quatAngles.x
        eulerAngles.y = quatAngles.y
        eulerAngles.z = quatAngles.z

        eulerAngles.x -= 90
        eulerAngles.y -= 90

        eulerAngles.x = math.radians(eulerAngles.x)
        eulerAngles.y = math.radians(eulerAngles.y)
        eulerAngles.z = math.radians(eulerAngles.z)

        eulerAngles.x = -eulerAngles.x
        eulerAngles.y = eulerAngles.z
        eulerAngles.z = eulerAngles.y
        

        entityObject.location[0] = HammerUnitToBlenderUnit(vecOrigin.x)
        entityObject.location[1] = HammerUnitToBlenderUnit(vecOrigin.y)
        entityObject.location[2] = HammerUnitToBlenderUnit(vecOrigin.z)

        if entityObject.rotation_mode != 'XYZ':
            entityObject.rotation_mode = 'XYZ'

        entityObject.rotation_euler.x = eulerAngles.x
        entityObject.rotation_euler.y = eulerAngles.y
        entityObject.rotation_euler.z = eulerAngles.z

        entityObject.keyframe_insert(data_path="rotation_euler", frame=tickCount)
        entityObject.keyframe_insert(data_path="location", frame=tickCount)

        


    def UpdateBaseSkeletal(self, ent_data, entityObject, entBoneList, tickCount: int):

        for name, boneVec in ent_data.ent_pos.items():

            entBone = entBoneList[name]

            bone = entBone.proxy_bone

            bone.location[0] = HammerUnitToBlenderUnit(boneVec.x)
            bone.location[1] = HammerUnitToBlenderUnit(boneVec.y)
            bone.location[2] = HammerUnitToBlenderUnit(boneVec.z)

            bone.keyframe_insert(data_path="location", frame=tickCount)

        for name, boneQuat in ent_data.ent_rot.items():

            entBone = entBoneList[name]

            bone = entBone.proxy_bone

            if bone.rotation_mode != 'QUATERNION':
                bone.rotation_mode = 'QUATERNION'

            bone.rotation_quaternion.w = boneQuat.w
            bone.rotation_quaternion.x = boneQuat.x
            bone.rotation_quaternion.y = boneQuat.y
            bone.rotation_quaternion.z = boneQuat.z

            bone.keyframe_insert(data_path="rotation_quaternion", frame=tickCount)
        











def HammerUnitToBlenderUnit(hammerUnit):
    
    blenderUnit = hammerUnit * bpy.context.scene.entrec_props.scale_factor

    return blenderUnit









    


