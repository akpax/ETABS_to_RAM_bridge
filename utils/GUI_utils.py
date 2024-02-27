from tkinter import Tk, Button, filedialog, font
from tkinter import ttk
import json
from ETABS_utils import *
from RAM_utils import *
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


class ETABS_to_RAM_APP:
    def __init__(self, root):
        root.title("ETABS to RAM Concept Column Load Transfer")
        root.geometry("800x600")
        notebook = ttk.Notebook(root)
        f1 = ttk.Frame(notebook)

        f2 = ttk.Frame(notebook)
        notebook.add(f1, text="Model Paths Config")
        notebook.add(f2, text="Load Transfer Hub")
        notebook.pack(expand=True, fill="both")  # pack frames into notebook

        #### f1 WIDGETS ###
        # label and selection for input file
        ttk.Label(
            f1, text="Select ETABS Model file:", font=font.nametofont("TkHeadingFont")
        ).grid(row=0, column=0, pady=20)
        Button(f1, text="Browse", command=self.select_ETABS_model_path).grid(
            row=0, column=2
        )
        self.ETABS_model_path_label = ttk.Label(f1, text="")
        self.ETABS_model_path_label.grid(row=0, column=1)

        ttk.Label(
            f1, text="Select RAM Model file:", font=font.nametofont("TkHeadingFont")
        ).grid(row=1, column=0)
        Button(f1, text="Browse", command=self.select_RAM_model_path).grid(
            row=1, column=2
        )
        self.RAM_model_path_label = ttk.Label(f1, text="")
        self.RAM_model_path_label.grid(row=1, column=1)

        Button(
            f1, text="Access ETABS and RAM Concept Data", command=self.pull_model_data
        ).grid(row=2, column=0, columnspan=3, pady=20)

        self.progress_bar = ttk.Progressbar(
            f1, orient="horizontal", mode="indeterminate"
        )

    def select_ETABS_model_path(self):
        ETABS_model_path = filedialog.askopenfilename(
            filetypes=[("EDB files", "*.EDB")]
        )
        if ETABS_model_path:
            self.ETABS_model_path = ETABS_model_path
            ETABS_model_name = Path(self.ETABS_model_path).name
            self.ETABS_model_path_label.config(
                text=f'"{ETABS_model_name}"', font=path_font
            )

    def select_RAM_model_path(self):
        RAM_model_path = filedialog.askopenfilename(filetypes=[("cpt files", "*.cpt")])
        if RAM_model_path:
            self.RAM_model_path = RAM_model_path
            RAM_model_name = Path(self.RAM_model_path).name
            self.RAM_model_path_label.config(text=f'"{RAM_model_name}"', font=path_font)

    def pull_model_data(self):
        self.progress_bar.grid(row=3, column=2, columnspan=3)
        self.progress_bar.start()
        root.update_idletasks()
        self.SapModel, self.ETABSObject = initalize_SapModel()
        open_ETABS_file(self.SapModel, self.ETABS_model_path)
        print("successfully opened ETABS file")
        self.ETABS_load_cases = find_load_cases_by_type(self.SapModel)
        self.cols_df = find_columns(get_all_frame_elements(self.SapModel))

        lb_in_F = 1
        set_units(self.SapModel, unit_enum=lb_in_F)

        self.concept, self.model, self.cad_manager = start_concept_and_open_model(
            self.RAM_model_path
        )
        set_units_to_US(self.model)
        self.RAM_loading_layers = get_all_loading_layers(self.cad_manager)
        self.progress_bar.stop()

    def transfer_loads(self):
        pass


if __name__ == "__main__":
    root = Tk()
    ETABS_to_RAM_APP(root)
    root.mainloop()
