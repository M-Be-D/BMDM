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
            self.menu()
            self.main_frame.pack(expand=True)

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

    def menu(self):
        """
        Create and arrange the top menu buttons for accessing different functionalities of the application
        """
        # Create a frame at the top of the window to hold the menu buttons and configure its grid layout
        tap_frame = tk.Frame(self.window)
        tap_frame.pack(side='top')
        tap_frame.rowconfigure(0, weight=1)
        tap_frame.columnconfigure(0, weight=1)
        # Create buttons for each main feature and assign their commands
        config_button = tk.Button(tap_frame, text='config', font=("B Nazanin", 12), width=5, height=1, command=self.config)
        admit_button = tk.Button(tap_frame, text='admit', font=("B Nazanin", 12), width=5, height=1, command=self.admit)
        stats_button = tk.Button(tap_frame, text='stats', font=("B Nazanin", 12), width=5, height=1, command=self.stats)
        tag_button = tk.Button(tap_frame, text='tag', font=("B Nazanin", 12), width=5, height=1, command=self.tag)
        find_button = tk.Button(tap_frame, text='find', font=("B Nazanin", 12), width=5, height=1, command=self.find)
        hist_button = tk.Button(tap_frame, text='hist', font=("B Nazanin", 12), width=5, height=1, command=self.hist)
        export_button = tk.Button(tap_frame, text='export', font=("B Nazanin", 12), width=5, height=1, command=self.export)
        remove_button = tk.Button(tap_frame, text='remove', font=("B Nazanin", 12), width=5, height=1, command=self.remove)
        # Arrange the buttons in a single row grid with padding for better spacing
        config_button.grid(row=0, column=0, padx=8, pady=8)
        admit_button.grid(row=0, column=1, padx=8, pady=8)
        stats_button.grid(row=0, column=2, padx=8, pady=8)
        tag_button.grid(row=0, column=3, padx=8, pady=8)
        find_button.grid(row=0, column=4, padx=8, pady=8)
        hist_button.grid(row=0, column=5, padx=8, pady=8)
        export_button.grid(row=0, column=6, padx=8, pady=8)
        remove_button.grid(row=0, column=7, padx=8, pady=8)