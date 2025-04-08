import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QLabel, QComboBox, QPushButton, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt

class VentanaVerCursos(QDialog):
    def __init__(self, profesor_email):
        """
        Recibe el email del profesor; a partir de este se consulta usuarios.json para obtener su id.
        Luego se carga el archivo cursoEstudianteProfesor.json y se filtran los cursos que tengan asignado ese profesor.
        Opcionalmente, se pueden filtrar por año y semestre.
        """
        super().__init__()
        self.profesor_email = profesor_email
        self.profesor_id = self.obtener_profesor_id()
        self.setWindowTitle("Ver Cursos Impartidos (Profesor)")
        self.setFixedSize(600, 500)
        self.init_ui()
        self.load_cursos()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        header = QLabel("Cursos asignados a mi perfil", self)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Filtros opcionales: año y semestre.
        filtros_layout = QFormLayout()
        self.input_filtro_anio = QLineEdit()
        self.input_filtro_anio.setPlaceholderText("Ej: 2022")
        filtros_layout.addRow("Filtrar por Año:", self.input_filtro_anio)
        
        self.input_filtro_semestre = QLineEdit()
        self.input_filtro_semestre.setPlaceholderText("Ej: 1")
        filtros_layout.addRow("Filtrar por Semestre:", self.input_filtro_semestre)
        
        btn_filtrar = QPushButton("Filtrar Cursos")
        btn_filtrar.clicked.connect(self.filtrar_cursos)
        filtros_layout.addRow(btn_filtrar)
        
        layout.addLayout(filtros_layout)
        
        # Lista de cursos
        self.lista_cursos = QListWidget()
        self.lista_cursos.itemDoubleClicked.connect(self.ver_estudiantes)
        layout.addWidget(self.lista_cursos)
        
        self.setLayout(layout)
    
    def obtener_profesor_id(self):
        """
        Lee el archivo usuarios.json y busca el registro de tipo "profesor" que tenga
        el email igual a self.profesor_email. Devuelve su campo "id" (o None si no se encuentra).
        """
        path = os.path.join("data", "usuarios.json")
        profesor_id = None
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for user in data.get("users", []):
                    if user.get("tipo", "").lower() == "profesor" and user.get("email", "").strip().lower() == self.profesor_email.strip().lower():
                        profesor_id = user.get("id")
                        break
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al leer usuarios.json: {e}")
        else:
            QMessageBox.warning(self, "Error", "No se encontró el archivo usuarios.json.")
        return profesor_id
    
    def load_cursos(self):
        """
        Carga la información desde cursoEstudianteProfesor.json.
        Se espera que la estructura sea:
        {
            "cursos": {
                "<anio>": {
                    "<semestre>": [
                        { ... curso con campos, incluyendo "profe" y "estudiantes": [ { "id":..., "nombre":..., "notas": { ... } }, ... ] }
                    ]
                }
            }
        }
        Almacena todos los cursos asignados al profesor en self.lista_cursos_data y los muestra.
        """
        self.all_cursos = []  # Lista completa de cursos filtrados por profesor
        path = os.path.join("data", "cursoEstudianteProfesor.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cursos_dict = data.get("cursos", {})
                # Recorremos cada año y cada semestre
                for anio_key, semestres in cursos_dict.items():
                    for semestre_key, cursos_list in semestres.items():
                        for curso in cursos_list:
                            if curso.get("profe") == self.profesor_id:
                                self.all_cursos.append(curso)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al leer cursoEstudianteProfesor.json: {e}")
        else:
            QMessageBox.warning(self, "Error", "No se encontró el archivo cursoEstudianteProfesor.json.")
        
        # Una vez cargados, se muestran (sin filtrar o filtrados si hay datos en los filtros)
        self.populate_lista_cursos(self.all_cursos)
    
    def populate_lista_cursos(self, cursos):
        self.lista_cursos.clear()
        if cursos:
            for curso in cursos:
                # Se muestra información resumida; por ejemplo: "ID - Nombre (Tipo) | Año: X, Semestre: Y"
                item_text = (f"{curso.get('id')} - {curso.get('nombre')} "
                             f"({curso.get('tipo')}) | Año: {curso.get('anio')}, Semestre: {curso.get('semestre')}")
                self.lista_cursos.addItem(item_text)
        else:
            self.lista_cursos.addItem("No se encontraron cursos para este profesor con esos filtros.")
    
    def filtrar_cursos(self):
        """
        Si se ingresa un año y/o semestre en los cuadros de filtro, se filtran los cursos.
        """
        filtro_anio = self.input_filtro_anio.text().strip()
        filtro_semestre = self.input_filtro_semestre.text().strip()
        
        try:
            anio = int(filtro_anio) if filtro_anio else None
            semestre = int(filtro_semestre) if filtro_semestre else None
        except ValueError:
            QMessageBox.warning(self, "Error", "El año y el semestre deben ser numéricos.")
            return
        
        filtered = []
        for curso in self.all_cursos:
            cond = True
            if anio is not None and curso.get("anio") != anio:
                cond = False
            if semestre is not None and curso.get("semestre") != semestre:
                cond = False
            if cond:
                filtered.append(curso)
        self.populate_lista_cursos(filtered)
    
    def ver_estudiantes(self, item):
        """
        Al hacer doble clic en un curso, se mostrará un mensaje con la lista de estudiantes asignados a ese curso.
        """
        # Se obtiene el texto del item, pero para obtener los datos completos se podría buscar el curso
        # en la lista self.all_cursos usando el id (asumiendo que los ids son únicos).
        texto = item.text()
        curso_id = texto.split(" - ")[0].strip()
        # Buscar el curso en la lista completa
        curso_encontrado = None
        for curso in self.all_cursos:
            if curso.get("id") == curso_id:
                curso_encontrado = curso
                break
        if curso_encontrado:
            estudiantes = curso_encontrado.get("estudiantes", [])
            if estudiantes:
                lista = "\n".join([f"{est.get('id')} - {est.get('nombre')}" for est in estudiantes])
                QMessageBox.information(self, "Estudiantes en el Curso", lista)
            else:
                QMessageBox.information(self, "Estudiantes en el Curso", "No hay estudiantes asignados a este curso.")
        else:
            QMessageBox.warning(self, "Error", "Curso no encontrado.")
            