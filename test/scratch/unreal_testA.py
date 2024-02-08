import unreal

materialEditingLib = unreal.MaterialEditingLibrary()

# IF OcclusionRoughnessMetalness exist in folder, set rgb to 0

#main pbr mat to be instanced
main_mat = unreal.load_asset('/Game/dawnOfWar/assets/warlock/PBR_mat.PBR_mat')
main_mat_nam = main_mat.get_fname()

#old material to replace with correct name
old_mat = unreal.load_asset('/Game/dawnOfWar/assets/warlock/belt_mat.belt_mat')
old_mat_nam = old_mat.get_fname()

# base color texture test material
bsClr_tex = unreal.load_asset('/Game/dawnOfWar/assets/warlock/belt_mat_BaseColor.belt_mat_BaseColor')
bsClr_tex_nam = bsClr_tex.get_fname()

blueprintName = str(old_mat_nam) + '_inst'
blueprintPath = '/Game/Blueprints'

factory = unreal.MaterialInstanceConstantFactoryNew()
#factory = unreal.MaterialFactoryNew()

factory.set_editor_property( 'create_new', 1 )
factory.set_editor_property( 'edit_after_new', 1 )

assetTools = unreal.AssetToolsHelpers.get_asset_tools()
myInst = assetTools.create_asset( blueprintName , blueprintPath, None, factory)

#save instance created
unreal.EditorAssetLibrary.save_loaded_asset(myInst)

myInst_bsClr = 'BaseColor'

#set instance parent to pre-made material
myInst.set_editor_property('parent', main_mat)
# materialEditingLib.set_material_instance_parent(myInst, old_mat)

#myInst.set_editor_property('scalar_parameter_values', ['1', '1', '1'])
#myInst.set_editor_property('texture_parameter_values', myInst_bsClr(1))
#myInst.set_editor_property('texture_parameter_values', ['BaseColor', 'Normal', 'OcclusionRoughnessMetallic'])
#connect textures
print( myInst.get_texture_parameter_value('BaseColor') )


materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                    'BaseColor', 
                                                                    bsClr_tex)

# recompile (probably unneeded)
materialEditingLib.update_material_instance(myInst)

print('______________________')
print('\n')
print('______________________')



#....\Unreal Projects\Python\unreal_testA.py
