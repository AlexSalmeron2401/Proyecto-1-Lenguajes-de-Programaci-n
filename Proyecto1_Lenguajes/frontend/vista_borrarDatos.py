import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)

class VentanaBorrarDatos(QDialog):
    def __init__(self, profesor_email):
        super().__init__()
        self.setWindowTitle("Borrar Curso / Semestre")
        self.setFixedSize(400, 300)
        self.profesor_email = profesor_email  # Correo del profesor para identificar su registro en usuarios.json
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        self.input_anio = QLineEdit()
        self.input_anio.setPlaceholderText("Ej: 2000")
        form_layout.addRow("Año:", self.input_anio)
        
        self.input_semestre = QLineEdit()
        self.input_semestre.setPlaceholderText("Ej: 1 o 2")
        form_layout.addRow("Semestre:", self.input_semestre)
        
        self.input_curso_id = QLineEdit()
        self.input_curso_id.setPlaceholderText("ID del Curso (si desea borrar solo un curso)")
        form_layout.addRow("ID del Curso:", self.input_curso_id)
        
        layout.addLayout(form_layout)
        
        botones_layout = QHBoxLayout()
        btn_borrar_curso = QPushButton("Borrar Curso")
        btn_borrar_curso.clicked.connect(self.borrar_curso)
        botones_layout.addWidget(btn_borrar_curso)
        
        btn_borrar_semestre = QPushButton("Borrar Semestre")
        btn_borrar_semestre.clicked.connect(self.borrar_semestre)
        botones_layout.addWidget(btn_borrar_semestre)
        
        layout.addLayout(botones_layout)
        self.setLayout(layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid #ccc;
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
    
    def borrar_curso(self):
        anio_str = self.input_anio.text().strip()
        semestre_str = self.input_semestre.text().strip()
        curso_id = self.input_curso_id.text().strip()
        
        if not anio_str or not semestre_str or not curso_id:
            QMessageBox.warning(self, "Error", "Ingrese año, semestre y ID del curso para borrar.")
            return
        
        try:
            anio = int(anio_str)
            semestre = int(semestre_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "Año y semestre deben ser numéricos.")
            return
        
        path = os.path.join("data", "usuarios.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    usuarios_data = json.load(f)
                except json.JSONDecodeError:
                    usuarios_data = {"users": []}
        else:
            usuarios_data = {"users": []}
        
        profesor_encontrado = False
        curso_eliminado = False
        
        # Buscar el registro del profesor
        for user in usuarios_data["users"]:
            if user.get("email") == self.profesor_email and user.get("tipo") == "profesor":
                profesor_encontrado = True
                if "anos" in user and isinstance(user["anos"], list):
                    nuevos_anos = []
                    for bloque in user["anos"]:
                        # Se asume que cada bloque tiene "anio", "semestre" y "cursos"
                        if bloque.get("anio") == anio and bloque.get("semestre") == semestre:
                            cursos = bloque.get("cursos", [])
                            nuevos_cursos = [curso for curso in cursos if curso.get("id") != curso_id]
                            if len(nuevos_cursos) < len(cursos):
                                # Si quedan cursos, actualizamos el bloque; si no, omitimos el bloque.
                                if nuevos_cursos:
                                    bloque["cursos"] = nuevos_cursos
                                    nuevos_anos.append(bloque)
                                curso_eliminado = True
                            else:
                                nuevos_anos.append(bloque)
                        else:
                            nuevos_anos.append(bloque)
                    user["anos"] = nuevos_anos
                break
        
        if not profesor_encontrado:
            QMessageBox.warning(self, "Error", "No se encontró el profesor en usuarios.json.")
            return
        
        if not curso_eliminado:
            QMessageBox.information(self, "Info", "No se encontró el curso con ese ID en el año y semestre indicados.")
            return
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(usuarios_data, f, indent=4, ensure_ascii=False)
        QMessageBox.information(self, "Borrado", f"Curso con ID {curso_id} borrado exitosamente.")
        self.accept()
    
    def borrar_semestre(self):
        anio_str = self.input_anio.text().strip()
        semestre_str = self.input_semestre.text().strip()
        
        if not anio_str or not semestre_str:
            QMessageBox.warning(self, "Error", "Ingrese año y semestre para borrar el semestre.")
            return
        
        try:
            anio = int(anio_str)
            semestre = int(semestre_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "Año y semestre deben ser numéricos.")
            return
        
        path = os.path.join("data", "usuarios.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    usuarios_data = json.load(f)
                except json.JSONDecodeError:
                    usuarios_data = {"users": []}
        else:
            usuarios_data = {"users": []}
        
        profesor_encontrado = False
        bloque_eliminado = False
        
        for user in usuarios_data["users"]:
            if user.get("email") == self.profesor_email and user.get("tipo") == "profesor":
                profesor_encontrado = True
                if "anos" in user and isinstance(user["anos"], list):
                    nuevos_anos = [bloque for bloque in user["anos"]
                                   if not (bloque.get("anio") == anio and bloque.get("semestre") == semestre)]
                    if len(nuevos_anos) < len(user["anos"]):
                        bloque_eliminado = True
                    user["anos"] = nuevos_anos
                break
        
        if not profesor_encontrado:
            QMessageBox.warning(self, "Error", "No se encontró el profesor en usuarios.json.")
            return
        
        if not bloque_eliminado:
            QMessageBox.information(self, "Info", "No se encontró información para ese año y semestre.")
            return
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(usuarios_data, f, indent=4, ensure_ascii=False)
        QMessageBox.information(self, "Borrado", f"Se borró toda la información del año {anio}, semestre {semestre}.")
        self.accept()
