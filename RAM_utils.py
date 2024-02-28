import sys  # add RAM concept API installation to path so it can be found (it is in same location as application not in venv)


# TODO clean up these lines with updated validation utils
def add_RAM_module_to_path(path: str):
    sys.path.insert(1, path)


RAM_module_path = R"C:\Program Files\Bentley\Engineering\RAM Concept CONNECT Edition\RAM Concept CONNECT Edition V8\python"
add_RAM_module_to_path(RAM_module_path)
from ram_concept.concept import Concept
from ram_concept.cad_manager import CadManager
from ram_concept.force_loading_layer import ForceLoadingLayer
from ram_concept.model import Model
from ram_concept.force_loading_layer import ForceLoadingLayer

# loading_cause_dict = {
#     "BALANCE": "balance",
#     "HYPERSTATIC": "hyperstatic",
#     "LIVE_PARKING": "live_parking",
#     "LIVE_REDUCIBLE": "live_reducible",
#     "LIVE_ROOF": "live_roof",
#     "LIVE_STORAGE": "live_storage",
#     "LIVE_UNREDUCIBLE": "live_unreducible",
#     "OTHER_DEAD": "other_dead",
#     "OTHER_GRAVITY": "other",
#     "SEISMIC_SERVICE": "seismic_service_",
#     "SEISMIC_ULTIMATE": "seismic_ultimate_",
#     "SELF_DEAD": "self_dead",
#     "SHRINKAGE": "shrinkage",
#     "SNOW": "snow",
#     "STRESSING_DEAD": "stressing_dead",
#     "TEMPERATURE": "temperature",
#     "WIND_SERVICE": "wind_service_",
#     "WIND_ULTIMATE": "wind_ultimate_",
# }


def check_RAM_connection():
    try:
        concept = Concept.start_concept(headless=True)
        if concept.ping() == "PONG":
            concept.shut_down()
            return True
    except:
        return False


def start_concept_and_open_model(path, headless=True):
    concept = Concept.start_concept(headless=headless)
    model = concept.open_file(path)
    cad_manager = model.cad_manager
    return concept, model, cad_manager


def set_units_to_US(model):
    units = model.units
    units.set_US_API_units()


def get_all_loading_layers(cad_manager):
    return [str(layer.name) for layer in cad_manager.force_loading_layers]


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
    if check_loading_layer_exists(layer_name):
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


if __name__ == "__main__":
    RAM_module_path = R"C:\Program Files\Bentley\Engineering\RAM Concept CONNECT Edition\RAM Concept CONNECT Edition V8\python"
    add_RAM_module_to_path(RAM_module_path)
    from ram_concept.concept import Concept

    print(check_RAM_connection())
    Concept.start_concept(headless=False)
