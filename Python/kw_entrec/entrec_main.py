#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
# 
#  Purpose: 
# 
#  Product Contributors: Barber
# 
#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\


# This block is for automatically installing PyZMQ if it isnt already installed in Blender's Python interpreter
import subprocess
import sys

def pip_list():
    args = [sys.executable, "-m", "pip", "list"]
    subProc = subprocess.run(args, check=True, capture_output=True)
    return subProc.stdout.decode()

def install_pyzmq():
    args = [sys.executable, "-m", "pip", "install", "pyzmq"]
    subProc = subprocess.run(args, check=True, capture_output=True)



if "pyzmq" not in pip_list():
    print("KleinWorks: PyZMQ not installed, using pip to install PyZMQ...")
    install_pyzmq()




if "bpy" in locals():
    import importlib
    
    importlib.reload(pysource_ipc)
    importlib.reload(entrec_utils)

else:
    from . import pysource_ipc
    from . import entrec_utils
    from . import cpy_entrecbridge

import bpy

if bpy.ops.sourceio != None:
        from . import entrec_sourceIO

import json
import math
import re
import time


CL_OUTPUT_PORTNUM = 5533
CL_INPUT_PORTNUM  = 5551

SV_OUTPUT_PORTNUM = 5577
SV_INPUT_PORTNUM  = 5550


cl_ipc = pysource_ipc.pysrc_ipc.InSourceOutSource()
sv_ipc = pysource_ipc.pysrc_ipc.InSourceOutSource()

entRecUtils  = entrec_utils.EntRecUtils()
entRecBridge = cpy_entrecbridge.PyEntRecBridge()






def EntRecMainLoop():

    enable_data_reception    = bpy.context.scene.entrec_props.enable_data_reception
    enable_data_transferring = bpy.context.scene.entrec_props.enable_data_transferring
    is_recording             = bpy.context.scene.entrec_props.is_recording



    if enable_data_reception       is True:
        if cl_ipc.INPUTFuncLoop is None:
            cl_ipc.ReceiveData()
        if sv_ipc.INPUTFuncLoop is None:
            sv_ipc.ReceiveData()

        if entRecUtils.cl_lastInputTick < cl_ipc.INPUTtickCount:
            if cl_ipc.INPUTtickCount == 1:
                entRecBridge.ClientInitialMetadata(bytes(cl_ipc.receivedMetaDataBuffer, 'UTF-8'))

            entRecBridge.ClientRecv(bytes(cl_ipc.receivedDataBuffer, 'UTF-8'), cl_ipc.INPUTtickCount, cl_ipc.peerENGINEtickCount)

        if entRecUtils.sv_lastInputTick < sv_ipc.INPUTtickCount:
            if sv_ipc.INPUTtickCount == 1:
                entRecBridge.ServerInitialMetadata(bytes(sv_ipc.receivedMetaDataBuffer, 'UTF-8'))

            entRecBridge.ServerRecv(bytes(sv_ipc.receivedDataBuffer, 'UTF-8'), sv_ipc.INPUTtickCount, sv_ipc.peerENGINEtickCount)
        

        if cl_ipc.peerIsDoneTransfering     and sv_ipc.peerIsDoneTransfering or \
           cl_ipc.isReceivingInput == False and sv_ipc.peerIsDoneTransfering or \
           sv_ipc.isReceivingInput == False and cl_ipc.peerIsDoneTransfering:
            
            if cl_ipc.firstENGINEtick <= sv_ipc.firstENGINEtick:
                entRecUtils.first_engine_tick = cl_ipc.firstENGINEtick
            else:
                entRecUtils.first_engine_tick = sv_ipc.firstENGINEtick
            
            print("ParseRawMsgData")
            entRecBridge.ParseRawMsgData()
            print("FilterParsedMessages")
            entRecBridge.FilterParsedMessages()
            
            print("ApplyEntMetadata")
            for entity_metadata in entRecBridge.m_filtered_initial_metadata:
                ApplyEntMetadata(entity_metadata)
            
            print("ApplyEntData")
            ApplyEntData()

            print(f"CL first engine tick:  {sv_ipc.firstENGINEtick}")
            print(f"SV first engine tick: {cl_ipc.firstENGINEtick}")

            print("ClearContents")
            entRecBridge.ClearContents()




    entRecUtils.cl_lastInputTick  = cl_ipc.INPUTtickCount
    entRecUtils.sv_lastInputTick  = sv_ipc.INPUTtickCount


    if enable_data_transferring     is True:
        if cl_ipc.OUTPUTFuncLoop is None:
            cl_ipc.TransferData()
        if sv_ipc.OUTPUTFuncLoop is None:
            sv_ipc.TransferData()


    entRecUtils.cl_lastOutputTick = cl_ipc.OUTPUTtickCount
    entRecUtils.sv_lastOutputTick = sv_ipc.OUTPUTtickCount

    cl_ipc.RunFuncLoop()
    sv_ipc.RunFuncLoop()

    if is_recording == False and cl_ipc.isReceivingInput == False and sv_ipc.isReceivingInput == False:
        entRecUtils.cl_lastOutputTick = 0
        entRecUtils.sv_lastOutputTick = 0

        entRecUtils.cl_lastInputTick  = 0
        entRecUtils.sv_lastInputTick  = 0
        return None
    else:
        return 0.0001
        

    


