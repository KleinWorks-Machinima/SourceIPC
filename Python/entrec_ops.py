#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
# 
#  Purpose: 
# 
#  Product Contributors: Barber
# 
#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\

if "bpy" in locals():
    import importlib
    
    importlib.reload(entrec_main)
else:
    from . import entrec_main


import bpy
import threading




class StartRecordingOperator(bpy.types.Operator):
    bl_idname = "entrec.startrecording"
    bl_label  = "Start Recording"

    

    @classmethod
    def poll(cls, context):
        return context.scene.entrec_props.is_recording is False


    def execute(self, context):
        timers = bpy.app.timers

        timers.register(function=entrec_main.EntRecMainLoop)

        context.scene.entrec_props.is_recording = True


        return {'FINISHED'}
    



class StopRecordingOperator(bpy.types.Operator):
    bl_idname = "entrec.stoprecording"
    bl_label  = "Stop Recording"

    @classmethod
    def poll(cls, context):
        return context.scene.entrec_props.is_recording is True


    def execute(self, context):

        context.scene.entrec_props.is_recording = False

        return {'FINISHED'}








class ResetSockets(bpy.types.Operator):
    bl_idname = "entrec.resetsockets"
    bl_label  = "Reset Sockets"


    @classmethod
    def poll(cls, context):
        return context.scene.entrec_props.is_recording is False


    def execute(self, context):

        

        return {'FINISHED'}








# copy paste gaming

class DeleteSelectedReceivingEntityOperator(bpy.types.Operator):
    bl_idname = "entrec.delete_selected_entity_receiving"
    bl_label  = "Delete Selected Entity"


    

    def execute(self, context):

        entlist       = bpy.context.scene.entrec_props.receiving_entlist
        entlist_index = bpy.context.scene.entrec_props.receiving_entlist_index

        entlist.remove(entlist_index)


        return {'FINISHED'}
    



class DeleteSelectedTransferringEntityOperator(bpy.types.Operator):
    bl_idname = "entrec.delete_selected_entity_transferring"
    bl_label  = "Delete Selected Entity"


    

    def execute(self, context):

        entlist       = bpy.context.scene.entrec_props.transferring_entlist
        entlist_index = bpy.context.scene.entrec_props.transferring_entlist_index

        entlist.remove(entlist_index)


        return {'FINISHED'}
    
