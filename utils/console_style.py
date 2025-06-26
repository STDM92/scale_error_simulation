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

