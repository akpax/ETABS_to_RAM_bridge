from tkinter import Tk, Button, filedialog, font, StringVar, Listbox
from tkinter import ttk
import json
import os
from .GUI_utils import *
from .RAM_utils import *
from pathlib import Path


path_font = "Arial 7 italic"


class PathSelectorGUI:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path

        self.win = Tk()
        self.win.title("File Selector")

        self.dll_path = None

        # label and selection for input file
        ttk.Label(
            self.win,
            text="Select ETABS .dll file:",
            font=("Arial 13 bold"),
        ).grid(row=0, column=0, padx=30, pady=10, sticky="w")
        Button(self.win, text="Browse", command=self.select_dll_path).grid(
            row=0, column=2, ipadx=10, ipady=3, padx=30
        )
        self.dll_path_label = ttk.Label(self.win, text="")
        self.dll_path_label.grid(row=0, column=1)

        Button(self.win, text="Submit", command=self.on_submit).grid(
            row=8, column=1, columnspan=2, ipadx=25, ipady=3, pady=25
        )

    def select_dll_path(self):
        dll_path = filedialog.askopenfilename(filetypes=[("DLL files", "*.dll")])
        if dll_path:
            self.dll_path = dll_path
            self.dll_path_label.config(text=f'"{self.dll_path}"', font=path_font)

    def on_submit(self):
        self.write_to_config_json()
        self.win.destroy()

    def write_to_config_json(self):
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        data["ETABS_dll_path"] = self.dll_path
        with open(self.config_path, "w") as f:
            json.dump(data, f)

    def run(self):
        self.win.mainloop()


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Determine the absolute path to the directory containing the main script.
        # This assumes that the main script is located in the project root.
        main_dir = os.path.dirname(os.path.abspath(sys.modules["__main__"].__file__))
        print(sys.modules["__main__"].__file__)
        print(main_dir)
        base_path = main_dir

    return os.path.join(base_path, relative_path)
