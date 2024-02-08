#select base color textures.  looks for other textures in same folder and creates mat inst in same folder



import unreal

print("Hello!")

'''

materialEditingLib = unreal.MaterialEditingLibrary()

#main pbr mat to be instanced
main_mat = unreal.load_asset('/Game/dawnOfWar/materials/master_materials/pbr_tile_mat_layer.pbr_tile_mat_layer')
main_mat_nam = main_mat.get_fname()

#print(str(main_mat_nam))


#select base color texture
selectedAssets = unreal.EditorUtilityLibrary().get_selected_assets()

index = 0
for i in selectedAssets: #i is base color texture
    index += 1
    if '_Base_Color' in str(i.get_fname()): # so all textures can be selected at once and individual base color dont have to be found
        print( 'Base_Color Selected!!!   #__ ' + str(i.get_fname()) + ' __#')

        i_name = i.get_fname()
        i_path = i.get_path_name()

        i_name_raw_str = str(i_name).replace('_Base_Color', '') # name without _BaseColor
        i_folder_path_str = i_path.replace(str(i_name) + '.' + str(i_name), '')

        print(i_name_raw_str)
        print(i_folder_path_str)

        # base color texture test material
        bsClr_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_Base_Color.' + i_name_raw_str + '_BaseColor')

        # normal texture test material
        nrml_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_Normal.' + i_name_raw_str + '_Normal')

        # Metallic texture test material
        mtl_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_Metallic.' + i_name_raw_str + '_Metallic')
        mtl_tex.set_editor_property('srgb', 0) # set to linear color (turn off srgb)

        # Metallic texture test material
        rough_tex = unreal.load_asset(i_folder_path_str + i_name_raw_str + '_Roughness.' + i_name_raw_str + '_Metallic')
        rough_tex.set_editor_property('srgb', 0) # set to linear color (turn off srgb)



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

        # connect correct texture to parameter
        materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                            'BaseColor', 
                                                                            bsClr_tex)
        materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                            'Normal', 
                                                                            nrml_tex)
        materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                            'Metallic', 
                                                                            mtl_tex)
        materialEditingLib.set_material_instance_texture_parameter_value(   myInst, 
                                                                            'Roughness', 
                                                                            rough_tex)


        # recompile (probably unneeded)
        materialEditingLib.update_material_instance(myInst)
    else:
        print(str(i.get_fname()) + ' is not a _Base_Color...   Skipping...')

        
    unreal.log('##____________' + str(index) + '____________##')


print ('ITS DONE!!!')

#this script location, copy and paste in unreal console
#....\unreal_editor_automation\mat_instance_connector_simple1.py

'''
