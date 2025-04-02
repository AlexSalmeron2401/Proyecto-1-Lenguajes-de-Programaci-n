import subprocess
import json
import os
from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel,
    QMessageBox, QFormLayout, QHBoxLayout
)

# Importamos las ventanas de administración y visor
from frontend.vista_admins import VentanaPrincipalAdmin
from frontend.vista_visores import VentanaPrincipalVisor

class VentanaLogin(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(400, 300)
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingrese su correo")
        form_layout.addRow("Correo electrónico:", self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Contraseña:", self.password_input)
        
        layout.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.clicked.connect(self.login)
        btn_layout.addWidget(self.login_button)
        
        self.registro_button = QPushButton("Registrarse")
        self.registro_button.clicked.connect(self.abrir_registro)
        btn_layout.addWidget(self.registro_button)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f7f7f7;
            }
            QLabel {
                font-size: 12pt;
                color: #333;
            }
            QLineEdit {
                font-size: 12pt;
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                font-size: 12pt;
                padding: 8px;
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
    
    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        self.guardar_credenciales(email, password)
        
        # Ejecutar OCaml para obtener la información en formato "rol:nombre"
        info = self.ejecutar_ocaml()
        if info:
            # Se espera que info tenga el formato "rol:nombre"
            parts = info.split(":")
            if len(parts) == 2:
                rol, nombre = parts[0].strip(), parts[1].strip()
            else:
                rol = info.strip()
                nombre = ""
            if rol.lower() == "profesor":
                self.ventana_principal = VentanaPrincipalAdmin(nombre)
            elif rol.lower() == "estudiante":
                self.ventana_principal = VentanaPrincipalVisor(nombre)
            else:
                QMessageBox.warning(self, "Error", f"Rol desconocido: {rol}")
                return
            
            self.ventana_principal.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Login fallido: credenciales incorrectas.")
    
    def guardar_credenciales(self, email, password):
        os.makedirs("data", exist_ok=True)
        data = {"users": [{"email": email, "password": password}]}
        with open("data/credenciales.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def ejecutar_ocaml(self):
        try:
            ruta_backend = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
            ejecutable = os.path.join(ruta_backend, "verificar_credenciales")
            
            result = subprocess.run([ejecutable], capture_output=True, text=True)
            if result.returncode != 0:
                print("Error al ejecutar OCaml:")
                print(result.stderr)
                return None
            else:
                output = result.stdout
                info = None
                for line in output.splitlines():
                    if line.startswith("Partner:"):
                        info = line.split("Partner:")[1].strip()
                        break
                return info
        except Exception as e:
            print(f"Error al ejecutar OCaml: {e}")
            return None
    
    def abrir_registro(self):
        from frontend.vista_registro import VentanaRegistro
        self.registro = VentanaRegistro()
        if self.registro.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Registro", "Registro completado. Ahora inicie sesión.")
