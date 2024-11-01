#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
# 
#  Purpose: 
# 
#  Product Contributors: Barber
# 
#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\



import bpy



class EntityBone(bpy.types.PropertyGroup):
    name:       bpy.props.StringProperty(name="Name", default="{NO_NAME}")
    proxy_bone: bpy.props.PointerProperty(type=bpy.types.Object)


class EntRecEntity(bpy.types.PropertyGroup):

    ent_id:        bpy.props.IntProperty(   name="ID",    default=0)
    ent_name:      bpy.props.StringProperty(name="Name",  default="{NO_NAME}")
    ent_type:      bpy.props.StringProperty(name="Type",  default="{NO_TYPE}")
    ent_modelpath: bpy.props.StringProperty(name="Model", default="{NO_MODEL}")

    ent_bonelist:  bpy.props.CollectionProperty(type=EntityBone)

    ent_blender_object: bpy.props.PointerProperty(type=bpy.types.Object)
    ent_mesh_object:    bpy.props.PointerProperty(type=bpy.types.Object)


class EntRecProperties(bpy.types.PropertyGroup):
    is_recording: bpy.props.BoolProperty(default=False)

    enable_data_transferring: bpy.props.BoolProperty(default=True)
    enable_data_reception:    bpy.props.BoolProperty(default=True)


    receiving_entlist_index:    bpy.props.IntProperty()
    #transferring_entlist_index: bpy.props.IntProperty()

    receiving_entlist:    bpy.props.CollectionProperty(type=EntRecEntity)
    #transferring_entlist: bpy.props.CollectionProperty(type=EntRecEntity)

    models_filepath: bpy.props.StringProperty(name="Models Filepath", subtype='FILE_PATH', default="\\",)

    scale_factor:    bpy.props.FloatProperty(name="", default=0.05245901639, precision=11,)







class ENTREC_UL_receiving_entlist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        layout.label(text=item.ent_name)
        layout.label(text=item.ent_type)
        layout.label(text=f"{item.ent_id}")
        layout.label(text=item.ent_modelpath)


'''
class ENTREC_UL_transferring_entlist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        
        layout.label(text=item.ent_name)
        layout.label(text=item.ent_type)
        layout.label(text=item.ent_modelpath)
'''


classes = (
    EntityBone,
    EntRecEntity,
    EntRecProperties,
    ENTREC_UL_receiving_entlist,
    #ENTREC_UL_transferring_entlist,
)