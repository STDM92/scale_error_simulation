import os
import pathlib
import tempfile
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory, askopenfilename

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Messagebox
from PyPDF2 import PdfReader, PdfWriter

import config as cfg
import utils.util_functions as utils


class Application(tk.Tk):
    """
    Main application window for the Strap Weight Simulation GUI.
    """
    def __init__(self, fig):
        super().__init__()
        self.title('Strap Weight Simulation')
        self.style = Style('darkly')
        self.geometry('900x600')
        # Fix horizontal size, allow vertical resizing
        self.resizable(width=False, height=True)

        # Store the Matplotlib figure
        self.fig = fig

        # Create and pack the file browser frame
        browser = FileBrowser(self)
        browser.pack(fill='both', expand=True)


class FileBrowser(ttk.Frame):
    """
    Frame containing controls for loading/saving PDFs and displaying
    a scrollable Matplotlib figure.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # ---------------------------------------------------------------------
        # Application variables
        # ---------------------------------------------------------------------
        base_path = pathlib.Path().absolute() / "figures"
        self.start_path_var = tk.StringVar(value=str(base_path))
        self.existing_pdf_path_var = tk.StringVar()
        self.create_dir_var = tk.StringVar()
        self.new_pdf_name_var = tk.StringVar()
        self.decision_var = tk.StringVar(value='extend')

        # Simulation config options
        self.config_names = utils.gather_config_names(cfg)

        # ---------------------------------------------------------------------
        # Grid layout configuration
        # ---------------------------------------------------------------------
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        # ---------------------------------------------------------------------
        # Notebook tabs: Results (figure) and Save (PDF controls)
        # ---------------------------------------------------------------------
        self._build_notebook()

    def _build_notebook(self):
        # Create Notebook
        nb = ttk.Notebook(self)
        nb.grid(row=2, column=0, sticky='nsew', padx=0, pady=0)

        # Tabs
        tab_results = ttk.Frame(nb)
        tab_save = ttk.Frame(nb)
        nb.add(tab_results, text='Results')
        nb.add(tab_save, text='Save')

        # Make Results tab expandable for figure
        tab_results.rowconfigure(0, weight=1)
        tab_results.columnconfigure(0, weight=1)
        self._tab_results = tab_results

        # Build contents
        self._build_scrollable_figure(tab_results)
        self._build_save_controls(tab_save)

        # Handle tab change for toolbar
        nb.bind('<<NotebookTabChanged>>', self._on_tab_changed)

    def _build_scrollable_figure(self, parent):
        """
        Creates a scrollable canvas area and embeds the Matplotlib Figure.
        """
        # Container for scrollable area
        container = ttk.Frame(parent)
        container.grid(row=0, column=0, sticky='nsew')

        # Canvas + vertical scrollbar
        canvas = tk.Canvas(container)
        v_scroll = ttk.Scrollbar(
            container,
            orient='vertical',
            command=canvas.yview,
            bootstyle="primary-round"
        )
        canvas.configure(yscrollcommand=v_scroll.set)

        # ─── Mouse-wheel support ───
        def _on_mousewheel(event):
            # Windows / macOS
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        def _on_mousewheel_linux(event):
            # Linux: Button-4 = up, Button-5 = down
            if event.num == 4:
                canvas.yview_scroll(-1, 'units')
            elif event.num == 5:
                canvas.yview_scroll(1, 'units')

        # Bind wheel events to canvas
        canvas.bind_all('<MouseWheel>', _on_mousewheel)
        canvas.bind_all('<Button-4>', _on_mousewheel_linux)
        canvas.bind_all('<Button-5>', _on_mousewheel_linux)
        # ───────────────────────────



        # Layout canvas and scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')

        # Inner frame inside the canvas
        inner = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner, anchor='nw')
        inner.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        # Embed the figure
        self.figure_canvas = FigureCanvasTkAgg(self.master.fig, master=inner)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().pack(fill='both', expand=True)

        # Prepare toolbar (initially hidden)
        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, inner)
        self.toolbar.update()
        self.toolbar.pack_forget()

    def _build_save_controls(self, parent):
        """
        Builds the controls for creating or extending PDF files,
        faithfully mirroring the original layout and functionality.
        """
        # Ensure frame expands horizontally
        parent.columnconfigure(0, weight=1)

        # Decision frame
        decision_frame = ttk.Labelframe(
            parent,
            text='Extend an existing or create a new PDF',
            padding=(20, 10, 10, 5)
        )
        decision_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        decision_frame.columnconfigure(1, weight=1)

        # Radio selection
        ttk.Label(decision_frame, text='Selection').grid(row=0, column=0, padx=10, pady=2, sticky='w')
        option_frame = ttk.Frame(decision_frame, padding=(15, 10, 0, 10))
        option_frame.grid(row=0, column=1, columnspan=2, sticky='w')
        ttk.Radiobutton(
            option_frame,
            text='Extend Existing',
            variable=self.decision_var,
            value='extend',
            command=self._show_extend
        ).pack(side='left', padx=10)
        ttk.Radiobutton(
            option_frame,
            text='Create New',
            variable=self.decision_var,
            value='create',
            command=self._show_create
        ).pack(side='left', padx=10)

        # Extend existing PDF section
        self.extend_frame = ttk.Labelframe(parent, text='Extend Existing PDF', padding=(40, 10, 10, 5))
        self.extend_frame.grid(row=1, column=0, padx=10, pady=2, sticky='ew')
        self.extend_frame.columnconfigure(1, weight=1)
        # Path row
        ttk.Label(self.extend_frame, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='e')
        ttk.Entry(
            self.extend_frame,
            textvariable=self.existing_pdf_path_var,
            width=80
        ).grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        ttk.Button(
            self.extend_frame,
            text='Browse',
            command=self._browse_existing,
            style='primary.TButton'
        ).grid(row=0, column=2, sticky='ew', pady=2, padx=10)
        # Figure name + Create
        ttk.Label(self.extend_frame, text='Figure Name').grid(row=1, column=0, padx=10, pady=2, sticky='e')
        ttk.Entry(
            self.extend_frame,
            width=80
        ).grid(row=1, column=1, sticky='ew', padx=10, pady=2)
        ttk.Button(
            self.extend_frame,
            text='Create',
            command=self._export_to_pdf,
            style='primary.Outline.TButton'
        ).grid(row=1, column=2, sticky='ew', pady=2, padx=10)

        # Create new PDF section
        self.create_frame = ttk.Labelframe(parent, text='Create new PDF', padding=(40, 10, 10, 5))
        self.create_frame.grid(row=2, column=0, padx=10, pady=2, sticky='ew')
        self.create_frame.columnconfigure(1, weight=1)
        # Path row
        ttk.Label(self.create_frame, text='Path').grid(row=0, column=0, padx=10, pady=2, sticky='e')
        ttk.Entry(
            self.create_frame,
            textvariable=self.create_dir_var,
            width=80
        ).grid(row=0, column=1, sticky='ew', padx=10, pady=2)
        ttk.Button(
            self.create_frame,
            text='Browse',
            command=self._browse_create_dir,
            style='primary.TButton'
        ).grid(row=0, column=2, sticky='ew', pady=2, padx=10)
        # PDF name
        ttk.Label(self.create_frame, text='PDF Name').grid(row=1, column=0, padx=10, pady=2, sticky='e')
        ttk.Entry(
            self.create_frame,
            textvariable=self.new_pdf_name_var,
            width=80
        ).grid(row=1, column=1, sticky='ew', padx=10, pady=2)
        ttk.Button(
            self.create_frame,
            text='Create',
            command=self._export_to_pdf,
            style='primary.Outline.TButton'
        ).grid(row=1, column=2, sticky='ew', pady=2, padx=10)
        # Figure name
        ttk.Label(self.create_frame, text='Figure Name').grid(row=2, column=0, padx=10, pady=2, sticky='e')
        ttk.Entry(
            self.create_frame,
            width=80
        ).grid(row=2, column=1, sticky='ew', padx=10, pady=2)

        # Initially show only extend
        self._show_extend()

    def _show_extend(self):
        self.extend_frame.lift()
        self.create_frame.lower()

    def _show_create(self):
        self.create_frame.lift()
        self.extend_frame.lower()

    def _browse_existing(self):
        path = askopenfilename(
            title="Select existing PDF",
            initialdir=self.start_path_var.get(),
            filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.existing_pdf_path_var.set(path)

    def _browse_create_dir(self):
        folder = askdirectory(
            title="Select output folder",
            initialdir=self.start_path_var.get()
        )
        if folder:
            self.create_dir_var.set(folder)

    def _export_to_pdf(self):
        """
        Exports the current Matplotlib figure to PDF, either extending an
        existing file or creating a new one.
        """
        mode = self.decision_var.get()
        if mode == 'extend':
            target = self.existing_pdf_path_var.get().strip()
            if not target:
                Messagebox.show_error("Select an existing PDF first.")
                return
        else:
            folder = self.create_dir_var.get().strip()
            name = self.new_pdf_name_var.get().strip()
            if not folder or not name:
                Messagebox.show_error("Choose a folder and enter a new PDF name.")
                return
            os.makedirs(folder, exist_ok=True)
            target = os.path.join(folder, f"{name}.pdf")

        # Add title and underline
        title_text = os.path.splitext(os.path.basename(target))[0]
        if title_text:
            txt = self.master.fig.suptitle(
                title_text,
                x=0.5, y=0.98,
                horizontalalignment='center',
                fontsize=16, fontweight='bold'
            )
            import matplotlib.lines as mlines
            underline = mlines.Line2D([0.1, 0.9], [0.96, 0.96],
                                      transform=self.master.fig.transFigure,
                                      color=txt.get_color(), linewidth=1)
            self.master.fig.add_artist(underline)

        # Save and merge
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        self.master.fig.savefig(tmp.name)
        writer = PdfWriter()
        if os.path.exists(target):
            for p in PdfReader(target).pages:
                writer.add_page(p)
        for p in PdfReader(tmp.name).pages:
            writer.add_page(p)
        with open(target, 'wb') as f:
            writer.write(f)
        os.remove(tmp.name)

        Messagebox.show_info("Saved to PDF")
        self.master.destroy()

    def _on_tab_changed(self, event):
        """
        Show or hide the Matplotlib toolbar when switching tabs.
        """
        notebook = event.widget
        tab_text = notebook.tab(notebook.select(), 'text')
        if tab_text == 'Results':
            self.toolbar.pack(side='bottom', fill='x')
        else:
            self.toolbar.pack_forget()


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.plot([0, 1, 2], [10, 20, 30])
    app = Application(fig)
    app.mainloop()
