from ETABS_utils import *


# prompt user for key variables
ETABS_model_folder_path = R"test_models\ETABS_gravity"
ETABS_dll_path = R"C:\Program Files\Computers and Structures\ETABS 20\ETABSv1.dll"
ETABS_model_file_path = R"test_models\ETABS_gravity\2023-08-29_Gravity Model.EDB"
ETABS_exe_path = R"C:\Program Files\Computers and Structures\ETABS 20\ETABS.exe"

# initialize_ETABS_library(ETABS_dll_path)
SapModel, ETABSObject = initalize_SapModel(ETABS_exe_path)
open_ETABS_file(SapModel, ETABS_model_file_path)
load_cases = find_load_cases_by_type(SapModel)
print(load_cases)

results = analyze_ETABS(SapModel)
# close ETABS application
exit_ETABS(ETABSObject)
