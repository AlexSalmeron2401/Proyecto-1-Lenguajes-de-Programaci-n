import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QComboBox, QPushButton, QListWidget, QMessageBox, QHBoxLayout
)

class VentanaAgregarEstudiantes(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Estudiante")
        self.setGeometry(250, 250, 500, 500)
        
        self.cursos_asignados = []  # Lista de cursos asignados al estudiante (cada uno es un dict)
        self.cursos_info = []       # Lista de todos los cursos disponibles (se cargan del JSON "informacion")
        self.load_cursos_info()
        
        layout = QVBoxLayout()
        
        # Formulario para ingresar datos del estudiante
        form_layout = QFormLayout()
        self.input_nombre = QLineEdit()
        form_layout.addRow("Nombre del Estudiante:", self.input_nombre)
        self.input_id = QLineEdit()
        form_layout.addRow("ID del Estudiante:", self.input_id)
        layout.addLayout(form_layout)
        
        # Sección para seleccionar un curso desde la información
        self.combo_cursos = QComboBox()
        self.populate_combo_cursos()
        layout.addWidget(QLabel("Seleccione un curso para asignar:"))
        layout.addWidget(self.combo_cursos)
        
        # Botón para agregar el curso seleccionado
        btn_agregar_curso = QPushButton("Agregar Curso")
        btn_agregar_curso.clicked.connect(self.agregar_curso)
        layout.addWidget(btn_agregar_curso)
        
        # Lista para mostrar los cursos asignados
        layout.addWidget(QLabel("Cursos asignados:"))
        self.lista_cursos_asignados = QListWidget()
        layout.addWidget(self.lista_cursos_asignados)
        
        # Botón para eliminar un curso asignado
        btn_borrar_curso = QPushButton("Borrar Curso Asignado")
        btn_borrar_curso.clicked.connect(self.borrar_curso_asignado)
        layout.addWidget(btn_borrar_curso)
        
        # Botones Aceptar y Cancelar
        botones_layout = QHBoxLayout()
        btn_ok = QPushButton("Aceptar")
        btn_ok.clicked.connect(self.aceptar)
        botones_layout.addWidget(btn_ok)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        botones_layout.addWidget(btn_cancel)
        layout.addLayout(botones_layout)
        
        self.setLayout(layout)
    
    def load_cursos_info(self):
        """Carga la información de cursos desde data/informacion.json y la aplana en self.cursos_info."""
        path = os.path.join("data", "informacion.json")
        self.cursos_info = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    for registro in data.get("informacion", []):
                        anio = registro.get("anio")
                        semestre = registro.get("semestre")
                        for curso in registro.get("cursos", []):
                            # Agregar la información del año y semestre al curso
                            curso["anio"] = anio
                            curso["semestre"] = semestre
                            self.cursos_info.append(curso)
                except json.JSONDecodeError:
                    QMessageBox.warning(self, "Error", "Error al leer data/informacion.json.")
    
    def populate_combo_cursos(self):
        """Llena el combo con la lista de cursos disponibles."""
        self.combo_cursos.clear()
        for curso in self.cursos_info:
            # Formato: "Año: {anio}, Semestre: {semestre} - {id} - {nombre} ({tipo})"
            display_text = (f"Año: {curso.get('anio')}, Semestre: {curso.get('semestre')} - "
                            f"{curso.get('id')} - {curso.get('nombre')} ({curso.get('tipo')})")
            self.combo_cursos.addItem(display_text, curso)
    
    def agregar_curso(self):
        index = self.combo_cursos.currentIndex()
        if index < 0:
            QMessageBox.warning(self, "Error", "No hay curso seleccionado.")
            return
        curso = self.combo_cursos.itemData(index)
        self.cursos_asignados.append(curso)
        display_text = (f"Año: {curso.get('anio')}, Semestre: {curso.get('semestre')} - "
                        f"{curso.get('id')} - {curso.get('nombre')}")
        self.lista_cursos_asignados.addItem(display_text)
    
    def borrar_curso_asignado(self):
        item = self.lista_cursos_asignados.currentItem()
        if item:
            row = self.lista_cursos_asignados.row(item)
            self.lista_cursos_asignados.takeItem(row)
            del self.cursos_asignados[row]
        else:
            QMessageBox.warning(self, "Error", "Seleccione un curso asignado para borrar.")
    
    def aceptar(self):
        nombre = self.input_nombre.text().strip()
        id_est = self.input_id.text().strip()
        if not nombre or not id_est:
            QMessageBox.warning(self, "Error", "El nombre y el ID del estudiante son obligatorios.")
            return
        if not self.cursos_asignados:
            QMessageBox.warning(self, "Error", "Debe asignar al menos un curso al estudiante.")
            return
        
        # Crea el diccionario del estudiante
        estudiante = {
            "nombre": nombre,
            "id": id_est,
            "cursos": self.cursos_asignados  # Cada curso ya contiene anio, semestre, etc.
        }
        self.write_estudiante_json(estudiante)
        QMessageBox.information(self, "Éxito", "Estudiante agregado correctamente.")
        self.accept()
    
    def write_estudiante_json(self, estudiante):
        """Guarda o actualiza el archivo data/estudiantes.json con el nuevo estudiante."""
        path = os.path.join("data", "estudiantes.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {"estudiantes": []}
        else:
            data = {"estudiantes": []}
        
        data["estudiantes"].append(estudiante)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
