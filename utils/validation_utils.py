"""
This module performs functions that perform validation on user provided paths to .dll files (ETABS)
and well as python dirctory of RAM Cconcept. 

These validation functions are used inside the ETABS_utils and RAM_utils modules before importing 
ETABS and RAM specfiic modules. 

If paths are missing or not validated a window will appear prompting the user to provide paths.

"""

import clr
import json
from pathlib import Path
from tkinter import (
    Tk,
    Button,
    filedialog,
    StringVar,
    Listbox,
    Toplevel,
    font,
    messagebox,
)
from tkinter import ttk
import os
import System
import sys


from pathlib import Path


path_font = "Arial 7 italic"
documentation_link = "https://github.com/akpax/ETABs_RAM_bridge"
tk_file_types = {
    "ETABS .dll": ("DLL files", "*.dll"),
    "ETABS .exe": ("EXE files", "*.exe"),
    "RAM Concept Python Directory": None,
}


class PathSelectorGUI:
    def __init__(self, root, validation_func, file_type, config_path="config.json"):
        self.config_path = config_path
        self.validation_func = validation_func
        self.file_type = file_type
        self.root = root
        self.path = None

        if tk_file_types[file_type] is None:
            browse_comand = self.select_directory
        else:
            browse_comand = self.select_path

        root.title("File Selector")

        # label and selection for input file
        ttk.Label(
            root,
            text=f"Select {file_type} file:",
            font=font.nametofont("TkHeadingFont"),
        ).grid(row=0, column=0, padx=30, pady=10, sticky="w")
        Button(root, text="Browse", command=browse_comand).grid(
            row=0, column=2, ipadx=10, ipady=3, padx=30
        )
        self.path_label = ttk.Label(root, text="")
        self.path_label.grid(row=0, column=1)

        Button(root, text="Submit", command=self.on_submit).grid(
            row=8, column=1, columnspan=2, ipadx=25, ipady=3, pady=25
        )

    def select_path(self):
        path = filedialog.askopenfilename(filetypes=[tk_file_types[self.file_type]])
        if path:
            self.initialize_and_display_path(path)

    def select_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.initialize_and_display_path(path)

    def initialize_and_display_path(self, path):
        self.path = path
        file_name = Path(self.path).name
        self.path_label.config(text=f'"{file_name}"', font=path_font)

    def on_submit(self):
        if self.validation_func(self.path):
            add_or_replace_json_key(self.file_type, self.path, self.config_path)
            messagebox.showinfo(
                title="Success",
                message="Path provided has been validated and stored in config.json for future use.",
            )
            self.root.destroy()

        else:
            messagebox.showerror(
                master=self.root,
                title="Success",
                message=f"Path provided did not pass validation. \n Please submit alternate path",
            )


def ensure_config_exists(path):
    path = Path(path)
    if not path.exists():
        path.touch()


def validate_ETABS_dll_path(path):
    global ETABSv1
    try:
        clr.AddReference(path)
        import ETABSv1

        print("succesfully imported")
        return True
    except Exception as e:
        print(f"{e}")
        return False


def validate_ETABS_exe_path(path):
    """
    Opting out of validating ETABS path for now due to computational time cost
    """
    return True


def validate_RAM_path(path):
    try:
        sys.path.insert(1, path)
        from ram_concept.concept import Concept

        concept = Concept.start_concept(headless=True)
        if concept.ping() == "PONG":
            concept.shut_down()
            return True
    except:
        return False


def get_path_from_config(key, path):
    try:
        with open(path, "r") as f:
            data = json.load(f)
            return data.get(key)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def add_or_replace_json_key(key, value, path):
    """
    Adds or replaces a key in a JSON file.
    """

    try:
        with open(path, "r", encoding="utf-8") as file:
            content = json.load(file)

        # Add or replace the key-value pair
        content[key] = value
    except json.JSONDecodeError as e:  # acount for empty .json case
        print(f"Error decoding JSON from file {path}: {e}")
        content = {key: value}
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        # Write the updated content back to the file
        with open(path, "w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=4)
            return True


def validate_and_get_path(validation_func, key, config_path="config.json"):
    ensure_config_exists(config_path)
    path = get_path_from_config(key, config_path)
    if path is None or not validation_func(path):
        # GUI prompts user for path and writes to json
        root = Tk()
        PathSelectorGUI(
            root,
            validation_func,
            key,
        )
        root.mainloop()
        path = get_path_from_config(key, config_path)
    return path
