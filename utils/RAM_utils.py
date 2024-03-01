import sys  # add RAM concept API installation to path so it can be found (it is in same location as application not in venv)
import requests

from .validation_utils import (
    validate_and_get_path,
    validate_RAM_path,
)

RAM_dir_path = validate_and_get_path(validate_RAM_path, "RAM Concept Python Directory")
sys.path.insert(1, RAM_dir_path)

from ram_concept.concept import Concept
from ram_concept.cad_manager import CadManager
from ram_concept.force_loading_layer import ForceLoadingLayer
from ram_concept.model import Model
from ram_concept.force_loading_layer import ForceLoadingLayer


def start_concept_and_open_model(path, headless=True):
    concept = Concept.start_concept(headless=headless)
    model = concept.open_file(path)
    cad_manager = model.cad_manager
    return concept, model, cad_manager


def set_units_to_US(model):
    units = model.units
    units.set_US_API_units()


def get_all_loading_layers(cad_manager, omitted_layers=["Self-Dead Loading"]):
    # omit self-dead loading because we cannot write to this layer
    return [
        layer.name
        for layer in cad_manager.force_loading_layers
        if layer.name not in omitted_layers
    ]


def check_loading_layer_exists(cad_manager, layer_name):
    current_loading_layers = get_all_loading_layers(cad_manager)
    if layer_name in current_loading_layers:
        return True
    else:
        False


def add_force_loading_layer(cad_manager, new_layer_name):
    if not check_loading_layer_exists(cad_manager, new_layer_name):
        cad_manager.add_force_loading_layer(new_layer_name)


def add_axial_loads_to_loading_layer(cad_manager, layer_name, x, y, Fz):
    print(Fz[0])
    print(type(Fz[0]))
    if check_loading_layer_exists(cad_manager, layer_name):
        force_loading_layer = cad_manager.force_loading_layer(layer_name)
        force_loading_layer.add_point_loads(x, y, Fz=Fz)


def calibrate_ETABS_to_RAM(ETABs_coord: list, RAM_coord: list):
    """
    this function takes the same point in ETABs coordinates and in RAM coordinates and creates
    delta values to adjust coordinates of ETABs loads for proper location into RAM concept

    Assumes coordinates are given in form [x_cord, y_cord]
    """
    location_delta = [RAM_coord[0] - ETABs_coord[0], RAM_coord[1] - ETABs_coord[1]]
    return location_delta
