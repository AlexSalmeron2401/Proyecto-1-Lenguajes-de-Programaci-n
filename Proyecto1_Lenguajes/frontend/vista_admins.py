from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QDialog
from PyQt5.QtCore import Qt
import os
import json

from frontend.vista_verCursos import VentanaVerCursos
from frontend.vista_estudiantesCursos import VentanaVerEstudiantesCursos

class VentanaPrincipalAdmin(QWidget):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre  # Nombre del profesor (extraído del login)
        self.setWindowTitle("Panel de Administración")
        self.setFixedSize(1280, 720)
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Encabezado
        header = QLabel("Panel de Administración")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Mensaje personalizado de bienvenida
        welcome_label = QLabel(f"Bienvenido, {self.nombre}! Eres un Administrador.")
        welcome_label.setObjectName("welcomeLabel")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Lista de botones con la funcionalidad deseada
        botones = [
            ("Ver Cursos Impartidos", self.abrir_ver_cursos),
            ("Ver Cursos de Estudiantes", self.abrir_ver_estudiantes),
            ("Logout", self.logout)
        ]
        
        for texto, slot in botones:
            btn = QPushButton(texto)
            btn.clicked.connect(slot)
            btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(btn)
        
        self.setLayout(layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F4F7F6;
            }
            #header {
                font-size: 28pt;
                font-weight: bold;
                color: #34495E;
            }
            QLabel#welcomeLabel {
                font-size: 16pt;
                color: #2C3E50;
            }
            QPushButton {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 14pt;
                font-weight: bold;
                letter-spacing: 1px;
                padding: 10px 20px;
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
    
    def obtener_profesor_email(self):
        """Lee el correo del profesor desde data/credenciales.json."""
        path = os.path.join("data", "credenciales.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                users = data.get("users", [])
                if users and isinstance(users, list):
                    return users[0].get("email", "")
                return ""
        except Exception as e:
            print(f"Error al leer credenciales: {e}")
            return ""
    
    def abrir_ver_cursos(self):
        profesor_email = self.obtener_profesor_email()
        self.hide()
        self.verCursos = VentanaVerCursos(profesor_email)
        self.verCursos.exec_()
        self.show()
    
    def abrir_ver_estudiantes(self):
        profesor_email = self.obtener_profesor_email()
        self.hide()
        self.verEstCursos = VentanaVerEstudiantesCursos(profesor_email)
        self.verEstCursos.exec_()
        self.show()
    
    def logout(self):
        from frontend.vista_login import VentanaLogin
        self.hide()
        self.login = VentanaLogin()
        self.login.show()
        self.close()
