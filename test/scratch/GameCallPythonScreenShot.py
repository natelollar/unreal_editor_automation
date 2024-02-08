import unreal
from datetime import datetime

@unreal.uclass()
class AutomationLib(unreal.AutomationLibrary):
    pass

dateTimeSuffix = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

AutomationLib.take_high_res_screenshot( 1280, 
                                        720, 
                                        'myFancyPicture_' + dateTimeSuffix + '.png', 
                                        None, 
                                        False, 
                                        False, 
                                        unreal.ComparisonTolerance.LOW,  #needed unreal at start
                                        '')

# py ....\Unreal Projects\Python\GameCallPythonScreenShot.py

#connect jump to 'execute console command' in blueprint, to take picture on jump