def ApplyEntMetadata(entity_data):


    receiving_entlist = bpy.context.scene.entrec_props.receiving_entlist
    models_filepath   = bpy.context.scene.entrec_props.models_filepath

    for ent in receiving_entlist:

        if ent.ent_id == entity_data.ent_id:
            return None

    entity = receiving_entlist.add()
    entity.ent_name = entity_data.ent_name
    entity.ent_id   = entity_data.ent_id

        
        
    if entity_data.ent_type == int(entrec_utils.ENTREC_TYPES.BASE_ENTITY):

        entity.ent_type      = "base_entity"
        entity.ent_modelpath = entity_data.ent_model

        # retreives the full path of the folder the MDL file is located in
        model_path = models_filepath + re.sub(r"\\[^\\]*?\.mdl$", "", entity.ent_modelpath)
        print(model_path)

        # retreives the name of the MDL file itself
        model_file = re.sub(r'.*/', "", entity.ent_modelpath)
        print(model_file)


        if bpy.ops.sourceio != None:    
            bpy.ops.entrec.sourceio_mdl(filepath=model_path, files=[{'name':model_file}])
        else:
            bpy.ops.mesh.primitive_cube_add()

        entModel = bpy.context.view_layer.objects.active

        entModel.name = entity.ent_name
                            
        entity.ent_blender_object = entModel

    elif entity_data.ent_type == int(entrec_utils.ENTREC_TYPES.POINT_CAMERA):

        entity.ent_type = "point_camera"

        entCameraData   = bpy.data.cameras.new(name=entity.ent_name)
            
        entCameraObject = bpy.data.objects.new(name=entity.ent_name, object_data=entCameraData)

        bpy.context.view_layer.active_layer_collection.collection.objects.link(entCameraObject)

        entity.ent_blender_object = entCameraObject
        
    elif entity_data.ent_type == int(entrec_utils.ENTREC_TYPES.BASE_SKELETAL):

        entity.ent_type      = "base_skeletal"
        entity.ent_modelpath = entity_data.ent_model

        # retreives the full path of the folder the MDL file is located in
        model_path = models_filepath + re.sub(r"\\[^\\]*?\.mdl$", "", entity.ent_modelpath)
        print(model_path)

        # retreives the name of the MDL file itself
        model_file = re.sub(r'.*/', "", entity.ent_modelpath)
        print(model_file)

        bpy.ops.entrec.sourceio_mdl(filepath=model_path, files=[{'name':model_file}])

        entModel = bpy.context.view_layer.objects.active.find_armature()

        entModel.name = entity.ent_name
                            
        entity.ent_blender_object = entModel

        skelCollection = bpy.data.collections.new(f"{entity.ent_name}")

        skelCollection.objects.link(bpy.context.view_layer.objects.active)
        skelCollection.objects.link(entModel)
        bpy.context.scene.collection.objects.unlink(bpy.context.view_layer.objects.active)
        bpy.context.scene.collection.objects.unlink(entModel)


        boneCollection = bpy.data.collections.new(f"{entity.ent_name} BONES")

        bpy.context.scene.collection.children.link(skelCollection)
        bpy.context.scene.collection.children.link(boneCollection)

        poseBones = entModel.pose.bones

        for bone in poseBones:
            entBone      = entity.ent_bonelist.add()
            entBone.name = bone.name


            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, segments=4, ring_count= 5, align='CURSOR')
            proxyBone = bpy.context.view_layer.objects.active
            bpy.context.scene.collection.objects.unlink(proxyBone)
            proxyBone.name = entBone.name
            entBone.proxy_bone = proxyBone

            rotConstraint = bone.constraints.new("COPY_ROTATION")
            rotConstraint.mix_mode = 'REPLACE'
            rotConstraint.target = proxyBone

            posConstraint = bone.constraints.new("COPY_LOCATION")
            posConstraint.target = proxyBone

            boneCollection.objects.link(proxyBone)

    return None
    






