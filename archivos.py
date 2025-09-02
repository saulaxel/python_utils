import os


def quitar_extension(nombre_archivo: str) -> str:
    return os.path.splitext(nombre_archivo)[0]


def nombre_base(ruta_archivo: str) -> str:
    return os.path.basename(ruta_archivo)
