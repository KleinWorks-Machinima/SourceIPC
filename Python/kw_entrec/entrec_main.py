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


import bpy

if bpy.ops.sourceio != None:
        from . import entrec_sourceIO

import json
import math
import re



entRecIPC = pysource_ipc.pysrc_ipc.InSourceOutSource("tcp://*:5556", "tcp://localhost:5555")
entRecIPC.dropOutTolerance = 15

entRecUtils = entrec_utils.EntRecUtils()






def EntRecMainLoop():

    enable_data_reception    = bpy.context.scene.entrec_props.enable_data_reception
    enable_data_transferring = bpy.context.scene.entrec_props.enable_data_transferring
    is_recording             = bpy.context.scene.entrec_props.is_recording

   

    if enable_data_reception       is True:
        if entRecIPC.INPUTFuncLoop is None:
            entRecIPC.ReceiveData()
        
        EntRecReceiveData(entRecUtils.lastInputTick)

    entRecUtils.lastInputTick  = entRecIPC.INPUTtickCount


    if enable_data_transferring     is True:
        if entRecIPC.OUTPUTFuncLoop is None:
            entRecIPC.TransferData()
        
        EntRecTransferData(entRecUtils.lastOutputTick)

    entRecUtils.lastOutputTick = entRecIPC.OUTPUTtickCount

    entRecIPC.RunFuncLoop()

    if is_recording == False and entRecIPC.isReceivingInput == False:
        entRecUtils.lastOutputTick = 0
        entRecUtils.lastInputTick  = 0
        return None
    else:
        return 0.0001






def EntRecReceiveData(lastInputTick: int):

    if lastInputTick != entRecIPC.INPUTtickCount:
        if entRecIPC.INPUTtickCount == 1:

            EntRecUpdateEntList()

        EntRecUpdateEntities()

    






def EntRecTransferData(lastOutputTick: int):
    if lastOutputTick != entRecIPC.OUTPUTtickCount:
        pass
        

    


def EntRecUpdateEntList():

    receiving_entlist = bpy.context.scene.entrec_props.receiving_entlist
    models_filepath   = bpy.context.scene.entrec_props.models_filepath
    

    receivedMetadata = json.loads(entRecIPC.receivedMetaDataBuffer)


    for index, entity_js in enumerate(receivedMetadata["EntList"]):        

        if index < len(receiving_entlist):

            if receiving_entlist[index].ent_name == entity_js['ent_name']:
                continue


        entity = receiving_entlist.add()

        entity.ent_name = entity_js['ent_name']
        
        if entity_js['ent_type'] == int(entrec_utils.ENTREC_TYPES.BASE_ENTITY):

            entity.ent_type      = "base_entity"
            entity.ent_modelpath = entity_js['ent_modelpath']

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

        elif entity_js['ent_type'] == int(entrec_utils.ENTREC_TYPES.POINT_CAMERA):

            entity.ent_type = "point_camera"

            entCameraData   = bpy.data.cameras.new(name=entity.ent_name)
            
            entCameraObject = bpy.data.objects.new(name=entity.ent_name, object_data=entCameraData)

            bpy.context.view_layer.active_layer_collection.collection.objects.link(entCameraObject)

            entity.ent_blender_object = entCameraObject
        
        elif entity_js['ent_type'] == int(entrec_utils.ENTREC_TYPES.BASE_SKELETAL):

            entity.ent_type      = "base_skeletal"
            entity.ent_modelpath = entity_js['ent_modelpath']

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

            for index, bone_js in enumerate(entity_js['bonedata']):
                entBone  = entity.ent_bonelist.add()
                entBone.name = bone_js['name']
                poseBone = poseBones[entBone.name]


                bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, segments=4, ring_count= 5, align='CURSOR')
                proxyBone = bpy.context.view_layer.objects.active
                bpy.context.scene.collection.objects.unlink(proxyBone)
                proxyBone.name = entBone.name
                entBone.proxy_bone = proxyBone

                rotConstraint = poseBone.constraints.new("COPY_ROTATION")
                rotConstraint.mix_mode = 'REPLACE'
                rotConstraint.target = proxyBone

                posConstraint = poseBone.constraints.new("COPY_LOCATION")
                posConstraint.target = proxyBone

                boneCollection.objects.link(proxyBone)

    return None





def EntRecUpdateEntities():

    receiving_entlist    = bpy.context.scene.entrec_props.receiving_entlist

    receivedData = json.loads(entRecIPC.receivedDataBuffer)

    curTickCount = entRecIPC.INPUTtickCount

    for index, entity_js in enumerate(receivedData["EntList"]):

        if len(receiving_entlist) < index:
            continue

        if receiving_entlist[index].ent_name != entity_js['ent_name']:
            continue

        entity = receiving_entlist[index]


        if entity.ent_type   == 'base_entity':
            entRecUtils.UpdateBaseEntity(entity_js,   entity.ent_blender_object, curTickCount)

        elif entity.ent_type == 'point_camera':
            entRecUtils.UpdatePointCamera(entity_js,  entity.ent_blender_object, curTickCount)

        elif entity.ent_type == 'base_skeletal':
            entRecUtils.UpdateBaseSkeletal(entity_js, entity.ent_blender_object, entity.ent_bonelist, curTickCount)

    return None


