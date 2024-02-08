import unreal
import sys

blueprintName = 'ASteamingBlueprint2'
blueprintPath = '/Game/Blueprints'

createdAssetsCount = int(sys.argv[1])
createdAssetsName = str(sys.argv[2])
createdAssetsName += '%d'  #replace value with number later

factory = unreal.BlueprintFactory()

factory.set_editor_property("ParentClass", unreal.Character)

assetTools = unreal.AssetToolsHelpers.get_asset_tools()

for x in range(createdAssetsCount):
    myFile = assetTools.create_asset(createdAssetsName%(x), blueprintPath, None, factory) #(x) is basically a number
    unreal.EditorAssetLibrary.save_loaded_asset(myFile)


# coat_mat_OcclusionRoughnessMetallic
# py ....\Unreal Projects\Python\CreateAssetWithArgs.py

