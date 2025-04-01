import subprocess
import json
import os
from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel,
    QMessageBox, QFormLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt

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
        # Crear layout principal con margen y espaciado
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Layout del formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingrese su correo")
        form_layout.addRow("Correo electrónico:", self.email_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Contraseña:", self.password_input)
        
        layout.addLayout(form_layout)
        
        # Botones de acción
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
        # Hoja de estilo para darle un aspecto moderno
        self.setStyleSheet("""
            QDialog {
                background-color: #127575;
            }
            QLabel {
                font-size: 12pt;
                color: #ffffff;
            }
            QLineEdit {
                font-size: 12pt;
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #fff;
            }
            QPushButton {
                font-size: 12pt;
                padding: 8px 12px;
                background-color: #5cb85c;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
        """)
    
    def login(self):
        # Obtener y limpiar las credenciales
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        
        # Guardar las credenciales en data/credenciales.json para que OCaml las lea
        self.guardar_credenciales(email, password)
        
        # Ejecutar el binario OCaml y obtener el rol (se espera "profesor" o "estudiante")
        rol = self.ejecutar_ocaml()
        
        if rol:
            # Según el rol, se abre la ventana correspondiente:
            if rol.lower() == "profesor":
                self.ventana_principal = VentanaPrincipalAdmin(rol)
            elif rol.lower() == "estudiante":
                self.ventana_principal = VentanaPrincipalVisor(rol)
            else:
                QMessageBox.warning(self, "Error", f"Rol desconocido: {rol}")
                return
            
            self.ventana_principal.show()
            self.close()  # Cierra la ventana de login
        else:
            QMessageBox.warning(self, "Error", "Login fallido: credenciales incorrectas.")    
    
    def guardar_credenciales(self, email, password):
        os.makedirs("data", exist_ok=True)
        data = {"users": [{"email": email, "password": password}]}
        with open("data/credenciales.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def ejecutar_ocaml(self):
        try:
            # Construir la ruta al ejecutable OCaml compilado (ajusta la ruta según corresponda)
            ruta_backend = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
            ejecutable = os.path.join(ruta_backend, "verificar_credenciales")
            
            result = subprocess.run([ejecutable], capture_output=True, text=True)
            if result.returncode != 0:
                print("Error al ejecutar OCaml:")
                print(result.stderr)
                return None
            else:
                output = result.stdout
                rol = None
                # Se busca la línea que comience con "Partner:" y se extrae el rol
                for line in output.splitlines():
                    if line.startswith("Partner:"):
                        rol = line.split("Partner:")[1].strip()
                        break
                return rol
        except Exception as e:
            print(f"Error al ejecutar OCaml: {e}")
            return None
    
    def abrir_registro(self):
        from frontend.vista_registro import VentanaRegistro
        self.registro = VentanaRegistro()
        if self.registro.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Registro", "Registro completado. Ahora inicie sesión.")
