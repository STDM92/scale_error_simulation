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
import tempfile
from ttkbootstrap.dialogs import Messagebox
from PyPDF2 import PdfReader, PdfWriter


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
        #region application variables

        self.start_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()) + r"\figures")
        self.search_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()) + r"\figures")
        self.existing_pdf_path_var = tkinter.StringVar(value=str(pathlib.Path().absolute()) + r"\figures")
        self.search_term_var = tkinter.StringVar(value='txt')
        self.decision_var = tkinter.StringVar(value='extend')
        self.search_count = 0
        self.existing_pdf_path_var = tkinter.StringVar()
        self.create_dir_var = tkinter.StringVar()
        self.new_pdf_name_var = tkinter.StringVar()
        self.decision_var = tkinter.StringVar(value='extend')
        #endregion


        #region decision-making GUI elements


        decision_labelframe = ttk.Labelframe(self, text='Extend an existing or create a new PDF', padding=(20, 10, 10, 5))
        decision_labelframe.pack(side='top', fill='x')
        decision_labelframe.pack_propagate(False)
        decision_labelframe.columnconfigure(1, weight=1)


        ttk.Label(decision_labelframe, text='Selection').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        option_frame = ttk.Frame(decision_labelframe, padding=(15, 10, 0, 10))
        option_frame.grid(row=0, column=1, columnspan=2, sticky='ew')

        r1 = ttk.Radiobutton(option_frame, text='Extend Existing', variable=self.decision_var, value='extend', command=self.enable_extend_pdf)
        r1.pack(side='left', fill='x', pady=2, padx=10)

        r2 = ttk.Radiobutton(option_frame, text='Create New', variable=self.decision_var, value='create', command=self.enable_create_pdf)
        r2.pack(side='left', fill='x', pady=2, padx=10)
        #endregion


        # region extend existing PDF GUI elements
        self.input_labelframe = ttk.Labelframe(self, text='Extend Existing PDF', padding=(40, 10, 10, 5))
        self.input_labelframe.pack(side='top', fill='x', pady=10)
        self.input_labelframe.columnconfigure(1, weight=1)

        ttk.Label(self.input_labelframe, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e1 = ttk.Entry(self.input_labelframe, textvariable=self.existing_pdf_path_var, width=80)
        e1.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        e2 = ttk.Entry(self.input_labelframe, width=80)
        e2.grid(row=1, column=1, sticky='ew', padx=10, pady=2)

        b1 = ttk.Button(self.input_labelframe, text='Browse', command=self.browse_existing, style='primary.TButton')
        b1.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)
        b2 = ttk.Button(self.input_labelframe, text='Create', command=self.on_create, style='primary.Outline.TButton')
        b2.grid(row=1, column=2, sticky='ew', pady=2)

        ttk.Label(self.input_labelframe, text='Figure Name').grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        #endregion


        # region create new pdf GUi elements
        self.create_new_labelframe = ttk.Labelframe(self, text='Create new PDF', padding=(40, 10, 10, 5))
        self.create_new_labelframe.pack(side='top', fill='x', pady=10)
        self.create_new_labelframe.columnconfigure(1, weight=1)


        ttk.Label(self.create_new_labelframe, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='ew')
        e3 = ttk.Entry(self.create_new_labelframe, textvariable=self.create_dir_var, width=80)
        e3.grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        e4 = ttk.Entry(self.create_new_labelframe, textvariable=self.new_pdf_name_var, width=80)
        e4.grid(row=1, column=1, sticky='ew', padx=10, pady=2)
        e5 = ttk.Entry(self.create_new_labelframe)
        e5.grid(row=2, column=1, sticky='ew', padx=10, pady=2)

        b3 = ttk.Button(self.create_new_labelframe, text='Browse', command=self.browse_create_dir, style='primary.TButton')
        b3.grid(row=0, column=2, sticky='ew', pady=2, ipadx=10)
        b4 = ttk.Button(self.create_new_labelframe, text='Create', command=self.on_create, style='primary.Outline.TButton')
        b4.grid(row=1, column=2, sticky='ew', pady=2)

        ttk.Label(self.create_new_labelframe, text='PDF Name').grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        ttk.Label(self.create_new_labelframe, text='Figure Name').grid(row=2, column=0, padx=10, pady=2, sticky='ew')


        self.create_new_labelframe.pack_forget()
        # endregion


    def enable_extend_pdf(self):
        self.input_labelframe.pack(side='top', fill='x', pady=10)
        self.create_new_labelframe.pack_forget()

    def enable_create_pdf(self):
        self.input_labelframe.pack_forget()
        self.create_new_labelframe.pack(side='top', fill='x', pady=10)

    def browse_existing(self):
        """Browse for an existing PDF to append to."""
        start = self.start_path_var.get()
        path = askopenfilename(
            title="Select existing PDF",
            initialdir=start,
            filetypes=[("PDF Files", "*.pdf")],
        )
        if path:
            self.existing_pdf_path_var.set(path)

    def browse_create_dir(self):
        """Browse for the folder where you’ll create a new PDF."""
        start = self.start_path_var.get()
        folder = askdirectory(
            title="Select output folder",
            initialdir=start,
        )
        if folder:
            self.create_dir_var.set(folder)

    def on_create(self):
        """
        Depending on decision_var:
         - 'extend': append current figure to existing_pdf_path_var
         - 'create': create new PDF in create_dir_var / new_pdf_name_var
        """
        mode = self.decision_var.get()
        # Determine target path
        if mode == 'extend':
            target = self.existing_pdf_path_var.get().strip()
            if not target:
                Messagebox.show_error("Select an existing PDF first.", parent=self)
                return
        else:  # create
            folder = self.create_dir_var.get().strip()
            name = self.new_pdf_name_var.get().strip()
            if not folder or not name:
                Messagebox.show_error("Choose a folder and enter a new PDF name.", parent=self)
                return
            os.makedirs(folder, exist_ok=True)
            target = os.path.join(folder, f"{name}.pdf")

        # Export current figure to temp PDF
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp_path = tmp.name; tmp.close()
        self.master.fig.savefig(tmp_path)

        # Merge into target
        writer = PdfWriter()
        if os.path.exists(target):
            for p in PdfReader(target).pages:
                writer.add_page(p)
        for p in PdfReader(tmp_path).pages:
            writer.add_page(p)

        # Write out and cleanup
        with open(target, "wb") as f:
            writer.write(f)
        os.remove(tmp_path)

        Messagebox.show_info(f"✅ Saved to {target}", parent=self)
        self.master.destroy()

if __name__ == '__main__':
    file_queue = Queue()
    searching = False
    Application().mainloop()