import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QComboBox, QPushButton, QMessageBox, QLineEdit
)
from PyQt5.QtCore import Qt

class VentanaProgramadorRelacionarCursoProfesor(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Relacionar Curso a Profesor - Vista Programador")
        self.setFixedSize(600, 500)
        self.init_ui()
        self.load_data()  # Carga cursos y profesores

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Encabezado
        header = QLabel("Relacionar Curso con Profesor", self)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Formulario de filtros para cursos
        filter_form = QFormLayout()
        self.input_anio = QLineEdit()
        self.input_anio.setPlaceholderText("Ingrese el año (ej. 2022)")
        filter_form.addRow("Año:", self.input_anio)
        
        self.input_semestre = QLineEdit()
        self.input_semestre.setPlaceholderText("Ingrese el semestre (1 o 2)")
        filter_form.addRow("Semestre:", self.input_semestre)
        
        layout.addLayout(filter_form)
        
        # Botón para filtrar cursos según año y semestre
        self.btn_filtrar = QPushButton("Filtrar Cursos")
        self.btn_filtrar.clicked.connect(self.filtrar_cursos)
        layout.addWidget(self.btn_filtrar)
        
        # Formulario con dos ComboBox: uno para cursos (filtrados) y otro para profesores
        form_layout = QFormLayout()
        self.combo_cursos = QComboBox()
        form_layout.addRow("Curso:", self.combo_cursos)
        
        self.combo_profesores = QComboBox()
        form_layout.addRow("Profesor:", self.combo_profesores)
        layout.addLayout(form_layout)
        
        # Botón para asignar el curso al profesor
        self.btn_asignar = QPushButton("Asignar Curso al Profesor")
        self.btn_asignar.clicked.connect(self.asignar_curso)
        layout.addWidget(self.btn_asignar)
        
        self.setLayout(layout)
    
    def load_data(self):
        """Carga cursos desde cursos.json y profesores desde usuarios.json."""
        # Cargar cursos desde cursos.json
        cursos_path = os.path.join("data", "cursos.json")
        self.cursos = []
        if os.path.exists(cursos_path):
            try:
                with open(cursos_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.cursos = data.get("cursos", [])
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al leer cursos.json: {e}")
        else:
            QMessageBox.warning(self, "Error", "No se encontró el archivo cursos.json.")
        
        # Inicialmente se muestran todos los cursos (sin filtro)
        self.populate_combo_cursos(self.cursos)
        
        # Cargar profesores desde usuarios.json (filtrando por tipo "profesor")
        usuarios_path = os.path.join("data", "usuarios.json")
        self.profesores = []
        if os.path.exists(usuarios_path):
            try:
                with open(usuarios_path, "r", encoding="utf-8") as f:
                    users_data = json.load(f)
                    for user in users_data.get("users", []):
                        if user.get("tipo", "").lower() == "profesor":
                            self.profesores.append(user)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al leer usuarios.json: {e}")
        else:
            QMessageBox.warning(self, "Error", "No se encontró el archivo usuarios.json.")
        
        self.populate_combo_profesores()
    
    def populate_combo_cursos(self, cursos):
        """Llena el ComboBox de cursos con la lista dada."""
        self.combo_cursos.clear()
        self.combo_cursos.addItem("-- Seleccionar Curso --", None)
        for curso in cursos:
            display_text = (f"{curso.get('id')} - {curso.get('nombre')} "
                            f"({curso.get('tipo')}) - Año: {curso.get('anio')}, Semestre: {curso.get('semestre')}")
            self.combo_cursos.addItem(display_text, curso)
    
    def populate_combo_profesores(self):
        """Llena el ComboBox de profesores con la lista cargada."""
        self.combo_profesores.clear()
        for prof in self.profesores:
            display_text = f"{prof.get('id')} - {prof.get('nombre')}"
            self.combo_profesores.addItem(display_text, prof)
    
    def filtrar_cursos(self):
        """Filtra los cursos según el año y semestre ingresados."""
        anio_text = self.input_anio.text().strip()
        semestre_text = self.input_semestre.text().strip()
        if not anio_text or not semestre_text:
            QMessageBox.warning(self, "Error", "Debe ingresar año y semestre para filtrar.")
            return
        try:
            anio = int(anio_text)
            semestre = int(semestre_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "El año y el semestre deben ser numéricos.")
            return
        
        cursos_filtrados = [curso for curso in self.cursos if curso.get("anio") == anio and curso.get("semestre") == semestre]
        if not cursos_filtrados:
            QMessageBox.information(self, "Info", "No se encontraron cursos para el año y semestre indicados.")
        self.populate_combo_cursos(cursos_filtrados)
    
    def asignar_curso(self):
        """
        Asigna el curso seleccionado al profesor y guarda la asignación en cursoProfesor.json.
        Permite que el mismo curso sea asignado a distintos profesores, pero no duplicar
        la asignación para el mismo profesor.
        Además, se verifica que el profesor asignado no sea el mismo que ya tenga ese curso.
        """
        curso = self.combo_cursos.currentData()
        profesor = self.combo_profesores.currentData()
        
        if not curso or not profesor:
            QMessageBox.warning(self, "Error", "Debe seleccionar un curso y un profesor.")
            return
        
        # Crear una copia del curso y añadir el campo "profe" con el ID del profesor
        curso_asignado = curso.copy()
        curso_asignado["profe"] = profesor.get("id")
        
        # Cargar asignaciones existentes desde cursoProfesor.json
        asignaciones_path = os.path.join("data", "cursoProfesor.json")
        if os.path.exists(asignaciones_path):
            try:
                with open(asignaciones_path, "r", encoding="utf-8") as f:
                    asignaciones_data = json.load(f)
            except json.JSONDecodeError:
                asignaciones_data = {"cursos": []}
        else:
            asignaciones_data = {"cursos": []}
        
        # Verificar que no se duplique la asignación para el mismo profesor y mismo curso
        if any(a.get("id") == curso_asignado.get("id") and a.get("profe") == curso_asignado.get("profe")
               for a in asignaciones_data.get("cursos", [])):
            QMessageBox.information(self, "Info", "El curso ya está asignado a este profesor.")
            return
        
        asignaciones_data["cursos"].append(curso_asignado)
        
        try:
            with open(asignaciones_path, "w", encoding="utf-8") as f:
                json.dump(asignaciones_data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Curso asignado exitosamente al profesor en cursoProfesor.json.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron guardar los cambios: {e}")