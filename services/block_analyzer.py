import os
import re
from collections import Counter

class BlockAnalyzer:
    patron_nombre_carpetas = re.compile(r"^C\d{1,2}_B\d+_R\d{1,2}$", re.IGNORECASE)
    patron_copy = re.compile(r"^copy(?:\d*)\.txt$", re.IGNORECASE)
    patron_data = re.compile(r"^data(?:\d*)\.txt$", re.IGNORECASE)
    patron_cover = re.compile(r"^C\d{1,2}_B\d+_R\d{1,2}-cover\.(jpg|jpeg|png)$", re.IGNORECASE)
    patron_video = re.compile(r"^C\d{1,2}_B\d+_R\d{1,2}\.mp4$", re.IGNORECASE)

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
        contador = Counter(archivos)

        txt_files = [f for f in archivos if f.lower().endswith('.txt')]
        copy_files = [f for f in txt_files if self.patron_copy.match(f)]
        data_files = [f for f in txt_files if self.patron_data.match(f)]
        invalid_txt = [f for f in txt_files if not (self.patron_copy.match(f) or self.patron_data.match(f))]

        tiene_copy = len(copy_files) > 0
        subdirs = [d for d in archivos if os.path.isdir(os.path.join(ruta_r, d))]

        tiene_data = len(data_files) > 0

        errores = []

        if not subdirs:
            return ["Falta carpeta interna con portada y video"]

        asset_dirs = [d for d in subdirs if self.patron_nombre_carpetas.match(d)]
        if not asset_dirs:
            errores.append("Falta carpeta interna con formato Cx_Bx_Rx")
            nombre_assets = None
        elif len(asset_dirs) > 1:
            errores.append(f"Más de una carpeta interna Cx_Bx_Rx encontrada: {asset_dirs}")
            nombre_assets = asset_dirs[0]
        else:
            nombre_assets = asset_dirs[0]

        if nombre_assets is None:
            return errores

        if not self.patron_nombre_carpetas.match(nombre_assets):
            errores.append("Nombre inválido debe tener formato C01_B1_R01")

        path_assets = os.path.join(ruta_r, nombre_assets)
        files_assets = os.listdir(path_assets)

        videos = [f for f in files_assets if f.lower().endswith(".mp4")]
        imgs = [f for f in files_assets if f.lower().endswith((".jpg", ".jpeg", ".png"))]

        invalid_assets_videos = [f for f in files_assets if f.lower().endswith('.mp4') and not self.patron_video.match(f)]
        invalid_assets_images = [f for f in files_assets if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not self.patron_cover.match(f)]
 
        if not videos:
            errores.append("Sin video con formato Cx_Bx_Rx.mp4")
        if len(videos) > 1:
            errores.append("Doble versión de video")
        if invalid_assets_videos:
            errores.append(f"Videos con nombre inválido: {invalid_assets_videos}")
        if not imgs:
            errores.append("Sin portada con formato Cx_Bx_Rx-cover.jpg")
        if len(imgs) > 1:
            errores.append("Múltiples portadas")
        if invalid_assets_images:
            errores.append(f"Imágenes con nombre inválido: {invalid_assets_images}")
        if invalid_txt:
            errores.append(f"TXT con nombre inválido: {invalid_txt}")
        if not tiene_copy:
            errores.append("Sin copy (copyX.txt)")
        if len(copy_files) > 1:
            errores.append("Múltiples archivos copy")
        if not tiene_data:
            errores.append("Sin data (dataX.txt)")
        if len(data_files) > 1:
            errores.append("Múltiples archivos data")
        return errores
