import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox,
    QPushButton, QListWidget, QMessageBox
)

class VentanaVerEstudiantesCursos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ver Cursos de Estudiantes")
        self.setGeometry(250, 250, 500, 400)
        layout = QVBoxLayout()
        
        # Se asume que los estudiantes se almacenan en data/estudiantes.json
        # con la estructura:
        # { "estudiantes": [ { "nombre": "María López", "id": "E001", "cursos": [ { "anio":2023, "semestre":1, "curso": { ... } }, ... ] }, ... ] }
        form_layout = QFormLayout()
        self.combo_estudiante = QComboBox()
        self.cargar_estudiantes()
        form_layout.addRow("Estudiante:", self.combo_estudiante)
        layout.addLayout(form_layout)
        
        # Botón para ver cursos del estudiante seleccionado
        self.btn_ver = QPushButton("Ver Cursos")
        self.btn_ver.clicked.connect(self.ver_cursos)
        layout.addWidget(self.btn_ver)
        
        # Lista para mostrar los cursos
        self.lista_cursos = QListWidget()
        layout.addWidget(self.lista_cursos)
        
        self.setLayout(layout)
    
    def cargar_estudiantes(self):
        path = os.path.join("data", "estudiantes.json")
        self.combo_estudiante.clear()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.estudiantes = data.get("estudiantes", [])
                    for est in self.estudiantes:
                        # Se agrega el nombre y se asocia el objeto completo
                        self.combo_estudiante.addItem(est.get("nombre"), est)
                except json.JSONDecodeError:
                    self.estudiantes = []
        else:
            self.estudiantes = []
    
    def ver_cursos(self):
        self.lista_cursos.clear()
        est_data = self.combo_estudiante.currentData()
        if not est_data:
            QMessageBox.warning(self, "Error", "No hay estudiante seleccionado.")
            return
        cursos = est_data.get("cursos", [])
        if not cursos:
            QMessageBox.information(self, "Info", "Este estudiante no tiene cursos registrados.")
            return
        for curso in cursos:
            # Se asume que cada curso está almacenado como un diccionario con claves: anio, semestre y curso (donde curso es un objeto con nombre, id, etc.)
            curso_info = curso.get("curso", {})
            item_text = f"Año: {curso.get('anio')}, Semestre: {curso.get('semestre')}, Curso: {curso_info.get('nombre', 'Desconocido')}"
            self.lista_cursos.addItem(item_text)
