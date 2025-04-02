import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QListWidget, QPushButton, QMessageBox, QComboBox
)
# Importa las clases definidas en tu módulo OOP (ajusta la ruta según corresponda)
from frontend.clases_informacion import CursoMatematico, CursoCarrera, CursoIngles, CursoOtros

class VentanaAgregarCursoDetallado(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Curso")
        self.setFixedSize(400, 200)
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Selección del tipo de curso
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Matemático", "Carrera", "Inglés", "Otros"])
        form_layout.addRow("Tipo de Curso:", self.combo_tipo)
        
        # Campo para el nombre del curso
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ingrese el nombre del curso")
        form_layout.addRow("Nombre del Curso:", self.input_nombre)
        
        # Campo para el ID del curso
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Ingrese el ID del curso")
        form_layout.addRow("ID del Curso:", self.input_id)
        
        layout.addLayout(form_layout)
        
        # Botones de Aceptar y Cancelar
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("Aceptar")
        btn_ok.clicked.connect(self.aceptar)
        btn_layout.addWidget(btn_ok)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)
        
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
    
    def aceptar(self):
        nombre = self.input_nombre.text().strip()
        id_curso = self.input_id.text().strip()
        if not nombre or not id_curso:
            QMessageBox.warning(self, "Error", "Nombre e ID son obligatorios.")
            return
        
        tipo_index = self.combo_tipo.currentIndex()
        try:
            # Asignamos 0.0 a todas las notas, ya que se ingresarán por estudiante posteriormente.
            if tipo_index == 0:  # Matemático
                self.curso = CursoMatematico(
                    nombre=nombre, id=id_curso,
                    nota_examen1=0.0, nota_examen2=0.0, nota_examen3=0.0,
                    nota_tareas=0.0, nota_total=0.0
                )
            elif tipo_index == 1:  # Carrera
                self.curso = CursoCarrera(
                    nombre=nombre, id=id_curso,
                    nota_proyecto1=0.0, nota_proyecto2=0.0,
                    nota_laboratorios=0.0, nota_total=0.0
                )
            elif tipo_index == 2:  # Inglés
                self.curso = CursoIngles(
                    nombre=nombre, id=id_curso,
                    nota_examen1=0.0, nota_examen2=0.0,
                    nota_laboratorios=0.0, nota_tareas=0.0, nota_total=0.0
                )
            elif tipo_index == 3:  # Otros
                self.curso = CursoOtros(
                    nombre=nombre, id=id_curso,
                    nota_trabajo1=0.0, nota_trabajo2=0.0, nota_trabajo3=0.0,
                    notas_tareas=0.0, nota_total=0.0
                )
            else:
                raise ValueError("Tipo de curso no reconocido.")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Error en la conversión de datos: {e}")
            return
        self.accept()
    
    def get_data(self):
        """Retorna el objeto curso creado."""
        return self.curso

