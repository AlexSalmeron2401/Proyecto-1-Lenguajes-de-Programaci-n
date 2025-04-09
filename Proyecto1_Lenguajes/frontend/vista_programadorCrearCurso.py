import os
import json
import datetime
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt

class VentanaProgramadorCrearCurso(QDialog):
    def __init__(self, nombre="Programador"):
        super().__init__()
        self.setWindowTitle("Crear Curso - Vista Programador")
        self.setFixedSize(500, 450)
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        header = QLabel("Crear Curso", self)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        form_layout = QFormLayout()
        
        # Campo para el ID del curso
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("ID del curso (ej. MA0101)")
        form_layout.addRow("ID del Curso:", self.input_id)
        
        # Campo para el Nombre del curso
        self.input_nombre_curso = QLineEdit()
        self.input_nombre_curso.setPlaceholderText("Nombre del curso")
        form_layout.addRow("Nombre del Curso:", self.input_nombre_curso)
        
        # QComboBox para seleccionar el tipo de curso
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Matematico", "Carrera", "Ingles", "Otro"])
        form_layout.addRow("Tipo del Curso:", self.combo_tipo)
        
        # Campo para el Año
        self.input_anio = QLineEdit()
        self.input_anio.setPlaceholderText("Año (ej. 2023)")
        form_layout.addRow("Año:", self.input_anio)
        
        # QComboBox para seleccionar el Semestre (solo 1 o 2)
        self.combo_semestre = QComboBox()
        self.combo_semestre.addItems(["1", "2"])
        form_layout.addRow("Semestre:", self.combo_semestre)
        
        layout.addLayout(form_layout)
        
        # Botón para guardar el curso
        self.btn_guardar = QPushButton("Guardar Curso")
        self.btn_guardar.clicked.connect(self.guardar_curso)
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
    
    def guardar_curso(self):
        id_curso = self.input_id.text().strip()
        nombre_curso = self.input_nombre_curso.text().strip()
        tipo = self.combo_tipo.currentText().strip()
        anio_str = self.input_anio.text().strip()
        semestre_str = self.combo_semestre.currentText().strip()
        
        if not id_curso or not nombre_curso or not tipo or not anio_str or not semestre_str:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return
        
        try:
            anio = int(anio_str)
            semestre = int(semestre_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "El año y el semestre deben ser numéricos.")
            return
        
        # Validar que el año esté entre 2010 y el año actual
        current_year = datetime.date.today().year
        if anio < 2010 or anio > current_year:
            QMessageBox.warning(self, "Error", f"El año debe estar entre 2010 y {current_year}.")
            return
        
        nuevo_curso = {
            "id": id_curso,
            "nombre": nombre_curso,
            "tipo": tipo.lower(),
            "anio": anio,
            "semestre": semestre
        }
        
        path = os.path.join("data", "cursos.json")
        
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}
        
        if "cursos" not in data:
            data["cursos"] = []
        
        data["cursos"].append(nuevo_curso)
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Curso guardado exitosamente en cursos.json.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar el curso: {e}")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ventana = VentanaProgramadorCrearCurso("Programador")
    ventana.exec_()
