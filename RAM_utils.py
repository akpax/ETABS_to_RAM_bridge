import sys  # add RAM concept API installation to path so it can be found (it is in same location as application not in venv)


def add_RAM_module_to_path(path: str):
    sys.path.insert(1, path)


def check_RAM_connection():
    try:
        concept = Concept.start_concept(headless=True)
        if concept.ping() == "PONG":
            concept.shut_down()
            return True
    except:
        return False


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
