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

frames_df = get_all_frame_elements(SapModel)

cols_df = find_columns(frames_df)

# set ETABS units to same foramt as RAM API
lb_in_F = 1
set_units(SapModel, unit_enum=lb_in_F)

results = run_ETABS_analysis(SapModel)
results_setup = get_ETABS_results_setup(results)
change_ETABS_output_case(results_setup, "Dead")
P_max = find_max_axial(results, cols_df["MyNames"].to_list())
print(P_max)

# close ETABS application
exit_ETABS(ETABSObject)
clean_up_ETABS()
