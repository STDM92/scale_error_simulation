import os
import tempfile
import tkinter.filedialog as filedialog
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox
from PyPDF2 import PdfReader, PdfWriter
import matplotlib.lines as mlines


# utils/console_style.py
BOLD      = "\033[1m"
RED       = "\033[31m"
CYAN      = "\033[36m"
RESET_ALL = "\033[0m"




def add_plot_to_pdf_bootstrap(fig, figures_dir="figures"):
    """
    Display a single GUI window for selecting/creating a PDF and entering a page title,
    then append the Matplotlib figure as a new page.
    Uses ttkbootstrap with the 'darkly' theme for a modern look.
    """
    # Initialize darkly theme
    style = tb.Style(theme="darkly")

    # Main window
        # Initialize ttkbootstrap style and main window
    style = tb.Style(theme="darkly")
    root = tb.Window(
        title="Append Plot to PDF",
        themename="darkly",
        size=(500, 250),
        resizable=(False, False)
    )

    # Variables to hold user input
    pdf_path_var = tb.StringVar()
    new_name_var = tb.StringVar()
    title_var    = tb.StringVar()

    # Browse button callback
    def browse_file():
        path = filedialog.askopenfilename(
            title="Select PDF to append (Cancel to create new)",
            initialdir=figures_dir,
            filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            pdf_path_var.set(path)

    # OK button callback
    def on_ok():
        pdf_path = pdf_path_var.get().strip()
        new_name = new_name_var.get().strip()
        page_title = title_var.get().strip()

        # Determine target file
        if not pdf_path and new_name:
            os.makedirs(figures_dir, exist_ok=True)
            pdf_path = os.path.join(figures_dir, f"{new_name}.pdf")
        elif not pdf_path:
            Messagebox.show_error("No PDF selected or name entered.", parent=root)
            return

        # Apply title if provided
        if page_title:
            txt = fig.suptitle(
                page_title,
                x=0.01,
                y=0.98,
                horizontalalignment="left",
                fontsize=20,
                fontweight="bold"
            )
            underline = mlines.Line2D([
                0.01, 0.99
            ], [0.96, 0.96], transform=fig.transFigure,
                color=txt.get_color(), linewidth=1
            )
            fig.add_artist(underline)

        # Save figure to temp PDF
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp_path = tmp.name; tmp.close()
        fig.savefig(tmp_path)

        # Merge into target PDF
        writer = PdfWriter()
        if os.path.exists(pdf_path):
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        new_reader = PdfReader(tmp_path)
        writer.add_page(new_reader.pages[0])

        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        with open(pdf_path, "wb") as f_out:
            writer.write(f_out)
        os.remove(tmp_path)

        Messagebox.show_info(f"✅ Saved plot page to {pdf_path}", parent=root)
        root.destroy()

    # Cancel callback
    def on_cancel():
        root.destroy()

    # Layout widgets
    padding = dict(padx=15, pady=8)
    tb.Label(root, text="PDF to append:", font=('Helvetica', 10, 'bold')).pack(fill='x', **padding)
    frame = tb.Frame(root)
    frame.pack(fill='x', **padding)
    tb.Entry(frame, textvariable=pdf_path_var, width=40).pack(side='left')
    tb.Button(frame, text="Browse...", command=browse_file).pack(side='left', padx=(5,0))

    tb.Label(root, text="Or new PDF name (no .pdf):", font=('Helvetica', 10, 'bold')).pack(fill='x', **padding)
    tb.Entry(root, textvariable=new_name_var, width=50).pack(**padding)

    tb.Label(root, text="Page title (optional):", font=('Helvetica', 10, 'bold')).pack(fill='x', **padding)
    tb.Entry(root, textvariable=title_var, width=50).pack(**padding)

    btn_frame = tb.Frame(root)
    btn_frame.pack(pady=15)
    tb.Button(btn_frame, text="OK", bootstyle="success", command=on_ok).pack(side='left', padx=10)
    tb.Button(btn_frame, text="Cancel", bootstyle="danger", command=on_cancel).pack(side='left', padx=10)

    # Start event loop
    root.mainloop()