
if "bpy" in locals():
    import importlib
    importlib.reload(pysrc_ipc)
    importlib.reload(pysrcIPC_messages)
else:
    from . import pysrc_ipc
    from . import pysrcIPC_messages

