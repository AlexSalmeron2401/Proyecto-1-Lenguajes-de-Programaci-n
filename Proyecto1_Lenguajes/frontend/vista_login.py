import subprocess
import json
import os
from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel,
    QMessageBox
)

# Importamos las ventanas de administración y visor desde sus módulos
from frontend.vista_admins import VentanaPrincipalAdmin
from frontend.vista_visores import VentanaPrincipalVisor

class VentanaLogin(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        
        self.email_label = QLabel("Correo electrónico:")
        self.email_input = QLineEdit()
        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.clicked.connect(self.login)
        
        layout = QVBoxLayout()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)
    
    def login(self):
        # Obtener y limpiar las credenciales
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        # Guardar las credenciales en data/credenciales.json
        self.guardar_credenciales(email, password)
        
        # Ejecutar el binario OCaml y obtener el partner
        partner = self.ejecutar_ocaml()
        
        if partner:
            if partner.lower() == "admin":
                self.ventana_principal = VentanaPrincipalAdmin(partner)
            elif partner.lower() == "visor":
                self.ventana_principal = VentanaPrincipalVisor()
            else:
                QMessageBox.warning(self, "Error", f"Partner desconocido: {partner}")
                return
            
            self.ventana_principal.show()
            self.close()  # Cierra la ventana de login
        else:
            QMessageBox.warning(self, "Error", "Login fallido: credenciales incorrectas.")    
    def guardar_credenciales(self, email, password):
        os.makedirs("data", exist_ok=True)
        data = {
            "users": [
                {"email": email, "password": password}
            ]
        }
        with open("data/credenciales.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def ejecutar_ocaml(self):
        try:
            # Construir la ruta absoluta al ejecutable OCaml compilado
            ruta_backend = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
            ejecutable = os.path.join(ruta_backend, "verificar_credenciales")
            
            # Ejecutar el binario y capturar la salida
            result = subprocess.run([ejecutable], capture_output=True, text=True)
            if result.returncode != 0:
                print("Error al ejecutar OCaml:")
                print(result.stderr)
                return None
            else:
                output = result.stdout
                #print("Salida de OCaml:") Linea de control para visualizar que sale desde ocaml
                #print(output) Linea de control para visualizar que sale desde ocaml
                # Buscar la línea que contenga "Partner:" y extraer el valor
                partner = None
                for line in output.splitlines():
                    if line.startswith("Partner:"):
                        partner = line.split("Partner:")[1].strip()
                        break
                return partner
        except Exception as e:
            print(f"Error al ejecutar OCaml: {e}")
            return None
