
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from ttkbootstrap import Style
import ttkbootstrap as tb


# Ensure ttkbootstrap is the first to create the Tk root
tb_style = tb.Style('darkly')  # applies theme to all ttkbootstrap widgets

class Application(tb.Window):
    """
    Main application window for saving or appending a Matplotlib figure to a PDF.
    """
    def __init__(self, fig=None, figures_dir='figures'):
        super().__init__(
            title='Save or Append Plot PDF',
            themename='darkly',
            size=(400, 180),
            resizable=(False, False),
            padding=10
        )
        self.fig = fig
        self.figures_dir = figures_dir
        # main content frame
        self.pdf_frame = PDFOptions(self)
        self.pdf_frame.pack(fill='both', expand=True)

class PDFOptions(ttk.Labelframe):(ttk.Labelframe):
    def __init__(self, master, padding=0):
        super().__init__(master, text='PDF File Options', padding=(20, 10, 10, 5))
        self.columnconfigure(1, weight=1)

        # variables
        self.pdf_path_var   = tk.StringVar()
        self.create_new_var = tk.BooleanVar(value=False)
        self.new_name_var   = tk.StringVar()

        # Row 0: PDF file selection
        ttk.Label(self, text='PDF File').grid(row=0, column=0, padx=10, pady=5, sticky='w')
        ttk.Entry(self, textvariable=self.pdf_path_var).grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        ttk.Button(
            self,
            text='Browse',
            command=self.on_browse,
            style='primary.TButton'
        ).grid(row=0, column=2, padx=10, pady=5)

        # Row 1: Create new file option
        ttk.Radiobutton(
            self,
            text='Create new file',
            variable=self.create_new_var,
            value=True,
            command=self.toggle_mode
        ).grid(row=1, column=0, columnspan=3, sticky='w', padx=10, pady=5)

        # Row 2: New PDF name entry
        ttk.Label(self, text='New PDF name (no .pdf)').grid(
            row=2, column=0, padx=10, pady=5, sticky='w'
        )
        self.entry_new = ttk.Entry(
            self,
            textvariable=self.new_name_var,
            state='disabled'
        )
        self.entry_new.grid(row=2, column=1, columnspan=2, sticky='ew', padx=10, pady=5)

        # Row 3: Action button
        ttk.Button(
            self,
            text='Create',
            command=self.on_create,
            style='primary.Outline.TButton'
        ).grid(row=3, column=1, pady=10)

        # Row 3: Cancel button
        ttk.Button(
            self,
            text='Cancel',
            command=self.on_cancel,
            style='danger.TButton'
        ).grid(row=3, column=2, pady=10)

    def on_browse(self):
        '''Open a file dialog to select a PDF.'''
        # TODO: implement file selection
        pass

    def toggle_mode(self):
        '''Enable new-name entry when creating new file.'''
        if self.create_new_var.get():
            self.entry_new.config(state='normal')
        else:
            self.entry_new.config(state='disabled')

    def on_create(self):
        '''Create a new PDF or append to selected file.'''
        # TODO: implement create/append logic
        pass

    def on_cancel(self):
        '''Close the application without action.'''
        self.master.destroy()

