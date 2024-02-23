from ETABS_utils import *


# prompt user for key variables
ETABS_model_folder_path = R"test_models\ETABS_gravity"
ETABS_dll_path = R"C:\Program Files\Computers and Structures\ETABS 20\ETABSv1.dll"
ETABS_model_file_path = R"test_models\ETABS_gravity\2023-08-29_Gravity Model.EDB"
ETABS_exe_path = R"C:\Program Files\Computers and Structures\ETABS 20\ETABS.exe"

# initialize_ETABS_library(ETABS_dll_path)
SapModel = initalize_SapModel(ETABS_exe_path)
