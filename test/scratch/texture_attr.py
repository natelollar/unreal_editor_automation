import unreal 

@unreal.uclass()
class EditorUtils(unreal.GlobalEditorUtilityBase):
    pass

selectedAssets = EditorUtils().get_selected_assets()

for i in selectedAssets:
    unreal.log('________________________')
    unreal.log('________________________')
    #unreal.log(i.get_full_name())
    unreal.log(i.get_fname())
    #unreal.log(i.get_path_name())
    #unreal.log(i.get_class())
    i.set_editor_property('srgb', 0)
    print('sRGB:  ' + str(i.get_editor_property('srgb')) )
    unreal.log('________________________')
    unreal.log('________________________')
# coat_mat_OcclusionRoughnessMetallic
# py ....\Unreal Projects\Python\texture_attr.py