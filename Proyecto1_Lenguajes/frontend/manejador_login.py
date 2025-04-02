import json
import subprocess
import time

def verificar_usuario(email, password):
    """ Guarda las credenciales en un JSON, ejecuta OCaml y espera la respuesta """

    # Guardar las credenciales en un archivo temporal
    credenciales = {"email": email, "password": password}
    with open("credenciales.json", "w") as file:
        json.dump(credenciales, file)

    # Ejecutar el backend de OCaml como subproceso
    try:
        subprocess.run(["backend_ocaml/verificador"], timeout=5)  # Tiempo límite de 5 segundos
    except subprocess.TimeoutExpired:
        return None, "Error: Tiempo de espera excedido."

    # Leer la respuesta del backend
    try:
        with open("respuesta.json", "r") as file:
            respuesta = json.load(file)
        if respuesta.get("success"):
            return respuesta["partner"], None
        else:
            return None, "Usuario o contraseña incorrectos."
    except FileNotFoundError:
        return None, "Error: No se encontró el archivo de respuesta."
