"""
This model contains wrapper functions for using the ETABS API.  
The ETABS API is accessed via ETABS.dll which the user is prompted for before
ETABSv1 is imported.

Note: When dealing with ETABS API, ret == 0 indicates a successfull API response.

"""

from pathlib import Path
import json
import pandas as pd
import clr
from validation_utils import (
    prompt_for_dll_path_until_valid,
    ensure_config_exists,
)
from System import String, Array

pd.options.mode.copy_on_write = True  # ensures a copy is returned rather than a view

ensure_config_exists()
ETABS_dll_path = prompt_for_dll_path_until_valid()
# TODO update GUI for better UX and and reocnfiogure to provide config file
ETABS_exe_path = R"C:\Program Files\Computers and Structures\ETABS 20\ETABS.exe"


clr.AddReference(ETABS_dll_path)
from ETABSv1 import *


# # TODO - figure out how to launch and make exe_path are optional
def initalize_SapModel():
    # create API helper object
    helper = cHelper(Helper())
    # create instance of ETABs object from specified path
    myETABSObject = cOAPI(helper.CreateObject(ETABS_exe_path))

    # start ETABS application
    myETABSObject.ApplicationStart()

    # create SapModel object
    return cSapModel(myETABSObject.SapModel), myETABSObject


def open_ETABS_file(SapModel, model_path):
    File = cFile(SapModel.File)
    ret = File.OpenFile(model_path)
    if ret == 0:
        return True
    else:
        return None


def find_load_cases_by_type(SapModel, load_case_type=1):
    LoadCases = cLoadCases(SapModel.LoadCases)
    load_cases = []
    num_names = 0
    try:
        [ret, num_names, load_cases] = LoadCases.GetNameList(
            num_names, load_cases, eLoadCaseType(load_case_type)
        )
        if ret == 0:
            return list(load_cases)
    except ValueError as e:
        print(f"{e}; see ETABS API documentations for valid load case enumerations")


# explore frame data
def convert_system_array_to_list(sys_str):
    p_str = [item for item in sys_str]
    return p_str


def set_units(SapModel, unit_enum=1):
    try:
        ret = SapModel.SetPresentUnits(eUnits(unit_enum))
        return ret
    except ValueError as e:
        print(f"{e}; see ETABS API documentations for valid unit enumerations")


def get_all_frame_elements(SapModel):
    FrameObj = cFrameObj(SapModel.FrameObj)

    NumberNames = 0
    MyNames = []
    PropName = []
    StoryName = []
    PointName1 = []
    PointName2 = []
    Point1X = []
    Point1Y = []
    Point1Z = []
    Point2X = []
    Point2Y = []
    Point2Z = []
    Angle = []
    Offset1X = []
    Offset2X = []
    Offset1Y = []
    Offset2Y = []
    Offset1Z = []
    Offset2Z = []
    CardinalPoint = []

    [
        ret,
        NumberNames,
        MyNames,
        PropName,
        StoryName,
        PointName1,
        PointName2,
        Point1X,
        Point1Y,
        Point1Z,
        Point2X,
        Point2Y,
        Point2Z,
        Angle,
        Offset1X,
        Offset2X,
        Offset1Y,
        Offset2Y,
        Offset1Z,
        Offset2Z,
        CardinalPoint,
    ] = FrameObj.GetAllFrames(
        NumberNames,
        MyNames,
        PropName,
        StoryName,
        PointName1,
        PointName2,
        Point1X,
        Point1Y,
        Point1Z,
        Point2X,
        Point2Y,
        Point2Z,
        Angle,
        Offset1X,
        Offset2X,
        Offset1Y,
        Offset2Y,
        Offset1Z,
        Offset2Z,
        CardinalPoint,
    )
    # create pandas data frame
    if ret == 0:
        data = {
            "MyNames": convert_system_array_to_list(MyNames),
            "PropName": convert_system_array_to_list(PropName),
            "StoryName": convert_system_array_to_list(StoryName),
            "PointName1": convert_system_array_to_list(PointName1),
            "PointName2": convert_system_array_to_list(PointName2),
            "Point1X": convert_system_array_to_list(Point1X),
            "Point1Y": convert_system_array_to_list(Point1Y),
            "Point1Z": convert_system_array_to_list(Point1Z),
            "Point2X": convert_system_array_to_list(Point2X),
            "Point2Y": convert_system_array_to_list(Point2Y),
            "Point2Z": convert_system_array_to_list(Point2Z),
            "Angle": convert_system_array_to_list(Angle),
            "Offset1X": convert_system_array_to_list(Offset1X),
            "Offset2X": convert_system_array_to_list(Offset2X),
            "Offset1Y": convert_system_array_to_list(Offset1Y),
            "Offset2Y": convert_system_array_to_list(Offset2Y),
            "Offset1Z": convert_system_array_to_list(Offset1Z),
            "Offset2Z": convert_system_array_to_list(Offset2Z),
            "CardinalPoint": convert_system_array_to_list(CardinalPoint),
        }

        return pd.DataFrame(data)


def run_ETABS_analysis(SapModel):
    """
    Run ETABS analysis, (compute intensive)
    """
    try:
        Analyze = cAnalyze(SapModel.Analyze)
        ret = Analyze.RunAnalysis()
        return cAnalysisResults(SapModel.Results)
    except:
        print("ETABS analysis failed")


def get_ETABS_results_setup(Results):
    return cAnalysisResultsSetup(Results.Setup)


def change_ETABS_output_case(Setup, load_case):
    try:
        ret = Setup.DeselectAllCasesAndCombosForOutput()
        ret = Setup.SetCaseSelectedForOutput(load_case)
        return ret
    except ValueError as e:
        print(f"{e}; see please select valid load case")


def find_max_axial(Results, frame_objs: list) -> dict:
    ObjectElm = 0
    P_max = {}
    for frame in frame_objs:
        # declare variables
        Name = str(frame)
        NumberResults = 0
        Obj = []
        ObjSta = []
        Elm = []
        ElmSta = []
        LoadCase = []
        StepType = []
        StepNum = []
        P = []
        V2 = []
        V3 = []
        T = []
        M2 = []
        M3 = []

        [
            ret,
            NumberResults,
            Obj,
            ObjSta,
            Elm,
            ElmSta,
            LoadCase,
            StepType,
            StepNum,
            P,
            V2,
            V3,
            T,
            M2,
            M3,
        ] = Results.FrameForce(
            Name,
            eItemTypeElm(ObjectElm),
            NumberResults,
            Obj,
            ObjSta,
            Elm,
            ElmSta,
            LoadCase,
            StepType,
            StepNum,
            P,
            V2,
            V3,
            T,
            M2,
            M3,
        )
        if ret == 0 and NumberResults != 0:
            P_max[frame] = abs(min(P))
        else:
            pass
            # print(f"Bad Response for frame: {frame}")
    return P_max


def find_columns(df):
    return df[(df["Point1X"] == df["Point2X"]) & (df["Point1Y"] == df["Point2Y"])]


def find_levels(df):
    # adjust so it is sorted
    return df["StoryName"].unique().tolist()


def exit_ETABS(myETABSObject):
    ret = myETABSObject.ApplicationExit(True)
    return ret


def clean_up_ETABS():
    global myETABSObject, SapModel
    myETABSObject = None
    SapModel = None
