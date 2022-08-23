import json
import tkinter as tk
from tkinter import ttk
import sys
import os


# noinspection PyTypeChecker
class SettingsScreen(tk.Toplevel):
    def __init__(self, container):
        super().__init__(container)
        # Variables
        self.controller = container
        self.configure(background="#292929")
        # String Vars
        self.icr_var = tk.StringVar()
        self.gpa_var = tk.StringVar()
        self.api_key_var = tk.StringVar()
        self.account_name_var = tk.StringVar()
        self.schedule_id_var = tk.StringVar()
        # Setup
        self.title("Settings")
        # Widgets
        the_title = ttk.Label(self, text="Settings", font=("Arial", 25), padding=20, anchor="center")
        icr_cutoff_label = ttk.Label(self, text="ICR Cutoff: ", padding=10)
        self.icr_cutoff_entry = ttk.Entry(self, width=5, textvariable=self.icr_var)
        gpa_cutoff_label = ttk.Label(self, text="GPA Cutoff: ", padding=10)
        self.gpa_cutoff_entry = ttk.Entry(self, width=5, textvariable=self.gpa_var)
        api_key_label = ttk.Label(self, text="API Key: ", padding=10)
        self.api_key_entry = ttk.Entry(self, width=30, textvariable=self.api_key_var)
        account_name_label = ttk.Label(self, text="Account Name: ", padding=10)
        self.account_name_entry = ttk.Entry(self, width=15, textvariable=self.account_name_var)
        schedule_id_label = ttk.Label(self, text="Schedule ID: ", padding=10)
        self.schedule_id_entry = ttk.Entry(self, width=10, textvariable=self.schedule_id_var)
        self.edit_button = ttk.Button(self, text="Edit", command=self.enable_entries)
        self.save_button = ttk.Button(self, text="Save", command=self.set_json_data)
        # Layout
        the_title.grid(row=0, column=0, columnspan=2, sticky="ew")
        icr_cutoff_label.grid(row=1, column=0, sticky="e")
        self.icr_cutoff_entry.grid(row=1, column=1, sticky="w", padx=10)
        gpa_cutoff_label.grid(row=2, column=0, sticky="e")
        self.gpa_cutoff_entry.grid(row=2, column=1, sticky="w", padx=10)
        api_key_label.grid(row=3, column=0, sticky="e")
        self.api_key_entry.grid(row=3, column=1, sticky="w", padx=10)
        account_name_label.grid(row=4, column=0, sticky="e")
        self.account_name_entry.grid(row=4, column=1, sticky="w", padx=10)
        schedule_id_label.grid(row=5, column=0, sticky="e")
        self.schedule_id_entry.grid(row=5, column=1, sticky="w", padx=10)
        self.edit_button.grid(row=6, column=0, padx=10, pady=10)
        self.save_button.grid(row=6, column=1, padx=10, pady=10)

        # Functions
        self.get_json_data()
        self.disable_entries()

    def get_json_data(self):
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        path_to_json = os.path.abspath(os.path.join(bundle_dir, 'data.json'))
        with open(path_to_json, "r") as the_file:
            the_data = json.load(the_file)
        self.icr_var.set(the_data["icr"])
        self.gpa_var.set(the_data["gpa"])
        self.api_key_var.set(the_data["api_key"])
        self.account_name_var.set(the_data["account_name"])
        self.schedule_id_var.set(the_data["schedule_id"])

    def set_json_data(self):
        with open("data.json", "w") as the_file:
            new_object = {
                "icr": float(self.icr_var.get()),
                "gpa": float(self.gpa_var.get()),
                "api_key": self.api_key_var.get(),
                "account_name": self.account_name_var.get(),
                "schedule_id": self.schedule_id_var.get()
            }
            json.dump(new_object, the_file)
        self.disable_entries()

    def disable_entries(self):
        for item in self.winfo_children():
            if "entry" in item.winfo_name():
                item["state"] = "disabled"
        self.save_button['state'] = "disabled"
        self.edit_button['state'] = "normal"

    def enable_entries(self):
        for item in self.winfo_children():
            if "entry" in item.winfo_name():
                item["state"] = "normal"
        self.save_button['state'] = "normal"
        self.edit_button['state'] = "disabled"
