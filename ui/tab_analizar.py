import tkinter as tk
from tkinter import filedialog

from services.block_analyzer import BlockAnalyzer


class TabAnalizar:
    def __init__(self, main_window):
        self.main = main_window
        self.frame = tk.Frame(main_window.tabs)

        self.analyzer = BlockAnalyzer()

        self.setup_ui()

    def setup_ui(self):
        container = tk.Frame(self.frame, padx=20, pady=20)
        container.pack(fill="both")

        tk.Button(container, text="Seleccionar Bloque a Analizar",
                  command=self.analizar, bg="lightcyan").pack(pady=10)

        self.txt_reporte = tk.Text(self.frame, height=25, width=80, font=("Consolas", 9))
        self.txt_reporte.pack(padx=10, pady=10)

    def analizar(self):
        ruta = filedialog.askdirectory(title="Selecciona la carpeta del Bloque")
        if not ruta:
            return

        self.txt_reporte.delete("1.0", tk.END)
        self.txt_reporte.insert(tk.END, f"ANALIZANDO BLOQUE: {ruta}\n")
        self.txt_reporte.insert(tk.END, "=" * 65 + "\n")

        resultados = self.analyzer.analizar(ruta)

        for carpeta, errores in resultados:
            if not errores:
                self.txt_reporte.insert(tk.END, f"{carpeta}: ✅ Listo para programar\n")
            else:
                self.txt_reporte.insert(tk.END, f"{carpeta}: ❌ {' | '.join(errores)}\n")