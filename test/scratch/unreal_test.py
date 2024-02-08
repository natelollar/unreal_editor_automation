'''
import unreal

test = unreal.GlobalEditorUtilityBase()

mySel = test.get_selected_assets()

for i in mySel:

    unreal.log('________________________')
    unreal.log('________________________')

    super_name = unreal.log(i.get_fname())

    unreal.log('________________________')
    unreal.log('________________________')

'''
# py Z:\Videos\Unreal Projects\Python\unreal_test.py

import unreal
#myVar = '/Game/dawnOfWar/assets/warlock/coat_mat_OcclusionRoughnessMetallic'
#unreal.log( myVar.get_fname() )


myTexture = unreal.load_asset('/Game/dawnOfWar/assets/warlock/coat_mat_OcclusionRoughnessMetallic.coat_mat_OcclusionRoughnessMetallic')
#for attribute in dir(myTexture): #lists all exposed attributes
#    print (attribute)

#print (help(myTexture))

#unreal.log(myTexture)
#unreal.log(myTexture.get_fname())

prop = myTexture.get_editor_property('srgb')
print(prop)

myTexture.set_editor_property('srgb', 1)
'''
if prop == False:
    myTexture.set_editor_property('srgb', 1)
else:
    print('ALREADY TRUE!')
'''
#Texture2D'/Game/dawnOfWar/assets/warlock/belt_mat_OcclusionRoughnessMetallic.belt_mat_OcclusionRoughnessMetallic'

