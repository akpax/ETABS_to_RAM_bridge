from pathlib import Path
import json
import clr
from validation_utils import prompt_for_dll_path_until_valid, ensure_config_exists
from System import String, Array


ensure_config_exists()
ETABS_dll_path = prompt_for_dll_path_until_valid()


clr.AddReference(ETABS_dll_path)
from ETABSv1 import *


# from enum import Enum  # not sure if necessary
# from System.Runtime.InteropServices import Marshal  # not sure if necessary


# import pandas as pd


# # TODO - find work arond fopr making ETABs global
# # def initialize_ETABS_library(path):
# #     global ETABSv1
# #     clr.AddReference(path)
# #     import ETABSv1


# # TODO - figure out how to launch and make exe_path are optional
def initalize_SapModel(ETABS_exe_path):
    # create API helper object
    helper = cHelper(Helper())
    # create instance of ETABs object from specified path
    myETABSObject = cOAPI(helper.CreateObject(ETABS_exe_path))

    # start ETABS application
    myETABSObject.ApplicationStart()

    # create SapModel object
    return cSapModel(myETABSObject.SapModel)
