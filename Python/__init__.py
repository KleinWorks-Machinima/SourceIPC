


bl_info = {
    "name": "EntRec",
    "blender": (3, 80, 0),
    "category": "Object",
}



if "bpy" in locals():
    import importlib
    importlib.reload(entrec_main)
    importlib.reload(entrec_props)
    importlib.reload(entrec_ops)
    importlib.reload(entrec_ui)

else:
    from source_ipc import entrec_main
    from source_ipc import entrec_props
    from source_ipc import entrec_ops
    from source_ipc import entrec_ui

import bpy

if bpy.ops.sourceio != None:
        from . import entrec_sourceIO


class EntRecInit(bpy.types.Operator):
    """Registers all EntRec related operators/panels/props."""
    bl_idname = "entrec.init"
    bl_label = "Initialize EntRec"
 
    @classmethod
    def poll(cls, context):
        return True
 
    def execute(self, context):
        if bpy.ops.sourceio != None:
            bpy.utils.register_class(entrec_sourceIO.ENTREC_OT_MDLImport)

        bpy.utils.register_class(entrec_props.EntRecEntity)
        bpy.utils.register_class(entrec_props.EntRecProperties)

        bpy.types.Scene.entrec_props = bpy.props.PointerProperty(type=entrec_props.EntRecProperties)

        bpy.utils.register_class(entrec_props.ENTREC_UL_receiving_entlist)
        bpy.utils.register_class(entrec_props.ENTREC_UL_transferring_entlist)

        bpy.utils.register_class(entrec_ops.StartRecordingOperator)
        bpy.utils.register_class(entrec_ops.StopRecordingOperator)

        bpy.utils.register_class(entrec_ops.DeleteSelectedReceivingEntityOperator)
        bpy.utils.register_class(entrec_ops.DeleteSelectedTransferringEntityOperator)

        bpy.utils.register_class(entrec_ui.EntRecControlPanel)

        bpy.utils.register_class(entrec_ui.ReceivingDataSettingsSubpanel)
        bpy.utils.register_class(entrec_ui.TransferDataSettingsSubpanel)

        bpy.utils.unregister_class(EntRecInit)

        return {'FINISHED'}




def register():
    bpy.utils.register_class(EntRecInit)




def unregister():
    if bpy.ops.sourceio != None:
            bpy.utils.unregister_class(entrec_sourceIO.ENTREC_OT_MDLImport)

    bpy.utils.unregister_class(entrec_props.EntRecEntity)
    bpy.utils.unregister_class(entrec_props.EntRecProperties)

    bpy.utils.unregister_class(entrec_props.ENTREC_UL_receiving_entlist)
    bpy.utils.unregister_class(entrec_props.ENTREC_UL_transferring_entlist)

    bpy.utils.unregister_class(entrec_ops.StartRecordingOperator)
    bpy.utils.unregister_class(entrec_ops.StopRecordingOperator)

    bpy.utils.unregister_class(entrec_ops.DeleteSelectedReceivingEntityOperator)
    bpy.utils.unregister_class(entrec_ops.DeleteSelectedTransferringEntityOperator)

    bpy.utils.unregister_class(entrec_ui.EntRecControlPanel)

    bpy.utils.unregister_class(entrec_ui.ReceivingDataSettingsSubpanel)
    bpy.utils.unregister_class(entrec_ui.TransferDataSettingsSubpanel)

    bpy.utils.register_class(EntRecInit)



if __name__ == "__main__":
    unregister()

