import os
import sys
import clr
from System import String, Array


# # ETABS_dll_path = input("Please input Path to ETABS .dll")
# clr.AddReference(ETABS_dll_path)
# from ETABSv1 import *


from enum import Enum  # not sure if necessary
from System.Runtime.InteropServices import Marshal  # not sure if necessary


import pandas as pd
from pathlib import Path


def initialize_ETABS_library(path):
    global ETABSv1
    clr.AddReference(path)
    import ETABSv1


def initalize_SapModel(ETABS_exe_path):
    # create API helper object
    helper = ETABSv1.cHelper(ETABSv1.Helper())
    # create instance of ETABs object from specified path
    myETABSObject = ETABSv1.cOAPI(helper.CreateObject(ETABS_exe_path))

    # start ETABS application
    myETABSObject.ApplicationStart()

    # create SapModel object
    return ETABSv1.cSapModel(myETABSObject.SapModel)
