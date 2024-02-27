import pytest
from utils.ETABS_utils import *
import clr
import pandas as pd
from pathlib import Path


@pytest.fixture(scope="class")
def SapModel_fixture():
    ETABS_exe_path = R"C:\Program Files\Computers and Structures\ETABS 20\ETABS.exe"
    SapModel, myETABSObject = initalize_SapModel(ETABS_exe_path)
    yield SapModel
    exit_ETABS(myETABSObject)


@pytest.fixture(scope="class")
def frames_df_fixture():
    path = Path(R"validation_data\frames_df_results.csv")
    return pd.read_csv(path)


class TestSapModel:
    def test_open_ETABS_file_valid(self, SapModel_fixture):
        """
        Checks that ETABS correctly opens the file for valid model path
        """
        ETABS_model_path_valid = (
            R"test_models\ETABS_gravity\2023-08-29_Gravity Model.EDB"
        )
        assert open_ETABS_file(SapModel_fixture, ETABS_model_path_valid) == True

    def test_open_ETABS_file_invalid(self, SapModel_fixture):
        """
        Checks that ETABS returns None for invalid file path
        """
        ETABS_model_path_invalid = R"test_models"
        assert open_ETABS_file(SapModel_fixture, ETABS_model_path_invalid) == None

    def test_find_load_cases_by_type_valid(self, SapModel_fixture):
        """
        Find load cases for linear static type (1)
        """
        load_cases = [
            "Const",
            "Mech",
            "Dead",
            "Live",
            "Roof Live",
            "S Dead",
            "EQ-X_R=5",
            "EQ-Y_R=5",
            "~LLRF",
        ]
        assert find_load_cases_by_type(SapModel_fixture) == load_cases

    def test_find_load_cases_by_type_bad_type(self, SapModel_fixture):
        """
        Expect none value for load case type that does not exist
        """
        load_case_enum = 10000000
        assert find_load_cases_by_type(SapModel_fixture, load_case_enum) == None

    def test_set_units_valid(self, SapModel_fixture):
        """
        Check for successfull response when unit enumeration is valid
        """
        unit_enum = 1
        assert set_units(SapModel_fixture, unit_enum) == 0

    def test_set_units_invalid(self, SapModel_fixture):
        """
        Check for no response when unit enumeration is invalid
        """
        unit_enum = 10000000
        assert set_units(SapModel_fixture, unit_enum) == None

    def test_get_all_frame_elements(self, SapModel_fixture, frames_df_fixture):
        frames_df = get_all_frame_elements(SapModel_fixture)
        pd.testing.assert_frame_equal(frames_df, frames_df_fixture)


@pytest.fixture
def results_fixture(SapModel_fixture):
    results = analyze_ETABS(SapModel_fixture)
    return results


def test_find_max_axial():
    pass
