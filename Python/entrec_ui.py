#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
# 
#  Purpose: 
# 
#  Product Contributors: Barber
# 
#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\



import bpy





class EntRecControlPanel(bpy.types.Panel):
    bl_idname = "ENTREC_PT_entrec_controlpanel"
    bl_label = "EntRec Control Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "EntRec"


    def draw_header(self, context):
        self.layout.label(text="", icon="MODIFIER_DATA")

    def draw(self, context):
        layout = self.layout

        topRow = layout.row(align=False)

        


        subTopColumn1 = topRow.column(align=False)
        subTopColumn1.alignment = 'RIGHT'

        subTopColumn1.scale_x = 0.8
        subTopColumn1.scale_y = 1


        startrec_op = subTopColumn1.operator('entrec.startrecording', text="Start Recording")
        stoprec_op  = subTopColumn1.operator('entrec.stoprecording',  text="Stop Recording")


        subTopColumn2 = topRow.column(align=False)

        subTopColumn2.enabled = context.scene.entrec_props.is_recording is False

        subTopColumn2.alignment = 'LEFT'

        subTopColumn2.scale_x = 0.95
        subTopColumn2.scale_y = 1



        subTopColumn2.prop(context.scene.entrec_props, 'enable_data_reception', text="Enable Data Reception")

        subTopColumn2.prop(context.scene.entrec_props, 'enable_data_transferring', text="Enable Data Transferring")

        layout.label(text="Path to folder containing \'models\\\' and \'materials\\\':")
        subRow = layout.row()
        subRow.prop(context.scene.entrec_props, 'models_filepath')
        





class TransferDataSettingsSubpanel(bpy.types.Panel):
    bl_label = "Transfer Data"
    bl_idname = "ENTREC_PT_transfer_data_settings"
    bl_parent_id = "ENTREC_PT_entrec_controlpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "EntRec"



    def draw_header(self, context):
        self.layout.label(text="", icon="EXPORT")

    def draw(self, context):
        layout = self.layout

        entList = context.scene.entrec_props.transferring_entlist
        entListIndex = context.scene.entrec_props.transferring_entlist_index

        mainBox = layout.box()

        mainBox.enabled = context.scene.entrec_props.enable_data_transferring is True

        mainBox.label(text="Selected entity info:")

        infoRow1 = mainBox.row(align=False)
        infoRow2 = mainBox.row(align=False)
        infoRow3 = mainBox.row(align=False)

        infoRow1.label(text="Entity ID:")
        infoRow2.label(text="Entity Type:")
        infoRow3.label(text="Entity Model:")

        if len(entList) > entListIndex:
            entity = entList[entListIndex]
            infoRow1.label(text=entity.ent_name)

            infoRow2.label(text=entity.ent_type)

            infoRow3.label(text=entity.ent_modelpath)

        mainBox.template_list(
            listtype_name = "ENTREC_UL_transferring_entlist",
            list_id = "",
            dataptr = context.scene.entrec_props,
            propname = "transferring_entlist",
            active_dataptr = context.scene.entrec_props,
            active_propname = "transferring_entlist_index" 
            )
        
        controlsRow = mainBox.row(align=True)
        if len(entList) < 1 or context.scene.entrec_props.is_recording is True:
            controlsRow.enabled = False
        else:
            controlsRow.enabled = True

        delSelectedOp  = controlsRow.operator('entrec.delete_selected_entity_receiving')






class ReceivingDataSettingsSubpanel(bpy.types.Panel):
    bl_label = "Receiving Data"
    bl_idname = "ENTREC_PT_Receiving_data_settings"
    bl_parent_id = "ENTREC_PT_entrec_controlpanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "EntRec"



    def draw_header(self, context):
        self.layout.label(text="", icon="IMPORT")

    def draw(self, context):
        layout = self.layout

        entList = context.scene.entrec_props.receiving_entlist
        entListIndex = context.scene.entrec_props.receiving_entlist_index

        mainBox = layout.box()

        mainBox.enabled = context.scene.entrec_props.enable_data_reception is True

        mainBox.label(text="Selected entity info:")

        infoRow1 = mainBox.row(align=False)
        infoRow2 = mainBox.row(align=False)
        infoRow3 = mainBox.row(align=False)

        infoRow1.label(text="Entity ID:")
        infoRow2.label(text="Entity Type:")
        infoRow3.label(text="Entity Model:")

        if len(entList) > entListIndex:
            entity = entList[entListIndex]
            infoRow1.label(text=entity.ent_name)

            infoRow2.label(text=entity.ent_type)

            infoRow3.label(text=entity.ent_modelpath)

        mainBox.template_list(
            listtype_name = "ENTREC_UL_receiving_entlist",
            list_id = "",
            dataptr = context.scene.entrec_props,
            propname = "receiving_entlist",
            active_dataptr = context.scene.entrec_props,
            active_propname = "receiving_entlist_index" 
            )
        

        controlsRow = mainBox.row(align=True)
        if len(entList) < 1 or context.scene.entrec_props.is_recording is True:
            controlsRow.enabled = False
        else:
            controlsRow.enabled = True

        delSelectedOp  = controlsRow.operator('entrec.delete_selected_entity_receiving')


