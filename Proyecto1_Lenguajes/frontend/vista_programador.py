import os
import json
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QDesktopWidget
from PyQt5.QtCore import Qt

from frontend.vista_programadorCrearCurso import VentanaProgramadorCrearCurso
from frontend.vista_programadorCrearUsuarios import VentanaProgramadorCrearUsuario
from frontend.vista_programadorRelacionarCursoProfesor import VentanaProgramadorRelacionarCursoProfesor
from frontend.vista_programadorRelacionarCursoEstudianteProfesor import VentanaProgramadorRelacionarCursoEstudianteProfesor

class VentanaProgramador(QWidget):
    def __init__(self, nombre="Programador"):
        super().__init__()
        self.nombre = nombre
        self.setWindowTitle("Panel de Programador")
        self.setFixedSize(600, 400)
        self.init_ui()
        self.center()  # Centrar la ventana en el monitor
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        header = QLabel(f"Bienvenido, {self.nombre}", self)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Lista de botones con la funcionalidad deseada
        botones = [
            ("Crear Curso", self.abrir_crear_curso),
            ("Crear Usuario", self.abrir_crear_usuario),
            ("Relacionar Curso con Profesor", self.abrir_relacionar_curso_profesor),
            ("Relacionar Curso con Estudiante",self.abrir_relacionar_curso_estudiante),
            ("Logout", self.logout)
        ]
        
        for texto, slot in botones:
            btn = QPushButton(texto)
            btn.clicked.connect(slot)
            btn.setCursor(Qt.PointingHandCursor)
            layout.addWidget(btn)
        
        self.setLayout(layout)
    
    def center(self):
        """Centra la ventana en el monitor."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def abrir_crear_curso(self):
        self.hide()
        ventana_crear = VentanaProgramadorCrearCurso()
        ventana_crear.exec_()
        self.show()
    
    def abrir_crear_usuario(self):
        self.hide()
        ventana_crear = VentanaProgramadorCrearUsuario()
        ventana_crear.exec_()
        self.show()
    def abrir_relacionar_curso_profesor(self):
        self.hide()
        ventana_crear = VentanaProgramadorRelacionarCursoProfesor()
        ventana_crear.exec_()
        self.show()
    def abrir_relacionar_curso_estudiante(self):
        self.hide()
        ventana_crear = VentanaProgramadorRelacionarCursoEstudianteProfesor()
        ventana_crear.exec_()
        self.show()
    def logout(self):
        from frontend.vista_login import VentanaLogin
        QMessageBox.information(self, "Logout", "Has cerrado sesión.")
        self.login = VentanaLogin()
        self.login.show()
        self.close()