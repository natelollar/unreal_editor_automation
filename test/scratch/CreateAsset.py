import unreal

blueprintName = 'ASteamingBlueprint2'
blueprintPath = '/Game/Blueprints'



factory = unreal.BlueprintFactory()

factory.set_editor_property("ParentClass", unreal.PlayerController)

assetTools = unreal.AssetToolsHelpers.get_asset_tools()
myFile = assetTools.create_asset(blueprintName, blueprintPath, None, factory)

unreal.EditorAssetLibrary.save_loaded_asset(myFile)



# py ....\Unreal Projects\Python\CreateAsset.py

