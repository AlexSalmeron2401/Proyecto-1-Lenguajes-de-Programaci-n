import json
import os

def crearArchivoJson():
    usuarios_iniciales = {
        "users": [
            {"email": "admin@escuela.edu", "password": "admin123", "partner": "admin"},
            {"email": "user@escuela.edu", "password": "user123", "partner": "visor"}
        ]
    }

    # Definir la ruta donde se guardará el archivo
    ruta = r"C:\Users\alexj\OneDrive\Documentos\Proyecto1_Lenguajes\usuarios.json"

    # Crear la carpeta si no existe
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    # Guardar el archivo JSON en la ruta definida
    with open(ruta, "w") as file:
        json.dump(usuarios_iniciales, file, indent=4)

#crearArchivoJson()
