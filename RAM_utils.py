import sys  # add RAM concept API instalation  to path so it can be found (it is in same location as application not in venv)

raw_path = r"C:\Program Files\Bentley\Engineering\RAM Concept CONNECT Edition\RAM Concept CONNECT Edition V8\python"
sys.path.insert(1, raw_path)

import pandas as pd
from ram_concept.concept import Concept
from ram_concept.model import Model
from ram_concept.model import StructureType
from ram_concept.force_loading_layer import ForceLoadingLayer
from ram_concept.point_load import PointLoad
from ram_concept.point_2D import Point2D


def calibrate_ETABS_to_RAM(ETABs_coord: list, RAM_coord: list):
    """
    this function takes the same point in ETABs coordinates and in RAM coordinates and creates
    delta values to adjust coordinates of ETABs loads for proper location into RAM concept

    Assumes coordinates are given in form [x_cord, y_cord]
    """
    location_delta = [RAM_coord[0] - ETABs_coord[0], RAM_coord[1] - ETABs_coord[1]]
    return location_delta
