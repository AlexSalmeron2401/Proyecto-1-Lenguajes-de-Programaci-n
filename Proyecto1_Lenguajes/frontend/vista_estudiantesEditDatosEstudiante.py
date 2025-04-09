import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt

class VentanaEditarDatosEstudiante(QDialog):
    def __init__(self, estudiante_email):
        """
        Recibe el email del estudiante para cargar sus datos y permitir la edición
        de nombre, la parte local del email y la contraseña.
        El ID del estudiante permanece inalterable.
        """
        super().__init__()
        self.estudiante_email = estudiante_email
        self.estudiante_data = None  # Se llenará con los datos del estudiante de usuarios.json
        self.setWindowTitle("Editar Datos Personales")
        self.setFixedSize(500, 300)
        
        self.init_ui()
        self.apply_styles()
        self.cargar_estudiante()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Encabezado
        header = QLabel("Editar Datos Personales", self)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Formulario de datos personales
        form_layout = QFormLayout()
        self.input_nombre = QLineEdit()
        form_layout.addRow("Nombre:", self.input_nombre)
        
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Ingrese la parte local del correo")
        form_layout.addRow("Correo (local):", self.input_email)
        
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Ingrese la contraseña")
        self.input_pass.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Contraseña:", self.input_pass)
        
        layout.addLayout(form_layout)
        
        # Mostrar el ID (solo lectura)
        self.label_id = QLabel("ID: ", self)
        layout.addWidget(self.label_id)
        
        # Botones Finales
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
    
    def cargar_estudiante(self):
        """
        Carga los datos del estudiante (nombre, email, password y ID) desde usuarios.json.
        Se espera que los usuarios se encuentren bajo la clave "users".
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
        
        # Llenar campos personales con los datos actuales
        self.input_nombre.setText(self.estudiante_data.get("nombre", ""))
        full_email = self.estudiante_data.get("email", "")
        # Extraemos la parte local del email
        local_email = full_email.split("@")[0] if "@" in full_email else full_email
        self.input_email.setText(local_email)
        self.input_pass.setText(self.estudiante_data.get("password", ""))
        self.label_id.setText(f"ID: {self.estudiante_data.get('id', '')}")
    
    def guardar_cambios(self):
        if not self.estudiante_data:
            QMessageBox.warning(self, "Error", "No se cargó la información del estudiante.")
            return
        
        nuevo_nombre = self.input_nombre.text().strip()
        nuevo_email_local = self.input_email.text().strip()
        nueva_pass = self.input_pass.text().strip()
        
        if not nuevo_nombre or not nuevo_email_local or not nueva_pass:
            QMessageBox.warning(self, "Error", "El nombre, el correo y la contraseña no pueden quedar vacíos.")
            return
        
        # Construir el email completo (usando el dominio fijo para estudiantes)
        nuevo_email = nuevo_email_local + "@estudiante.es"
        
        # Actualizar la información en memoria
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
        
        # Buscar y actualizar el registro del estudiante
        actualizado = False
        estudiante_id = str(self.estudiante_data.get("id")).strip()
        for user in data.get("users", []):
            if user.get("tipo") == "estudiante" and str(user.get("id")).strip() == estudiante_id:
                user["nombre"] = self.estudiante_data["nombre"]
                user["email"] = self.estudiante_data["email"]
                user["password"] = self.estudiante_data["password"]
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
