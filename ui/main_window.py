import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from ui.tab_crear import TabCrear
from ui.tab_analizar import TabAnalizar


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contenido - Drive Escritorio")
        self.root.geometry("700x700")

        # Variable global compartida
        self.ruta_drive_pc = tk.StringVar()

        # Frame superior (configuración global)
        self.setup_global_config()

        # Notebook con pestañas
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=1, fill="both")

        # Crear pestañas
        self.tab_crear = TabCrear(self)
        self.tab_analizar = TabAnalizar(self)

        # Añadir al notebook
        self.tabs.add(self.tab_crear.frame, text="1. Crear Estructura")
        self.tabs.add(self.tab_analizar.frame, text="2. Analizar Bloque")

    def setup_global_config(self):
        frame_top = tk.LabelFrame(self.root, text=" Configuración Global ", padx=10, pady=10)
        frame_top.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_top, text="Ruta de Google Drive en PC:").pack(side="left")
        tk.Entry(frame_top, textvariable=self.ruta_drive_pc, width=40).pack(side="left", padx=5)
        tk.Button(frame_top, text="Buscar...", command=self.seleccionar_ruta_global).pack(side="left")

    def seleccionar_ruta_global(self):
        ruta = filedialog.askdirectory()
        if ruta:
            self.ruta_drive_pc.set(ruta)