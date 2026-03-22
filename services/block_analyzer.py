import os
import re


class BlockAnalyzer:
    patron_regex = re.compile(r"^C\d{2}_B\d+_R\d{2}")
    data = "data.txt"

    def analizar(self, ruta_bloque):
        reporte = []

        subcarpetas = sorted([
            f for f in os.listdir(ruta_bloque)
            if os.path.isdir(os.path.join(ruta_bloque, f))
        ])

        for carpeta_r in subcarpetas:
            errores = self.analizar_R(os.path.join(ruta_bloque, carpeta_r))
            reporte.append((carpeta_r, errores))

        return reporte

    def analizar_R(self, ruta_r):
        archivos = os.listdir(ruta_r)

        tiene_copy = any(f.lower().endswith(".txt") for f in archivos)
        subdirs = [d for d in archivos if os.path.isdir(os.path.join(ruta_r, d))]

        tiene_data = "data.txt" in (f.lower() for f in archivos)
            

        if not subdirs:
            return ["Falta carpeta interna"]

        nombre_assets = subdirs[0]
        errores = []

        if not self.patron_regex.match(nombre_assets):
            errores.append("Nombre inválido debe tener formato C01_B1_R01")

        path_assets = os.path.join(ruta_r, nombre_assets)
        files_assets = os.listdir(path_assets)

        videos = [f for f in files_assets if f.lower().endswith(".mp4")]
        imgs = [f for f in files_assets if f.lower().endswith((".jpg", ".jpeg", ".png"))]

        if not videos:
            errores.append("Sin video (.mp4)")
        if len(videos) > 1:
            errores.append("Doble versión")
        if not imgs:
            errores.append("Sin portada (.jpg)")
        if not tiene_copy:
            errores.append("Sin copy (.txt)")
        if not tiene_data:
            errores.append("Sin data")

        return errores