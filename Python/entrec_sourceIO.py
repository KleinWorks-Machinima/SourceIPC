#//===================| CUSTOMIZED SOURCE-IO CODE |===================\\
# 
#  Disclaimer: This code has been borrowed and slightly modified from SourceIO Github page
#              to fit the needs of EntRec, this code also doesn't function unless
#              SourceIO is installed as an addon in Blender. None of this code is mine.
#               
#              All of the credit for this code's intricate function goes to the SourceIO Development
#              team and all of it's contributors.
# 
#  SourceIO Github: (https://github.com/REDxEYE/SourceIO)
# 
#//===================| CUSTOMIZED SOURCE-IO CODE |===================\\

from pathlib import Path

import bpy
from bpy.props import (BoolProperty, CollectionProperty, EnumProperty,
                       StringProperty)


from SourceIO.blender_bindings.operators.import_settings_base import ModelOptions, Source1BSPSettings
from SourceIO.blender_bindings.models        import import_model
from SourceIO.blender_bindings.models.common import put_into_collections
from SourceIO.blender_bindings.utils.resource_utils import serialize_mounted_content, deserialize_mounted_content

from SourceIO.library.shared.content_providers.content_manager import ContentManager
from SourceIO.library.utils import FileBuffer







# noinspection PyPep8Naming
class ENTREC_OT_MDLImport(bpy.types.Operator, ModelOptions):
    """Load Source Engine MDL models"""
    bl_idname = "entrec.sourceio_mdl"
    bl_label = "(Entrec) Import Source MDL file"
    bl_options = {'UNDO'}
    
    discover_resources: BoolProperty(name="Mount discovered content", default=True)
    filepath: StringProperty(subtype="FILE_PATH")
    files: CollectionProperty(name='File paths', type=bpy.types.OperatorFileListElement)
    filter_glob: StringProperty(default="*.mdl;*.md3", options={'HIDDEN'})

    def execute(self, context):

        self.scale = 0.05245901639

        if Path(self.filepath).is_file():
            directory = Path(self.filepath).parent.resolve()
        else:
            directory = Path(self.filepath).resolve()
        content_manager = ContentManager()
        if self.discover_resources:
            content_manager.scan_for_content(directory)
            serialize_mounted_content(content_manager)
        else:
            deserialize_mounted_content(content_manager)

        for file in self.files:
            mdl_path = directory / file.name
            with FileBuffer(mdl_path) as f:
                model_container = import_model(mdl_path, f, content_manager, self, None)


            bpy.context.scene.collection.objects.link(model_container.objects[0])
            bpy.context.view_layer.objects.active = model_container.objects[0]
            #put_into_collections(model_container, mdl_path.stem, bodygroup_grouping=self.bodygroup_grouping)
            # if self.import_animations and model_container.armature:
            #     import_animations(content_manager, model_container.mdl, model_container.armature, self.scale)
            # if self.write_qc:
            #     from ... import bl_info
            #     from ...library.source1.qc.qc import generate_qc
            #     qc_file = bpy.data.texts.new('{}.qc'.format(Path(file.name).stem))
            #     generate_qc(model_container.mdl, qc_file, ".".join(map(str, bl_info['version'])))
        return {'FINISHED'}
    


if __name__ == "__main__":
    bpy.utils.register_class(ENTREC_OT_MDLImport)