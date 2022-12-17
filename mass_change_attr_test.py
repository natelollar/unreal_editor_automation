# mass change attributes of all selected objects in unreal editor
import unreal 

selectedAssets = unreal.EditorUtilityLibrary().get_selected_assets()

for i in selectedAssets:
    if '_BaseColor' in str(i.get_fname()):
        print( 'BaseColor:' + str(i.get_fname()) )
        
        #i.set_editor_property('srgb', 0)
        #print('sRGB:  ' + str(i.get_editor_property('srgb')) )

        unreal.log('________________________')
    else:
        print( 'WRONG!:' + str(i.get_fname()) )

print ('DOIN GOOD!')


