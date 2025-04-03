import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt

class VentanaBorrarEstudiantesCursos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Borrar Curso de Estudiante")
        self.setFixedSize(400, 250)
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        self.input_estudiante_id = QLineEdit()
        self.input_estudiante_id.setPlaceholderText("Ej: 2019")
        form_layout.addRow("ID del Estudiante:", self.input_estudiante_id)
        
        self.input_curso_id = QLineEdit()
        self.input_curso_id.setPlaceholderText("Ej: MA0102")
        form_layout.addRow("ID del Curso:", self.input_curso_id)
        
        layout.addLayout(form_layout)
        
        btn_layout = QHBoxLayout()
        btn_borrar = QPushButton("Borrar Curso del Estudiante")
        btn_borrar.clicked.connect(self.borrar_curso_estudiante)
        btn_layout.addWidget(btn_borrar)
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        btn_layout.addWidget(btn_cerrar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QFormLayout QLabel {
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
    
    def borrar_curso_estudiante(self):
        estudiante_id = self.input_estudiante_id.text().strip()
        curso_id = self.input_curso_id.text().strip()
        if not estudiante_id or not curso_id:
            QMessageBox.warning(self, "Error", "Debe ingresar el ID del estudiante y el ID del curso.")
            return
        
        path = os.path.join("data", "usuarios.json")
        if not os.path.exists(path):
            QMessageBox.warning(self, "Error", "El archivo usuarios.json no existe.")
            return
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                usuarios_data = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al leer usuarios.json: {e}")
            return
        
        estudiante_encontrado = False
        curso_eliminado = False
        
        # Buscar el estudiante en el listado de usuarios
        for user in usuarios_data.get("users", []):
            if user.get("tipo") == "estudiante" and user.get("id") == estudiante_id:
                estudiante_encontrado = True
                cursos = user.get("cursos_cursados", [])
                new_cursos = [curso for curso in cursos if curso.get("id") != curso_id]
                if len(new_cursos) < len(cursos):
                    curso_eliminado = True
                    user["cursos_cursados"] = new_cursos
                break
        
        if not estudiante_encontrado:
            QMessageBox.information(self, "Info", "Estudiante no encontrado.")
            return
        
        if not curso_eliminado:
            QMessageBox.information(self, "Info", "El estudiante no tiene asignado ese curso.")
            return
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(usuarios_data, f, indent=4, ensure_ascii=False)
            # Verificar si la lista de cursos queda vacía y mostrar un mensaje
            for user in usuarios_data.get("users", []):
                if user.get("tipo") == "estudiante" and user.get("id") == estudiante_id:
                    if not user.get("cursos_cursados"):
                        QMessageBox.information(self, "Info", "El estudiante ahora no tiene cursos asignados.")
                    break
            QMessageBox.information(self, "Éxito", "Curso borrado del estudiante correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron guardar los cambios: {e}")
