#wip; will replace object material with a standard pbr material instance and auto connect textures
import unreal

materialEditingLib = unreal.MaterialEditingLibrary()

# IF OcclusionRoughnessMetalness exist in folder, set rgb to 0

#test object
tst_obj = unreal.load_asset('/Game/Blueprintzzzzzz/warlock_all_lowA_warlock_belt_low_dup.warlock_all_lowA_warlock_belt_low_dup')

#main pbr mat to be instanced
main_mat = unreal.load_asset('/Game/dawnOfWar/assets/warlock/PBR_mat.PBR_mat')
main_mat_nam = main_mat.get_fname()

#old material to replace with correct name
old_mat = unreal.load_asset('/Game/dawnOfWar/assets/warlock/belt_mat.belt_mat')
old_mat_nam = old_mat.get_fname()

# base color texture test material
bsClr_tex = unreal.load_asset('/Game/dawnOfWar/assets/warlock/belt_mat_BaseColor.belt_mat_BaseColor')
bsClr_tex_nam = bsClr_tex.get_fname()
# normal texture test material
nrml_tex = unreal.load_asset('/Game/dawnOfWar/assets/warlock/belt_mat_Normal.belt_mat_Normal')
nrml_tex_nam = bsClr_tex.get_fname()
# OcclusionRoughnessMetallic texture test material
aoRfMet_tex = unreal.load_asset('/Game/dawnOfWar/assets/warlock/belt_mat_OcclusionRoughnessMetallic.belt_mat_OcclusionRoughnessMetallic')
aoRfMet_tex_nam = bsClr_tex.get_fname()



blueprintName = str(old_mat_nam) + '_inst'
blueprintPath = '/Game/Blueprintzzzzzz'

factory = unreal.MaterialInstanceConstantFactoryNew()

factory.set_editor_property( 'create_new', 1 )
factory.set_editor_property( 'edit_after_new', 1 )

assetTools = unreal.AssetToolsHelpers.get_asset_tools()
myInst = assetTools.create_asset( blueprintName , blueprintPath, None, factory)

#save instance created
unreal.EditorAssetLibrary.save_loaded_asset(myInst)

myInst_bsClr = 'BaseColor'

#set instance parent to pre-made material
myInst.set_editor_property('parent', main_mat)

# connect correct texture to parameter
materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                    'BaseColor', 
                                                                    bsClr_tex)
materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                    'Normal', 
                                                                    nrml_tex)
materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                    'OcclusionRoughnessMetallic', 
                                                                    aoRfMet_tex)

# recompile (probably unneeded)
materialEditingLib.update_material_instance(myInst)

tst_obj.set_material(0, myInst)

print('______________________' + '\n' + '______________________')







