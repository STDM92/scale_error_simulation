"""
    Author: Israel Dryer
    Modified: 2021-04-09
    Adapted for ttkbootstrap from: https://github.com/israel-dryer/File-Search-Engine-Tk
"""
import os
import pathlib
import tkinter
from queue import Queue
from threading import Thread
from tkinter import ttk
from tkinter.filedialog import askdirectory, asksaveasfilename, askopenfilename

from ttkbootstrap import Style


class Application(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title('Strap Weight Simulation')
        self.style = Style('darkly')
        self.resizable(width=False, height=False)
        self.search = SearchEngine(self, padding=10)
        self.search.pack(fill='both', expand='no')


class SearchEngine(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # application variables

        self.start_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()) + r"\figures")
        self.search_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()) + r"\figures")
        self.existing_pdf_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()) + r"\figures")
        self.search_term_var = tkinter.StringVar(value='txt')
        self.decision_var = tkinter.StringVar(value='extend')
        self.search_count = 0

        # container for decision-making new pdf or extend existing pdf
        decision_labelframe = ttk.Labelframe(self, text='Extend an existing or create a new PDF', padding=(20, 10, 10, 5))
        decision_labelframe.pack(side='top', fill='x')
        decision_labelframe.pack_propagate(False)
        decision_labelframe.columnconfigure(1, weight=1)

        # decision-making
        ttk.Label(decision_labelframe, text='Selection').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        option_frame = ttk.Frame(decision_labelframe, padding=(15, 10, 0, 10))
        option_frame.grid(row=0, column=1, columnspan=2, sticky='ew')

        r1 = ttk.Radiobutton(option_frame, text='Extend Existing', variable=self.decision_var, value='extend', command=self.enable_extend_pdf)
        r1.pack(side='left', fill='x', pady=2, padx=10)

        r2 = ttk.Radiobutton(option_frame, text='Create New', variable=self.decision_var, value='create', command=self.enable_create_pdf)
        r2.pack(side='left', fill='x', pady=2, padx=10)


        # container extend exsiting
        self.input_labelframe = ttk.Labelframe(self, text='Extend Existing PDF', padding=(40, 10, 10, 5))
        self.input_labelframe.pack(side='top', fill='x', pady=10)
        self.input_labelframe.columnconfigure(1, weight=1)

        # select document input
        ttk.Label(self.input_labelframe, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e1 = ttk.Entry(self.input_labelframe, textvariable=self.existing_pdf_path_var, width=80)
        e1.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b1 = ttk.Button(self.input_labelframe, text='Browse', command=self.browse_pdf, style='primary.TButton')
        b1.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)

        # figure name input
        ttk.Label(self.input_labelframe, text='Figure Name').grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        e2 = ttk.Entry(self.input_labelframe, width=80)
        e2.grid(row=1, column=1, sticky='ew', padx=10, pady=2)
        b2 = ttk.Button(self.input_labelframe, text='Create', command="", style='primary.Outline.TButton')
        b2.grid(row=1, column=2, sticky='ew', pady=2)

        # container create new
        self.create_new_labelframe = ttk.Labelframe(self, text='Create new PDF', padding=(40, 10, 10, 5))
        self.create_new_labelframe.pack(side='top', fill='x', pady=10)
        self.create_new_labelframe.columnconfigure(1, weight=1)

        # select document input
        ttk.Label(self.create_new_labelframe, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e3 = ttk.Entry(self.create_new_labelframe, textvariable=self.search_path_var, width=80)
        e3.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        b3 = ttk.Button(self.create_new_labelframe, text='Browse', command="", style='primary.TButton')
        b3.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)

        # pdf name input
        ttk.Label(self.create_new_labelframe, text='Figure Name').grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        e4 = ttk.Entry(self.create_new_labelframe, width=80)
        e4.grid(row=1, column=1, sticky='ew', padx=10, pady=2)
        b4 = ttk.Button(self.create_new_labelframe, text='Create', command="", style='primary.Outline.TButton')
        b4.grid(row=1, column=2, sticky='ew', pady=2)
        # figure name input
        ttk.Label(self.create_new_labelframe, text='Figure Name').grid(row=2, column=0, padx=10, pady=2, sticky='ew')
        e5 = ttk.Entry(self.create_new_labelframe)
        e5.grid(row=2, column=1, sticky='ew', padx=10, pady=2)


        self.create_new_labelframe.pack_forget()



    def enable_extend_pdf(self):
        self.input_labelframe.pack(side='top', fill='x', pady=10)
        self.create_new_labelframe.pack_forget()

    def enable_create_pdf(self):
        self.input_labelframe.pack_forget()
        self.create_new_labelframe.pack(side='top', fill='x', pady=10)

    def browse_pdf(self):
        """
        Open a file dialog to pick an existing PDF and store its path.
        Falls back to cwd if no figures_dir is set on the master.
        """
        start_dir = self.start_path_var.get()
        path = askopenfilename(
            title="Select existing PDF to append",
            initialdir=start_dir,
            filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.existing_pdf_path_var.set(path)

if __name__ == '__main__':
    file_queue = Queue()
    searching = False
    Application().mainloop()