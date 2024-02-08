# create material instance
import unreal

mySel = unreal.EditorUtilityLibrary().get_selected_assets()

for i in mySel:
    old_mat = i.get_material(0)
    print( i.get_material(0) )
    old_mat()


    unreal.log( '________________________' )


# ....\Unreal Projects\Python\create_mat_inst.py


#MaterialInstanceConstant'/Game/dawnOfWar/assets/warlock/PBR_mat_hat.PBR_mat_hat'

