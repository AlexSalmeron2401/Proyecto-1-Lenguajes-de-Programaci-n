import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QListWidget, QPushButton, QLabel, 
    QMessageBox
)
from PyQt5.QtCore import Qt

class VentanaEditarDatosEstudiante(QDialog):
    def __init__(self, estudiante_email):
        """
        Recibe el email del estudiante para cargar sus datos y permitir la edición.
        Solo se permite editar los datos personales (nombre, correo y contraseña).
        Los cursos asignados se mostrarán en modo solo lectura.
        El ID del estudiante permanece inalterable.
        """
        super().__init__()
        self.estudiante_email = estudiante_email
        self.estudiante_data = None  # Se llenará con los datos del estudiante de usuarios.json
        self.setWindowTitle("Editar Mi Información")
        self.setFixedSize(500, 400)
        
        self.init_ui()
        self.apply_styles()
        self.cargar_estudiante()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # --- Encabezado ---
        header = QLabel("Editar Datos Personales", self)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # --- Datos Personales ---
        form_personales = QFormLayout()
        self.input_nombre = QLineEdit()
        self.input_email = QLineEdit()
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        
        form_personales.addRow("Nombre:", self.input_nombre)
        form_personales.addRow("Correo:", self.input_email)
        form_personales.addRow("Contraseña:", self.input_pass)
        layout.addLayout(form_personales)
        
        # Mostrar el ID (solo lectura)
        self.label_id = QLabel("ID: ")
        layout.addWidget(self.label_id)
        
        # --- Lista de Cursos Asignados (Solo lectura) ---
        layout.addWidget(QLabel("Mis Cursos Asignados:", self))
        self.lista_cursos = QListWidget()
        self.lista_cursos.setEnabled(False)
        layout.addWidget(self.lista_cursos)
        
        # --- Botones Finales ---
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        btn_layout.addWidget(self.btn_guardar)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                color: #333;
            }
            QLineEdit {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #f9f9f9;
            }
            QListWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QPushButton {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                padding: 8px 16px;
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
    
    # ------------------- Carga de Estudiante -------------------
    def cargar_estudiante(self):
        """
        Carga los datos del estudiante (nombre, email, password, ID y cursos asignados) desde usuarios.json.
        """
        path = os.path.join("data", "usuarios.json")
        if not os.path.exists(path):
            QMessageBox.warning(self, "Error", "No existe el archivo usuarios.json.")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo leer usuarios.json: {e}")
            return
        
        for user in data.get("users", []):
            if user.get("tipo") == "estudiante" and user.get("email", "").strip().lower() == self.estudiante_email.lower():
                self.estudiante_data = user
                break
        
        if not self.estudiante_data:
            QMessageBox.warning(self, "Error", "No se encontró tu información en usuarios.json.")
            return
        
        # Llenar campos personales
        self.input_nombre.setText(self.estudiante_data.get("nombre", ""))
        self.input_email.setText(self.estudiante_data.get("email", ""))
        self.input_pass.setText(self.estudiante_data.get("password", ""))
        # Mostrar el ID (no editable)
        self.label_id.setText(f"ID: {self.estudiante_data.get('id', '')}")
        self.refrescar_lista_cursos()
    
    def refrescar_lista_cursos(self):
        self.lista_cursos.clear()
        if not self.estudiante_data:
            return
        for c in self.estudiante_data.get("cursos_cursados", []):
            texto = f"{c.get('id')} - {c.get('nombre')} ({c.get('tipo')})"
            self.lista_cursos.addItem(texto)
    
    # ------------------- Guardar Cambios -------------------
    def guardar_cambios(self):
        if not self.estudiante_data:
            QMessageBox.warning(self, "Error", "No se cargó la información del estudiante.")
            return
        
        nuevo_nombre = self.input_nombre.text().strip()
        nuevo_email = self.input_email.text().strip()
        nueva_pass = self.input_pass.text().strip()
        
        if not nuevo_nombre or not nuevo_email or not nueva_pass:
            QMessageBox.warning(self, "Error", "El nombre, el correo y la contraseña no pueden quedar vacíos.")
            return
        
        self.estudiante_data["nombre"] = nuevo_nombre
        self.estudiante_data["email"] = nuevo_email
        self.estudiante_data["password"] = nueva_pass
        
        path = os.path.join("data", "usuarios.json")
        if not os.path.exists(path):
            QMessageBox.warning(self, "Error", "No existe el archivo usuarios.json.")
            return
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo leer usuarios.json: {e}")
            return
        
        # Usar el id del estudiante convertido a cadena para identificarlo de forma única
        estudiante_id = str(self.estudiante_data.get("id")).strip()
        actualizado = False
        for user in data.get("users", []):
            if user.get("tipo") == "estudiante" and str(user.get("id")).strip() == estudiante_id:
                user["nombre"] = self.estudiante_data["nombre"]
                user["email"] = self.estudiante_data["email"]
                user["password"] = self.estudiante_data["password"]
                user["cursos_cursados"] = self.estudiante_data.get("cursos_cursados", [])
                actualizado = True
                break
        
        if not actualizado:
            QMessageBox.warning(self, "Error", "No se encontró tu registro para actualizar.")
            return
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Cambios guardados exitosamente.")
            self.estudiante_email = self.estudiante_data["email"]
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar en usuarios.json: {e}")
