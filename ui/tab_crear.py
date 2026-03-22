import tkinter as tk
from tkinter import ttk, messagebox

from services.folder_creator import FolderCreator


class TabCrear:
    def __init__(self, main_window):
        self.main = main_window
        self.frame = ttk.Frame(main_window.tabs)

        self.folder_creator = FolderCreator()

        self.setup_ui()

    def setup_ui(self):
        container = tk.Frame(self.frame, padx=20, pady=20,)
        container.pack(fill="both")

        tk.Label(container, text="Nombre del Ciclo (ej. 26-1):").grid(row=0, column=0, sticky="w")
        self.ent_nombre_ciclo = tk.Entry(container, width=20)
        self.ent_nombre_ciclo.grid(row=0, column=1, pady=5)

        tk.Label(container, text="Número de bloques:").grid(row=1, column=0, sticky="w")
        self.ent_num_bloques = tk.Entry(container, width=10)
        self.ent_num_bloques.grid(row=1, column=1, pady=5)

        tk.Button(container, text="Generar Formulario", command=self.generar_campos_dinamicos).grid(row=2, column=0, columnspan=2, pady=10)

        # Scroll
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def generar_campos_dinamicos(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            n = int(self.ent_num_bloques.get())
        except:
            return

        self.entradas_bloques = []

        for i in range(n):
            f = tk.Frame(self.scrollable_frame, pady=2)
            f.pack(fill="x")

            tk.Label(f, text=f"B{i+1}:").pack(side="left")

            nom = tk.Entry(f, width=15)
            nom.insert(0, f"Bloque {i+1}")
            nom.pack(side="left", padx=5)

            tk.Label(f, text="Piezas:").pack(side="left")

            pz = tk.Entry(f, width=5)
            pz.insert(0, "10")
            pz.pack(side="left", padx=5)

            self.entradas_bloques.append((nom, pz))

        tk.Button(self.scrollable_frame, text="CREAR CARPETAS EN DRIVE", bg="#2ecc71", fg="white",
                  command=self.ejecutar_creacion).pack(pady=20)

    def ejecutar_creacion(self):
        ruta = self.main.ruta_drive_pc.get()

        if not ruta:
            messagebox.showwarning("Error", "Selecciona la ruta de Drive primero")
            return

        nombre_ciclo = self.ent_nombre_ciclo.get()

        bloques = []
        for nom, pz in self.entradas_bloques:
            try:
                bloques.append((nom.get(), int(pz.get())))
            except:
                continue

        try:
            self.folder_creator.crear_estructura(ruta, nombre_ciclo, bloques)
            messagebox.showinfo("Éxito", "Estructura creada correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))