# mass change attributes of all selected objects in unreal editor
import unreal 

selectedAssets = unreal.EditorUtilityLibrary().get_selected_assets()

for i in selectedAssets:
    print( i.get_fname() )
    
    i.set_editor_property('srgb', 0)
    print('sRGB:  ' + str(i.get_editor_property('srgb')) )

    unreal.log('________________________')

print ('DOIN GOOD!')
