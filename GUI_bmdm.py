# libraries
from BioMedDataManager import BioMedDataManager
import tkinter as tk
from tkinter import ttk
import os
import json

class GUI_BioMedDataManager():
    '''
    GUI for bmdm project
    '''
    def __init__(self, window: tk.Tk):
        # Set paths and filenames used for storing data and application configurations
        self.bmdm_dir = ".bmdm"
        self.index_file = ".bmdm/index.json"
        self.config_file = ".bmdm/config.json"
        self.objects_dir = ".bmdm/objects"
        self.history_file = ".bmdm/history.log"
        # Initialize the GUI components, create the main frame, and set window properties
        self.window = window
        self.main_frame = tk.Frame(window)
        self.bmdm = BioMedDataManager()
        self.window.title('Biomedical data manager')
        self.window.geometry('640x400')
        self.window.resizable(False, False)
        # Check if data folder exists; if not, run initial boot setup, otherwise display the main menu
        if not os.path.exists('.bmdm'):
            self.boot()
        else:
            ...

    def boot(self):

        # Inner function to handle the boot process: initialize data manager, clear non-main-frame widgets, and load the main menu
        def boot_destroy():

            self.bmdm.boot()
            # Remove all widgets except the main frame to refresh the UI
            for widget in self.window.winfo_children():
                if str(widget) != '.!frame': # Remove all widgets except the main frame
                    widget.destroy()
            # set main menu in window
            self.menu()
            self.main_frame.pack(expand=True)
        # Create and pack a frame to hold the boot screen widgets
        frame = tk.Frame(self.window)
        frame.pack(expand=True)
        # Add a large label and a button to trigger the boot process
        label = tk.Label(frame, text='BMDM Boot', font=("B Nazanin", 40, "bold"))
        label.pack()
        boot_button = tk.Button(
            frame, text='BOOT',
            font=("B Nazanin", 40, "bold"),
            command=boot_destroy,
            anchor='center', bg='lightblue'
        )
        boot_button.pack()