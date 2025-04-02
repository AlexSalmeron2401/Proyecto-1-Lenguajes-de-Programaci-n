import os
import json
from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel,
    QMessageBox, QHBoxLayout, QComboBox, QFormLayout
)

class VentanaRegistro(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(300, 300, 400, 350)  # Tamaño ajustado para acomodar nuevos campos
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Campo para correo electrónico
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Correo electrónico")
        form_layout.addRow("Correo electrónico:", self.input_email)
        
        # Campo para contraseña
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")
        self.input_password.setEchoMode(QLineEdit.Password)
        form_layout.addRow("Contraseña:", self.input_password)
        
        # Campo para nombre completo
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre completo")
        form_layout.addRow("Nombre:", self.input_nombre)
        
        # Campo para ID
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID del usuario")
        form_layout.addRow("ID:", self.input_id)
        
        # Combo box para seleccionar el rol: Profesor o Estudiante
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(["Profesor", "Estudiante"])
        form_layout.addRow("Rol:", self.combo_rol)
        
        layout.addLayout(form_layout)
        
        # Botones de Aceptar y Cancelar
        botones_layout = QHBoxLayout()
        btn_ok = QPushButton("Registrar")
        btn_ok.clicked.connect(self.registrar)
        botones_layout.addWidget(btn_ok)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        botones_layout.addWidget(btn_cancel)
        
        layout.addLayout(botones_layout)
        self.setLayout(layout)
    
    def registrar(self):
        email = self.input_email.text().strip()
        password = self.input_password.text().strip()
        nombre = self.input_nombre.text().strip()
        user_id = self.input_id.text().strip()
        rol = self.combo_rol.currentText().strip().lower()  # "profesor" o "estudiante"
        
        if not email or not password or not nombre or not user_id or not rol:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return
        
        os.makedirs("data", exist_ok=True)
        path = os.path.join("data", "usuarios.json")
        
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    usuarios_data = json.load(f)
                except json.JSONDecodeError:
                    usuarios_data = {"users": []}
        else:
            usuarios_data = {"users": []}
        
        # Verificar si el usuario ya existe (por correo)
        for user in usuarios_data["users"]:
            if user.get("email") == email:
                QMessageBox.warning(self, "Error", "El usuario ya está registrado.")
                return
        
        # Crear el nuevo usuario según el rol seleccionado
        if rol == "profesor":
            nuevo_usuario = {
                "tipo": "profesor",
                "nombre": nombre,
                "id": user_id,
                "email": email,
                "password": password,
                "anos": []  # Para ser completada posteriormente
            }
        elif rol == "estudiante":
            nuevo_usuario = {
                "tipo": "estudiante",
                "nombre": nombre,
                "id": user_id,
                "email": email,
                "password": password,
                "cursos_cursados": []  # Para ser completada posteriormente
            }
        else:
            QMessageBox.warning(self, "Error", "Rol no reconocido.")
            return
        
        usuarios_data["users"].append(nuevo_usuario)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(usuarios_data, f, indent=4, ensure_ascii=False)
        
        QMessageBox.information(self, "Registro", "Usuario registrado exitosamente.")
        self.accept()
