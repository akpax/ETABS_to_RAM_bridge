from pathlib import Path
import json
import pandas as pd
import clr
from validation_utils import prompt_for_dll_path_until_valid, ensure_config_exists
from System import String, Array


ensure_config_exists()
ETABS_dll_path = prompt_for_dll_path_until_valid()


clr.AddReference(ETABS_dll_path)
from ETABSv1 import *


# # TODO - figure out how to launch and make exe_path are optional
def initalize_SapModel(ETABS_exe_path):
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


def find_load_cases_by_type(SapModel, LC_type=1):
    LoadCases = cLoadCases(SapModel.LoadCases)
    load_cases = []
    num_names = 0
    [ret, num_names, load_cases] = LoadCases.GetNameList(
        num_names, load_cases, eLoadCaseType(LC_type)
    )
    if ret == 0:
        return list(load_cases)


# explore frame data
def convert_system_array_to_list(sys_str):
    p_str = [item for item in sys_str]
    return p_str


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


def analyze_ETABS(SapModel):
    return cAnalysisResults(SapModel.Results)


def exit_ETABS(myETABSObject):
    ret = myETABSObject.ApplicationExit(True)
