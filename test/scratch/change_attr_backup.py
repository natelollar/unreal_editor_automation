import unreal 

#@unreal.uclass()
#class EditorUtils(unreal.GlobalEditorUtilityBase):
#    pass

#selectedAssets = EditorUtils().get_selected_assets()

selectedAssets = unreal.EditorUtilityLibrary().get_selected_assets()


for i in selectedAssets:
    print(i.get_fname())
    #unreal.log(i.get_fname())
    
    i.set_editor_property('srgb', 0)
    print('sRGB:  ' + str(i.get_editor_property('srgb')) )

    unreal.log('________________________')

print ('DOIN GOOD!')
# py ...\Unreal Projects\Python\list_selected.py