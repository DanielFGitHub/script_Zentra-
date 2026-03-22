import os

class FolderCreator:
    def crear_estructura(self, ruta_drive, nombre_ciclo, bloques):
        ruta_ciclo = os.path.join(ruta_drive, nombre_ciclo)

        for nombre_bloque, piezas in bloques:
            for i in range(1, piezas + 1):
                folder = os.path.join(ruta_ciclo, nombre_bloque, f"R{str(i).zfill(2)}")
                os.makedirs(folder, exist_ok=True)

        return True