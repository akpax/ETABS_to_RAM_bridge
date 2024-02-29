from tkinter import Tk, Button, filedialog, font, StringVar, Listbox, Canvas, N, S, E, W
from tkinter import ttk
import json
from utils.ETABS_utils import *
from utils.RAM_utils import *
from pathlib import Path
from PIL import ImageTk, Image


path_font = "Arial 7 italic"
arrow_image_path = R"images\arrow_medium.png"
blue_button_color_code = "#1F51FF"
white_color_code = "#FFFFFF"
red_button_color_code = "#D04848"


class ETABS_to_RAM_APP:
    def __init__(self, root):
        # initialize attritibutes
        self.ETABS_load_cases = []
        self.ETABS_levels = []
        self.ETABS_model_path = None
        self.RAM_model_path = None
        self.RAM_load_layers = []

        root.title("ETABS to RAM Concept Column Load Transfer")
        root.geometry("800x600")
        self.notebook = ttk.Notebook(root)
        f1 = ttk.Frame(self.notebook)
        f2 = ttk.Frame(self.notebook)
        self.notebook.add(f1, text="Model Paths Config")
        self.notebook.add(f2, text="Load Transfer Hub", state="disabled")
        # self.notebook.tab("Load Transfer Hub", state="normal")
        self.notebook.pack(expand=True, fill="both")  # pack frames into self.notebook

        #######################   f1 Widgets   #######################
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
        Button(
            f1,
            text="Browse",
            command=self.select_RAM_model_path,
        ).grid(row=1, column=2)
        self.RAM_model_path_label = ttk.Label(f1, text="")
        self.RAM_model_path_label.grid(row=1, column=1)

        self.pull_data_button = Button(
            f1,
            text="Access ETABS and RAM Concept Data",
            command=self.pull_model_data,
            state="disabled",
        )
        self.pull_data_button.grid(row=2, column=0, columnspan=3, pady=20)

        self.progress_bar = ttk.Progressbar(
            f1, orient="horizontal", mode="indeterminate"
        )

        #######################   f2 Widgets   #######################
        # __________________ETABS_frame___________________
        self.ETABS_frame = ttk.Frame(f2, relief="raised")
        self.ETABS_frame.grid(row=0, column=0)
        ttk.Label(
            self.ETABS_frame,
            text="ETABS User Inputs:",
            font=font.nametofont("TkHeadingFont"),
        ).grid(row=0, column=0, pady=20)

        ttk.Label(
            self.ETABS_frame,
            text="Select Level:",
            font=font.nametofont("TkDefaultFont"),
        ).grid(row=1, column=0, padx=(10, 0), sticky="w")
        self.levelvar = StringVar(self.ETABS_frame, value=self.ETABS_levels)
        self.combo_box_levels = ttk.Combobox(
            self.ETABS_frame, textvariable=self.levelvar
        )
        self.combo_box_levels.grid(
            row=1, column=1, padx=(0, 10)
        )  # grid after to avoid chaining and assigning .grid() return of None
        self.combo_box_levels["state"] = "readonly"  # make read only

        ttk.Label(
            self.ETABS_frame,
            text="Select Load Cases:",
            font=font.nametofont("TkDefaultFont"),
        ).grid(row=2, column=0, padx=(10, 0), sticky="w")
        self.load_case_var = StringVar(self.ETABS_frame, value=self.ETABS_load_cases)
        self.l_box = Listbox(
            self.ETABS_frame,
            listvariable=self.load_case_var,
            selectmode="extended",
            height=10,
        )
        self.l_box.grid(row=3, column=1, padx=(0, 10))
        ttk.Label(
            self.ETABS_frame,
            text="Note: Multiple Load Cases can be selected",
            font=path_font,
        ).grid(row=4, column=1, pady=(0, 10), padx=(0, 10))

        # __________________arrow image___________________
        img_loc = (35, 35)
        canvas = Canvas(f2, width=120, height=100)
        canvas.grid(row=0, column=1, padx=(40, 0))
        im = Image.open(arrow_image_path)
        im.convert("RGBA")
        self.photoimage = ImageTk.PhotoImage(im)
        canvas.create_image(*img_loc, image=self.photoimage)

        # __________________RAM_frame___________________
        self.RAM_frame = ttk.Frame(f2, relief="raised")
        self.RAM_frame.grid(row=0, column=2)
        ttk.Label(
            self.RAM_frame,
            text="RAM Concept Inputs:",
            font=font.nametofont("TkHeadingFont"),
        ).grid(row=0, column=0, pady=20)

        ttk.Label(
            self.RAM_frame,
            text="Select RAM Loading Layer:",
            font=font.nametofont("TkDefaultFont"),
        ).grid(row=1, column=0, pady=20, sticky="w")
        self.load_layers_var = StringVar(self.RAM_frame, value=self.RAM_load_layers)
        self.combo_box_load_layer = ttk.Combobox(
            self.RAM_frame,
            textvariable=self.load_layers_var,
        )
        self.combo_box_load_layer.grid(
            row=1, column=1, padx=(0, 10)
        )  # grid after to avoid chaining and assigning .grid() return of None
        self.combo_box_load_layer["state"] = "readonly"  # make read only

        ttk.Label(
            self.RAM_frame,
            text="Add Custom Loading Layer:",
            font=font.nametofont("TkDefaultFont"),
        ).grid(row=2, column=0, sticky="w")

        self.user_defined_load_layer = StringVar()
        ttk.Entry(self.RAM_frame, textvariable=self.user_defined_load_layer).grid(
            row=3, column=0
        )
        Button(self.RAM_frame, text="Add", command=self.add_load_layer).grid(
            row=3, column=1
        )

        ### styling ####
        # Colorize alternating lines of the listbox

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
        self.check_enable_data_button(self.pull_data_button)

    def select_RAM_model_path(self):
        RAM_model_path = filedialog.askopenfilename(filetypes=[("cpt files", "*.cpt")])
        if RAM_model_path:
            self.RAM_model_path = RAM_model_path
            RAM_model_name = Path(self.RAM_model_path).name
            self.RAM_model_path_label.config(text=f'"{RAM_model_name}"', font=path_font)
        self.check_enable_data_button(self.pull_data_button)

    def pull_model_data(self):
        self.pull_data_button["state"] = "disabled"
        self.progress_bar.grid(row=3, column=2, columnspan=3)
        self.progress_bar.start()
        root.update_idletasks()
        self.SapModel, self.ETABSObject = initalize_SapModel()
        open_ETABS_file(self.SapModel, self.ETABS_model_path)
        print("successfully opened ETABS file")
        self.ETABS_load_cases = find_load_cases_by_type(self.SapModel)
        self.load_case_var.set(self.ETABS_load_cases)
        # stylze list box entries
        self.stylize_list_box(self.l_box, len(self.ETABS_load_cases))
        print(f"ETABS Load Cases: {self.ETABS_load_cases}")
        self.cols_df = find_columns(get_all_frame_elements(self.SapModel))
        # populate combo box w levels
        self.ETABS_levels = find_levels(self.cols_df)
        self.combo_box_levels["values"] = self.ETABS_levels

        print(self.ETABS_levels)
        lb_in_F = 1
        set_units(self.SapModel, unit_enum=lb_in_F)

        # self.ETABS_results = run_ETABS_analysis(self.SapModel)
        # print(f"ETABS analysis complete")

        self.concept, self.model, self.cad_manager = start_concept_and_open_model(
            self.RAM_model_path
        )
        set_units_to_US(self.model)
        self.RAM_load_layers = get_all_loading_layers(self.cad_manager)
        self.combo_box_load_layer["values"] = self.RAM_load_layers

        self.progress_bar.stop()
        self.notebook.tab(1, state="normal")

        ttk.Separator(self.RAM_frame, orient="horizontal").grid(
            row=4, column=0, columnspan=2, sticky="ew"
        )

        Button(
            self.RAM_frame,
            text="Transfer Loads",
            command=self.transfer_loads,
            bg=blue_button_color_code,
            fg=white_color_code,
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            rowspan=2,
            padx=20,
            pady=(10, 5),
            sticky=(N, S, E, W),
        )

        Button(
            self.RAM_frame,
            text="Calibrate",
            command=self.launch_calibration_window,
            bg=red_button_color_code,
            fg=white_color_code,
        ).grid(row=8, column=0, columnspan=2, padx=(20, 20), pady=(5, 10), sticky="ew")

    def launch_calibration_window(self):
        pass

    def transfer_loads(self):
        user_level_selection = self.combo_box_levels.get()
        print(f"User Level Selection: {user_level_selection}")
        user_ETABS_load_case_selection = self.load_case_var.get()
        print(f"User ETABS Load Case Selection: {user_ETABS_load_case_selection}")
        user_RAM_layer_selection = self.load_layers_var.get()
        print(f" RAM load layer: {user_RAM_layer_selection}")

    def check_enable_data_button(self, button):
        if self.ETABS_model_path is not None and self.RAM_model_path is not None:
            button["state"] = "normal"

    def add_load_layer(self):
        user_entry = self.user_defined_load_layer.get()
        if user_entry != "":
            add_force_loading_layer(self.cad_manager, user_entry)
            print(f"added following user entry: {user_entry}")

    def stylize_list_box(self, list_box, number_items):
        for i in range(0, len(self.ETABS_load_cases), 2):
            list_box.itemconfigure(i, background="#f0f0ff")


class CalibrateWindow:
    def __init__(self):
        pass


if __name__ == "__main__":
    root = Tk()
    ETABS_to_RAM_APP(root)
    root.mainloop()
