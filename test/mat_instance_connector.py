#wip; will replace object material with a standard pbr material instance and auto connect textures
import unreal

materialEditingLib = unreal.MaterialEditingLibrary()

# IF OcclusionRoughnessMetalness exist in folder, set rgb to 0

#test object
tst_obj = unreal.load_asset('/Game/dawnOfWar/assets/orc/orc_dup.orc_dup')

#main pbr mat to be instanced
main_mat = unreal.load_asset('/Game/dawnOfWar/assets/materials/unreal_pbr_base_mat.unreal_pbr_base_mat')
main_mat_nam = main_mat.get_fname()

#old material to replace with correct name
old_mat = unreal.load_asset('/Game/dawnOfWar/assets/orc/materials/orc/test/orc_loincloth_mat_blinn_dup.orc_loincloth_mat_blinn_dup')
old_mat_nam = old_mat.get_fname()

# base color texture test material
bsClr_tex = unreal.load_asset('/Game/dawnOfWar/assets/orc/materials/orc/test/orc_loincloth_BaseColor_dup.orc_loincloth_BaseColor_dup')
bsClr_tex_nam = bsClr_tex.get_fname()
# normal texture test material
nrml_tex = unreal.load_asset('/Game/dawnOfWar/assets/orc/materials/orc/test/orc_loincloth_Normal_dup.orc_loincloth_Normal_dup')
nrml_tex_nam = bsClr_tex.get_fname()
# OcclusionRoughnessMetallic texture test material
aoRfMet_tex = unreal.load_asset('/Game/dawnOfWar/assets/orc/materials/orc/test/orc_loincloth_OcclusionRoughnessMetallic_dup.orc_loincloth_OcclusionRoughnessMetallic_dup')
aoRfMet_tex_nam = bsClr_tex.get_fname()



blueprintName = str(old_mat_nam).replace('_blinn_dup', '_inst')
blueprintPath = '/Game/Test_Mat_Output'

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


# Get a list of all mesh components on the object
#mesh_components = unreal.MeshEditorModule.get_mesh_components(tst_obj)

#unreal.MaterialBakingHelpers.replace_materials_on_single_mesh(mesh_components, 'orc_loincloth_mat_inst', old_material_name='orc_loincloth_mat_blinn_dup')



# recompile (probably unneeded)
materialEditingLib.update_material_instance(myInst)

tst_obj.set_material(11, myInst)


print('______________________' + '\n' + '______________________')


#copy and paste script location into unreal console



