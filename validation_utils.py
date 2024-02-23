from GUI_utils import PathSelectorGUI
import clr
import json
from pathlib import Path


def ensure_config_exists(path="config.json"):
    path = Path(path)
    if not path.exists():
        path.touch()


def check_ETABS_import_via_dll_path(path):
    global ETABSv1
    clr.AddReference(path)
    try:
        import ETABSv1

        print("succesfully imported")
        return True
    except ImportError as e:
        print(f"{e}")
        return False


def get_etabs_dll_path_from_config(config_path="config.json"):
    try:
        with open(config_path, "r") as f:
            data = json.load(f)
            return data.get("ETABS_dll_path")
    except (FileNotFoundError, json.JSONDecodeError):
        return None


# TODO modify thsi function so it accepts a different check function asn arg and can vlaidat concept too
def prompt_for_dll_path_until_valid():
    while True:
        ETABS_dll_path = get_etabs_dll_path_from_config()
        if ETABS_dll_path and check_ETABS_import_via_dll_path(ETABS_dll_path):
            print("Successfully imported ETABS module with provided DLL path.")
            return ETABS_dll_path  # Exit loop if the DLL path is valid and module import is successful
        else:
            print("Invalid DLL path. Please select the correct ETABS .dll file.")
            PathSelectorGUI(config_path="config.json").run()
