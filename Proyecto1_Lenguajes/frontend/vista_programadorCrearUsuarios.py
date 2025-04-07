import os
import json
import datetime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt

class VentanaProgramadorCrearUsuario(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crear Usuario")
        self.setFixedSize(400, 350)
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        header = QLabel("Registro de Usuario", self)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        form_layout = QFormLayout()
        
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ingrese nombre completo")
        form_layout.addRow("Nombre:", self.input_nombre)
        
        self.input_email_local = QLineEdit()
        self.input_email_local.setPlaceholderText("Ingrese la parte local del email")
        form_layout.addRow("Email (local):", self.input_email_local)
        
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["estudiante", "profesor"])
        form_layout.addRow("Tipo:", self.combo_tipo)
        
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Ingrese la contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Contraseña:", self.input_password)
        
        layout.addLayout(form_layout)
        
        self.btn_guardar = QPushButton("Guardar Usuario")
        self.btn_guardar.clicked.connect(self.guardar_usuario)
        layout.addWidget(self.btn_guardar)
        
        self.setLayout(layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f7f7f7;
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                color: #333;
            }
            QLineEdit, QComboBox {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QPushButton {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                padding: 8px 16px;
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
    
    def guardar_usuario(self):
        nombre = self.input_nombre.text().strip()
        email_local = self.input_email_local.text().strip()
        tipo = self.combo_tipo.currentText().strip().lower()
        password = self.input_password.text().strip()
        
        if not nombre or not email_local or not tipo or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return
        
        # Completar email según el tipo de usuario.
        if tipo == "estudiante":
            dominio = "@estudiante.es"
        elif tipo == "profesor":
            dominio = "@profesor.es"
        else:
            QMessageBox.warning(self, "Error", "Tipo de usuario no válido.")
            return
        email = email_local + dominio
        
        # Cargar usuarios existentes desde usuarios.json
        path_usuarios = os.path.join("data", "usuarios.json")
        if os.path.exists(path_usuarios):
            try:
                with open(path_usuarios, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {"users": []}
        else:
            data = {"users": []}
        
        # Validar que la parte local del email no se repita (sin incluir el dominio)
        for user in data.get("users", []):
            existing_email = user.get("email", "").strip()
            if "@" in existing_email:
                local_part = existing_email.split("@")[0]
                if local_part.lower() == email_local.lower():
                    QMessageBox.warning(self, "Error", "El email (parte local) ya está en uso.")
                    return
        
        # Generar ID automáticamente basado en el año actual.
        current_year = datetime.date.today().year
        count = 0
        for user in data.get("users", []):
            if user.get("tipo", "").lower() == tipo and str(user.get("id", "")).startswith(str(current_year)):
                count += 1
        
        if tipo == "profesor":
            # Formato: año + "00" + 4 dígitos
            new_id = f"{current_year}00{count+1:04d}"
        else:
            # tipo == "estudiante"
            # Formato: año + "000" + 4 dígitos
            new_id = f"{current_year}000{count+1:04d}"
        
        nuevo_usuario = {
            "id": new_id,
            "nombre": nombre,
            "tipo": tipo,
            "email": email,
            "password": password
        }
        
        data["users"].append(nuevo_usuario)
        
        try:
            with open(path_usuarios, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Usuario registrado exitosamente en usuarios.json.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar el usuario: {e}")
