import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QMessageBox
)

class VentanaBorrarDatos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Borrar Información")
        self.setGeometry(300, 300, 300, 200)
        
        layout = QVBoxLayout()
        
        # Formulario para ingresar año, semestre y opcionalmente ID del curso
        form_layout = QFormLayout()
        self.input_anio = QLineEdit()
        self.input_anio.setPlaceholderText("Ej: 2023")
        form_layout.addRow("Año:", self.input_anio)
        
        self.input_semestre = QLineEdit()
        self.input_semestre.setPlaceholderText("Ej: 1 o 2")
        form_layout.addRow("Semestre:", self.input_semestre)
        
        self.input_curso_id = QLineEdit()
        self.input_curso_id.setPlaceholderText("ID del Curso (opcional)")
        form_layout.addRow("ID del Curso:", self.input_curso_id)
        
        layout.addLayout(form_layout)
        
        # Botones para borrar curso o semestre
        botones_layout = QHBoxLayout()
        self.btn_borrar_curso = QPushButton("Borrar Curso")
        self.btn_borrar_curso.clicked.connect(self.borrar_curso)
        botones_layout.addWidget(self.btn_borrar_curso)
        
        self.btn_borrar_semestre = QPushButton("Borrar Semestre")
        self.btn_borrar_semestre.clicked.connect(self.borrar_semestre)
        botones_layout.addWidget(self.btn_borrar_semestre)
        
        layout.addLayout(botones_layout)
        self.setLayout(layout)
    
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
        
        path = os.path.join("data", "informacion.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = {"informacion": []}
        else:
            existing = {"informacion": []}
        
        found = False
        for entry in existing["informacion"]:
            if entry.get("anio") == anio and entry.get("semestre") == semestre:
                nuevos_cursos = [curso for curso in entry.get("cursos", []) if curso.get("id") != curso_id]
                if len(nuevos_cursos) < len(entry.get("cursos", [])):
                    entry["cursos"] = nuevos_cursos
                    found = True
        if not found:
            QMessageBox.information(self, "Info", "No se encontró curso con ese ID en ese semestre.")
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=4, ensure_ascii=False)
        QMessageBox.information(self, "Borrado", f"Curso con ID {curso_id} borrado exitosamente.")
        self.accept()
    
    def borrar_semestre(self):
        anio_str = self.input_anio.text().strip()
        semestre_str = self.input_semestre.text().strip()
        if not anio_str or not semestre_str:
            QMessageBox.warning(self, "Error", "Ingrese año y semestre para borrar.")
            return
        try:
            anio = int(anio_str)
            semestre = int(semestre_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "Año y semestre deben ser numéricos.")
            return
        
        path = os.path.join("data", "informacion.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = {"informacion": []}
        else:
            existing = {"informacion": []}
        
        original_len = len(existing["informacion"])
        existing["informacion"] = [
            entry for entry in existing["informacion"]
            if not (entry.get("anio") == anio and entry.get("semestre") == semestre)
        ]
        if len(existing["informacion"]) == original_len:
            QMessageBox.information(self, "Info", "No se encontró información para ese año y semestre.")
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=4, ensure_ascii=False)
        QMessageBox.information(self, "Borrado", f"Se borró la información del año {anio}, semestre {semestre}.")
        self.accept()