def ApplyEntData():

    receiving_entlist    = bpy.context.scene.entrec_props.receiving_entlist

    for frame in entRecBridge.m_parsed_recording:
        print(frame.frame_num)



        print("for index, ent_data in enumerate(frame.recorded_entdata):")
        for index, ent_data in enumerate(frame.recorded_entdata):

            if len(receiving_entlist) < index:
                print("ApplyEntData: Len is less than index")
                continue
            

            entity = None

            for i in range(len(receiving_entlist)):
                if receiving_entlist[i].ent_id == ent_data.ent_id:
                    entity = receiving_entlist[i]
                    continue
            if entity == None:
                print(f"ApplyEntData: Could not find ent named {ent_data.ent_name}")
                continue

            curFrame = ent_data.engine_tick_count - entRecUtils.first_engine_tick



            if entity.ent_type   == 'base_entity':
                entRecUtils.UpdateBaseEntity(ent_data,   entity.ent_blender_object, curFrame)

            elif entity.ent_type == 'point_camera':
                entRecUtils.UpdatePointCamera(ent_data,  entity.ent_blender_object, curFrame)

            elif entity.ent_type == 'base_skeletal':
                entRecUtils.UpdateBaseSkeletal(ent_data, entity.ent_blender_object, entity.ent_bonelist, curFrame)

        print("for event in frame.recorded_events:")
        for event in frame.recorded_events:
            print(f"processing event of type {event.event_type}...")

            curFrame = event.tick_count - entRecUtils.first_engine_tick

            if event.event_type == entrec_utils.ENTREC_EVENT.ENT_CREATED:
                ApplyEntMetadata(event.ent_metadata)

            if event.event_type == entrec_utils.ENTREC_EVENT.ENT_BROKEN:
                pass

            if event.event_type == entrec_utils.ENTREC_EVENT.ENT_DELETED:
                for ent in receiving_entlist:
                    if event.ent_id == ent.ent_id:
                        entObject = ent.ent_blender_object

                        entObject.hide_render   = False
                        entObject.hide_viewport = False

                        entObject.keyframe_insert(data_path="hide_render", frame=curFrame - 1)
                        entObject.keyframe_insert(data_path="hide_viewport", frame=curFrame - 1)

                        entObject.hide_render   = True
                        entObject.hide_viewport = True

                        entObject.keyframe_insert(data_path="hide_render", frame=curFrame)
                        entObject.keyframe_insert(data_path="hide_viewport", frame=curFrame)

                        
            
            if event.event_type == int(entrec_utils.ENTREC_EVENT.SOUND_CREATED):
                vec = event.sound_origin['0']

                speakerPosition = (entrec_utils.HammerUnitToBlenderUnit(vec.x),
                                   entrec_utils.HammerUnitToBlenderUnit(vec.y),
                                   entrec_utils.HammerUnitToBlenderUnit(vec.z))
                
                bpy.ops.object.speaker_add(location=speakerPosition)

                soundEmitter             = bpy.context.view_layer.objects.active
                soundEmitter.name        = re.sub(r'.*/', "", event.sound_name) + f"_{event.ent_id}"

                sounds_folder = bpy.context.scene.entrec_props.models_filepath + "sound\\"

                sound_path  = sounds_folder + event.sound_name.replace("/", "\\")

                bpy.ops.sound.open_mono(filepath=sound_path, relative_path=False)

                soundEmitter.data.sound  = bpy.data.sounds[re.sub(r'.*/', "", event.sound_name)]
                
                soundEmitter.animation_data.nla_tracks[0].strips[0].frame_start = curFrame
                soundEmitter.animation_data.nla_tracks[0].strips[0].frame_end   = curFrame + 10

                soundEmitter.data.muted = True
                soundEmitter.data.muted = False




    return None