class VentanaAgregarDatos(QDialog):
    """
    Este diálogo permite al profesor ingresar el año, semestre y la lista de cursos impartidos.
    La información se actualizará en el archivo "data/usuarios.json" dentro del registro del profesor.
    """
    def __init__(self, profesor_email):
        super().__init__()
        self.setWindowTitle("Agregar Cursos - Por Año")
        self.setFixedSize(500, 400)
        self.profesor_email = profesor_email  # Para identificar el registro del profesor
        self.cursos_detallados = []  # Lista de objetos Curso (detallados)
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulario para ingresar el año y seleccionar el semestre
        form_layout = QFormLayout()
        self.input_anio = QLineEdit()
        self.input_anio.setPlaceholderText("Ej: 2023")
        form_layout.addRow("Año:", self.input_anio)
        
        self.combo_semestre = QComboBox()
        self.combo_semestre.addItems(["1", "2"])
        form_layout.addRow("Semestre:", self.combo_semestre)
        
        layout.addLayout(form_layout)
        
        # Lista para mostrar los cursos detallados agregados
        from PyQt5.QtWidgets import QListWidget
        self.lista_cursos = QListWidget()
        layout.addWidget(self.lista_cursos)
        
        # Botón para agregar un curso detallado
        btn_agregar_curso = QPushButton("Agregar Curso Detallado")
        btn_agregar_curso.clicked.connect(self.agregar_curso_detallado)
        layout.addWidget(btn_agregar_curso)
        
        # Botón para borrar el curso seleccionado
        btn_borrar_curso = QPushButton("Borrar Curso Seleccionado")
        btn_borrar_curso.clicked.connect(self.borrar_curso)
        layout.addWidget(btn_borrar_curso)
        
        # Botones de Aceptar y Cancelar
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("Aceptar")
        btn_ok.clicked.connect(self.aceptar)
        btn_layout.addWidget(btn_ok)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)
        
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
            QComboBox {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #f9f9f9;
            }
            QListWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #ffffff;
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
    
    def agregar_curso_detallado(self):
        dialog = VentanaAgregarCursoDetallado()
        if dialog.exec_() == QDialog.Accepted:
            curso_obj = dialog.get_data()
            self.cursos_detallados.append(curso_obj)
            self.lista_cursos.addItem(f"{curso_obj.id} - {curso_obj.nombre}")
    
    def borrar_curso(self):
        item = self.lista_cursos.currentItem()
        if item:
            row = self.lista_cursos.row(item)
            self.lista_cursos.takeItem(row)
            del self.cursos_detallados[row]
        else:
            QMessageBox.warning(self, "Error", "Seleccione un curso para borrar.")
    
    def aceptar(self):
        anio_str = self.input_anio.text().strip()
        if not anio_str:
            QMessageBox.warning(self, "Error", "Debe ingresar un año.")
            return
        if not self.cursos_detallados:
            QMessageBox.warning(self, "Error", "Debe agregar al menos un curso.")
            return
        
        try:
            self.anio = int(anio_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "El año debe ser numérico.")
            return
        
        self.semestre = int(self.combo_semestre.currentText())
        # Actualizamos el archivo "data/usuarios.json"
        self.write_usuario_json()
        self.accept()
    
    def get_data(self):
        """Retorna la información del año, semestre y cursos detallados."""
        return {
            "anio": self.anio,
            "semestre": self.semestre,
            "cursos": [curso.to_dict() for curso in self.cursos_detallados]
        }
    
    def write_usuario_json(self):
        """Actualiza el archivo data/usuarios.json agregando la información de cursos al profesor identificado.
        Si ya existe un bloque para el mismo año y semestre, se actualiza ese bloque.
        """
        data_to_save = self.get_data()  # Ejemplo: { "anio": 2023, "semestre": 1, "cursos": [...] }
        path = os.path.join("data", "usuarios.json")
        
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    usuarios_data = json.load(f)
                except json.JSONDecodeError:
                    usuarios_data = {"users": []}
        else:
            usuarios_data = {"users": []}
        
        # Buscar el usuario profesor con el email proporcionado
        profesor_encontrado = False
        for user in usuarios_data["users"]:
            if user.get("email") == self.profesor_email and user.get("tipo") == "profesor":
                profesor_encontrado = True
                # Asegurarse de que exista la clave "anos"
                if "anos" not in user or not isinstance(user["anos"], list):
                    user["anos"] = []
                # Buscamos si ya existe un bloque para el mismo año y semestre
                bloque_existente = None
                for bloque in user["anos"]:
                    if bloque.get("anio") == self.anio and bloque.get("semestre") == self.semestre:
                        bloque_existente = bloque
                        break
                if bloque_existente:
                    # Si existe, se agregan los cursos nuevos a la lista existente
                    cursos_existentes = bloque_existente.get("cursos", [])
                    nuevos_cursos = [curso.to_dict() for curso in self.cursos_detallados]
                    bloque_existente["cursos"] = cursos_existentes + nuevos_cursos
                else:
                    # Si no existe, se crea un nuevo bloque
                    user["anos"].append(data_to_save)
                break
        
        if not profesor_encontrado:
            QMessageBox.warning(self, "Error", "No se encontró el profesor en usuarios.json.")
            return
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(usuarios_data, f, indent=4, ensure_ascii=False)
