import unreal

def set_mi_texture(mi_asset, param_name, tex_path):
    if not unreal.EditorAssetLibrary.does_asset_exist(tex_path):
        unreal.log_warning("Can't find texture: " + tex_path)
        return False

    tex_asset = unreal.EditorAssetLibrary.find_asset_data( tex_path ).get_asset()
    return unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mi_asset, param_name, tex_asset)

unreal.log("---------------------------------------------------")

AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
MaterialEditingLibrary = unreal.MaterialEditingLibrary
EditorAssetLibrary = unreal.EditorAssetLibrary

base_mtl = unreal.EditorAssetLibrary.find_asset_data("/Game/Environment/Cave/Materials/M_CaveBase")
    
#Iterate over selected meshes
sel_assets = unreal.EditorUtilityLibrary.get_selected_assets()

for sm_asset in sel_assets:
    if sm_asset.get_class().get_name() != "StaticMesh":
        continue #skip non-static-meshes
    
    asset_name = sm_asset.get_name()    
    if asset_name.startswith("S_"):
        asset_name = asset_name[2:] # Store mesh name without prefix

    asset_folder = unreal.Paths.get_path(sm_asset.get_path_name()) 

    base_folder = asset_folder[:-7] #get base folder (subtract "Meshes" from base path)
    mtl_folder = base_folder + "/Materials/"
    tex_folder = base_folder + "/Textures/"
    
    #create folder for materials if not exist
    if not unreal.EditorAssetLibrary.does_directory_exist(mtl_folder):
        unreal.EditorAssetLibrary.make_directory(mtl_folder)

    #name of material instance for this mesh
    mi_name = "MI_" + asset_name            
    mi_full_path = mtl_folder + mi_name

    #Check if material instance already exists
    if EditorAssetLibrary.does_asset_exist(mi_full_path):
        mi_asset = EditorAssetLibrary.find_asset_data(mi_full_path).get_asset()
        unreal.log("Asset already exists")
    else:
        mi_asset = AssetTools.create_asset(mi_name, mtl_folder, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())        

    #set material instance parameters!
    MaterialEditingLibrary.set_material_instance_parent( mi_asset, base_mtl.get_asset() )  # set parent material
    MaterialEditingLibrary.set_material_instance_scalar_parameter_value( mi_asset, "Desaturation", 0.3) # set scalar parameter 

    #find textures for this mesh
    set_mi_texture(mi_asset, "Base Color", tex_folder + "T_" + asset_name + "_basecolor")
    set_mi_texture(mi_asset, "Masks Map", tex_folder + "T_" + asset_name + "_masks")
    set_mi_texture(mi_asset, "Normal", tex_folder + "T_" + asset_name + "_normal")
    set_mi_texture(mi_asset, "BentNormal", tex_folder + "T_" + asset_name + "_Bentnormal")

    #set new material instance on static mesh    
    sm_asset.set_material(0, mi_asset)