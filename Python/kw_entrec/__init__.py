bl_info = {
    "name": "EntRec",
    "description": "Implementation of KleinWorks: Machinima's Entity Recording feature into Blender.",
    "blender": (3, 40, 0),
    "version": (0, 1),
    "location": "View3D > UI",
    "warning": "REQUIRES the latest version of SourceIO to be INSTALLED and ENABLED to function correctly.",
    "category": "Animation",
}



if "bpy" in locals():
    import importlib
    importlib.reload(entrec_main)
    importlib.reload(entrec_props)
    importlib.reload(entrec_ops)
    importlib.reload(entrec_ui)

else:
    from . import entrec_main, entrec_props, entrec_ops, entrec_ui

import bpy

    


classes = ()

if bpy.ops.sourceio != None:
        from . import entrec_sourceIO
        classes += entrec_sourceIO.classes

classes += entrec_props.classes
classes += entrec_ops.classes
classes += entrec_ui.classes





def register():
    entrec_main.cl_ipc.ConnectSockets(entrec_main.CL_OUTPUT_PORTNUM, entrec_main.CL_INPUT_PORTNUM)
    entrec_main.sv_ipc.ConnectSockets(entrec_main.SV_OUTPUT_PORTNUM, entrec_main.SV_INPUT_PORTNUM)


    for cls in classes:
        bpy.utils.register_class(cls)

    """
    if bpy.ops.sourceio != None:
        from . import entrec_sourceIO
        for cls in entrec_sourceIO.classes:
             bpy.utils.register_class(cls)

    for cls in entrec_props.classes:
        bpy.utils.register_class(cls)

    for cls in entrec_ui.classes:
        bpy.utils.register_class(cls)

    for cls in entrec_ops.classes:
        bpy.utils.register_class(cls)
    """


    bpy.types.Scene.entrec_props = bpy.props.PointerProperty(type=entrec_props.EntRecProperties)

    





def unregister():
    entrec_main.sv_ipc.DisconnectSockets()
    entrec_main.cl_ipc.DisconnectSockets()


    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.entrec_props



if __name__ == "__main__":
    register()

