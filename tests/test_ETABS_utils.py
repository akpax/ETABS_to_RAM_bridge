import pytest
from utils.ETABS_utils import *
import clr

# # ad reference to import ETABSv1, not imported when using pytest
ETABS_dll_path = R"C:\Program Files\Computers and Structures\ETABS 20\ETABSv1.dll"
clr.AddReference(ETABS_dll_path)
clr.AddReference(ETABS_dll_path)
from ETABSv1 import *


ETABS_model_path_invalid = R"test_models"


@pytest.fixture(scope="class")
def Sapmodel_fixture(ETABS_exe_path):
    ETABS_exe_path = R"C:\Program Files\Computers and Structures\ETABS 20\ETABS.exe"
    SapModel, ETABSObject = initalize_SapModel(ETABS_exe_path)
    yield SapModel, ETABSObject
    exit_ETABS()


class TestSapModel:
    def test_open_ETABS_file_valid(SapModel):
        """
        Checks that ETABS correctly opens the file for valid model path
        """
        ETABS_model_path_valid = (
            SapModel,
            R"test_models\ETABS_gravity\2023-08-29_Gravity Model.EDB",
        )
        assert open_ETABS_file(SapModel, ETABS_model_path_valid) == True

    def test_open_ETABS_file_invalid(SapModel):
        """
        Checks that ETABS returns None for invalid file path
        """
        ETABS_model_path_invalid = R"test_models"
        assert open_ETABS_file(SapModel, ETABS_model_path_invalid) == False
