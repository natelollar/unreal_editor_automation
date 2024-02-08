#select base color textures.  looks for other textures in same folder and creates mat inst in same folder

import unreal

materialEditingLib = unreal.MaterialEditingLibrary()

#main pbr mat to be instanced
main_mat = unreal.load_asset('/Game/dawnOfWar/materials/master_materials/basic_pbr_base_mat.basic_pbr_base_mat')
main_mat_nam = main_mat.get_fname()

#select base color texture
selectedAssets = unreal.EditorUtilityLibrary().get_selected_assets()

index = 0
for i in selectedAssets: #i is base color texture
    index += 1
    if '_Albedo' in str(i.get_fname()): # so all textures can be selected at once and individual base color dont have to be found
        print( 'Albedo Selected!!!   #__ ' + str(i.get_fname()) + ' __#')

        i_name = i.get_fname()
        i_path = i.get_path_name()

        i_name_raw_str = str(i_name).replace('_Albedo', '') # name without _BaseColor
        i_folder_path_str = i_path.replace(str(i_name) + '.' + str(i_name), '')

        print(i_name_raw_str)
        print(i_folder_path_str)

        # base color texture material
        bsClr_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_Albedo.' + i_name_raw_str + '_Albedo')

        # normal texture material
        nrml_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_Normal.' + i_name_raw_str + '_Normal')

        # OcclusionRoughnessMetallic texture material
        #aoRfMet_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_OcclusionRoughnessMetallic.' + i_name_raw_str + '_OcclusionRoughnessMetallic')
        #aoRfMet_tex.set_editor_property('srgb', 0) # set to linear color (turn off srgb)

        # Roughness texture material
        rf_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_Roughness.' + i_name_raw_str + '_Roughness')
        rf_tex.set_editor_property('srgb', 0) # set to linear color (turn off srgb)

        # Metalness texture material
        met_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_Metalness.' + i_name_raw_str + '_Metalness')
        met_tex.set_editor_property('srgb', 0) # set to linear color (turn off srgb)
        
        # Ambient Occlusion texture material
        ao_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_AO.' + i_name_raw_str + '_AO')
        ao_tex.set_editor_property('srgb', 0) # set to linear color (turn off srgb)


        # Emissive texture material
        emis_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_Emissive.' + i_name_raw_str + '_Emissive')
        emis_tex_nam = bsClr_tex.get_fname()



        blueprintName = i_name_raw_str + '_mat_inst'
        blueprintPath = i_folder_path_str #create mat inst in same folder as selected base color tex

        factory = unreal.MaterialInstanceConstantFactoryNew()

        factory.set_editor_property( 'create_new', 1 )
        factory.set_editor_property( 'edit_after_new', 1 )

        assetTools = unreal.AssetToolsHelpers.get_asset_tools()
        myInst = assetTools.create_asset( blueprintName , blueprintPath, None, factory)

        #save instance created
        unreal.EditorAssetLibrary.save_loaded_asset(myInst)


        #set instance parent to pre-made material
        myInst.set_editor_property('parent', main_mat)

        # connect correct texture to parameter (assuming only emissive is optional)
        materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                            'BaseColor', 
                                                                            bsClr_tex)
        materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                            'Normal', 
                                                                            nrml_tex)
        materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                            'Roughness', 
                                                                            rf_tex)
        materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                            'Metallic', 
                                                                            met_tex)
        
        #if AO or Emissive (not always present)
        if ao_tex != None:
            materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                                'AO', 
                                                                                ao_tex)
        else:
            pass
            
        if emis_tex != None:
            materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                                'Emissive', 
                                                                                emis_tex)
            materialEditingLib.set_material_instance_scalar_parameter_value(    myInst, 
                                                                                'Emissive_Scalar', 
                                                                                1.0)
        else:
            pass

        # recompile (maybe unneeded)
        materialEditingLib.update_material_instance(myInst)
    else:
        print(str(i.get_fname()) + ' is not a _BaseColor...   Skipping...')

        
    unreal.log('##____________' + str(index) + '____________##')


print ('ITS DONE!!!')

#copy and paste script location into unreal console
#....\unreal_editor_automation\mat_instance_connector_simple.py


