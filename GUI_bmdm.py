# libraries
from BioMedDataManager import BioMedDataManager
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
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
    
    def config(self):
        '''to configure and store user or doctor information'''
        #
        def _config():
            self.bmdm.config(name.get(), email.get())
            name_entry.config(state='readonly', bg='lightgrey')
            email_entry.config(state='readonly', bg='lightgrey')
        # Internal function to enable editing of the name and email input fields
        def _changeable():
            name_entry.config(state='normal', bg='white')
            email_entry.config(state='normal', bg='white')

        # Load existing configuration data from file
        with open(self.config_file, 'r') as conf_file:
            config_file = json.load(conf_file)
            
        self._destroy_frame() # Clear current frame before loading new widgets
        # Initialize StringVar variables with current configuration values
        name = tk.StringVar()
        name.set(config_file['manager']['name'])
        email = tk.StringVar()
        email.set(config_file['manager']['email'])
        # Create labels, input fields, and buttons for user interaction
        name_label = tk.Label(self.main_frame, text=':نام خود را وارد کنید')
        name_entry = tk.Entry(self.main_frame, textvariable=name)
        email_label = tk.Label(self.main_frame, text=':ایمیل خود را وارد کنید')
        email_entry = tk.Entry(self.main_frame, textvariable=email)
        submit_button = tk.Button(self.main_frame, text='ثبت', command=_config)
        change_value_button = tk.Button(self.main_frame, text='تغییر', command=_changeable)
        # Arrange widgets using grid layout
        name_label.grid(row=0, column=1, padx=3)
        name_entry.grid(row=0, column=0)
        email_label.grid(row=1, column=1, padx=3, pady=30)
        email_entry.grid(row=1, column=0, pady=30)
        submit_button.grid(row=2, column=0)
        change_value_button.grid(row=2, column=1)
        # Set the initial state of input fields to readonly if they already contain data
        if name.get():
            name_entry.config(state='readonly', bg='lightgrey')
        if email.get():
            email_entry.config(state='readonly', bg='lightgrey')

    def _destroy_frame(self):
        '''To destroy frame and cleaning screen'''
        if self.main_frame:    
            for widget in self.main_frame.winfo_children():
                widget.destroy()

    def admit(self):
        '''To add medical data'''
        self._destroy_frame() # Clear the main frame before loading admit widgets
        # Internal function to submit the selected file or folder path for admitting data,
        # and display success message upon completion
        def _admit():
            self.bmdm.admit(path)
            # successful
            success_label.config(text='با موفقیت انجام شد', font=("B Nazanin", 10, 'bold'), fg='green')
            # Update the UI label to show success message to the user

        # Open file dialog to select a single file and update the path input field accordingly
        def choose_file():
            global path #
            # Enable the path input field and clear its content
            path_input.config(state="normal")
            path_input.delete(0, tk.END)
            success_label.config(text='')
            # Open a dialog for selecting a single file (txt or json)
            path = filedialog.askopenfilename(
                title='انتخاب فایل',
                filetypes=[("Json files", "*.txt"), ("Text files", "*.json")]
            )
            path_input.insert(0, path)
            path_input.config(state='readonly')
        # clear and update the path input field with the selected folder path
        def choose_folder():  
            global path #
            # Enable the path input field and clear its content
            path_input.config(state="normal")
            path_input.delete(0, tk.END)
            success_label.config(text='')
            # Open a dialog for selecting a directory (folder)
            path = filedialog.askdirectory(title="انتخاب پوشه")
            path_input.insert(0, path)
            path_input.config(state="readonly")
        # Update the file button text and command based on the selected radio button (file or folder)
        def choose():
            # Enable and clear the path input field before new selection
            path_input.config(state="normal")
            path_input.delete(0, tk.END)
            success_label.config(text='')
            # Update the file selection button to correspond to the selected mode (file or folder)
            if choose_rbutton.get()=='file':
                file_button.config(text='انتخاب فایل', command=choose_file)
            if choose_rbutton.get()=='folder':
                file_button.config(text='انتخاب پوشه', command=choose_folder)
        # Show a help message box explaining supported formats and usage instructions
        def _help():
            help_massage = 'این نرم افزار فقط از فرمت های txt و json پشتیبانی میکنه\nاگر میخواهید فایلی را انتخاب کنید با زدن گزینه "انتخاب فایل" آن را انتخاب کنید\nو اگر میخواهید چند فایل را انتخاب کنید همه را در یک پوشه بریزید و پوشه را انتخاب کنید.'
            messagebox.showinfo(title='info', message=help_massage)
        # Define all main menu buttons with their labels, fonts, sizes, and command callbacks
        choose_rbutton = tk.StringVar()
        choose_rbutton.set('file') #
        label = tk.Label(self.main_frame, text=':روش ثبت اطلاعات بیمار یا بیماران را انتخاب کنید')
        file = tk.Radiobutton(self.main_frame, text='فایل', variable=choose_rbutton, value='file', command=choose)
        folder = tk.Radiobutton(self.main_frame, text='پوشه', variable=choose_rbutton, value='folder', command=choose)
        help_button = tk.Button(self.main_frame, text='?', font=("Arial", 10, "bold"), command=_help)
        file_button = tk.Button(self.main_frame, text='انتخاب فایل', command=choose_file)
        path_input = tk.Entry(self.main_frame, width=50)
        submit_button = tk.Button(self.main_frame, text='ثبت', command=_admit)
        success_label = tk.Label(self.main_frame)
        # Arrange all buttons in a single row with padding for spacing
        label.grid(row=0,column=3, pady=20)
        file.grid(row=0,column=2, pady=20)
        folder.grid(row=0,column=1, pady=20)
        help_button.grid(row=0,column=0)
        file_button.grid(row=1,column=3)
        path_input.grid(row=1,column=2)
        submit_button.grid(row=1,column=0)
        success_label.grid(row=2,column=2)