import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QComboBox, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QStackedWidget
)
from PyQt5.QtCore import Qt

class VentanaAgregarEstudiantes(QDialog):
    def __init__(self, profesor_email):
        """
        Recibe el correo del profesor para cargar los cursos que imparte y para luego 
        relacionar un estudiante registrado con alguno de esos cursos.
        """
        super().__init__()
        self.setWindowTitle("Asignar Curso a Estudiante")
        self.setFixedSize(650, 600)
        self.profesor_email = profesor_email
        self.cursos_asignados = []  # Lista de cursos asignados (cada uno es un dict con notas)
        self.cursos_info = []       # Lista de cursos disponibles, extraídos del registro del profesor
        self.load_cursos_info()     # Cargar cursos desde usuarios.json del profesor
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Formulario para ingresar datos del estudiante
        form_est = QFormLayout()
        self.input_nombre = QLineEdit()
        form_est.addRow("Nombre del Estudiante:", self.input_nombre)
        self.input_id = QLineEdit()
        form_est.addRow("ID del Estudiante:", self.input_id)
        layout.addLayout(form_est)
        
        # Combo para seleccionar un curso del profesor
        self.combo_cursos = QComboBox()
        self.populate_combo_cursos()
        layout.addWidget(QLabel("Seleccione un curso para asignar:"))
        layout.addWidget(self.combo_cursos)
        
        # Sección de notas: Usamos un QStackedWidget para formularios según el tipo de curso
        self.stack_notas = QStackedWidget()
        self.form_matematico = self.create_notas_form(["Examen 1:", "Examen 2:", "Examen 3:", "Tareas:"])
        self.form_carrera = self.create_notas_form(["Proyecto 1:", "Proyecto 2:", "Laboratorios:"])
        self.form_ingles = self.create_notas_form(["Examen 1:", "Examen 2:", "Laboratorios:", "Tareas:"])
        self.form_otros = self.create_notas_form(["Trabajo 1:", "Trabajo 2:", "Trabajo 3:", "Tareas:"])
        self.stack_notas.addWidget(self.form_matematico)
        self.stack_notas.addWidget(self.form_carrera)
        self.stack_notas.addWidget(self.form_ingles)
        self.stack_notas.addWidget(self.form_otros)
        layout.addWidget(QLabel("Ingrese las notas para el curso seleccionado:"))
        layout.addWidget(self.stack_notas)
        # Actualiza el formulario de notas según el curso seleccionado
        self.combo_cursos.currentIndexChanged.connect(self.update_notas_form)
        
        # Botón para asignar el curso al estudiante
        btn_asignar = QPushButton("Asignar Curso")
        btn_asignar.clicked.connect(self.agregar_curso)
        layout.addWidget(btn_asignar)
        
        # Lista para mostrar los cursos asignados al estudiante
        layout.addWidget(QLabel("Cursos asignados:"))
        self.lista_asignados = QListWidget()
        layout.addWidget(self.lista_asignados)
        
        # Botón para borrar un curso asignado
        btn_borrar = QPushButton("Borrar Curso Asignado")
        btn_borrar.clicked.connect(self.borrar_curso_asignado)
        layout.addWidget(btn_borrar)
        
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
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
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
    
    def create_notas_form(self, labels):
        """
        Crea un formulario de notas con las etiquetas proporcionadas.
        Retorna un QWidget con un QFormLayout y una lista 'inputs' con las QLineEdit.
        """
        widget = QDialog()
        form = QFormLayout()
        widget.inputs = []
        for text in labels:
            le = QLineEdit()
            le.setPlaceholderText("0.0")
            form.addRow(text, le)
            widget.inputs.append(le)
        widget.setLayout(form)
        return widget
    
    def load_cursos_info(self):
        """
        Carga los cursos asignados al profesor desde usuarios.json.
        Se busca el registro del profesor (por correo) y se recorre su lista "anos".
        Cada bloque de "anos" contiene uno o más cursos y se agregan al listado.
        """
        self.cursos_info = []
        path = os.path.join("data", "usuarios.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for user in data.get("users", []):
                        if user.get("email") == self.profesor_email and user.get("tipo") == "profesor":
                            for bloque in user.get("anos", []):
                                anio = bloque.get("anio")
                                semestre = bloque.get("semestre")
                                for curso in bloque.get("cursos", []):
                                    curso_copy = curso.copy()
                                    curso_copy["anio"] = anio
                                    curso_copy["semestre"] = semestre
                                    self.cursos_info.append(curso_copy)
                            break
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al cargar cursos: {e}")
    
    def populate_combo_cursos(self):
        """Llena el combo con la lista de cursos disponibles del profesor."""
        self.load_cursos_info()
        self.combo_cursos.clear()
        for curso in self.cursos_info:
            display_text = (f"Año: {curso.get('anio')}, Semestre: {curso.get('semestre')} - "
                            f"{curso.get('id')} - {curso.get('nombre')} ({curso.get('tipo')})")
            self.combo_cursos.addItem(display_text, curso)
    
    def update_notas_form(self):
        """Actualiza el formulario de notas según el tipo de curso seleccionado."""
        index = self.combo_cursos.currentIndex()
        if index < 0:
            return
        curso = self.combo_cursos.itemData(index)
        tipo = curso.get("tipo", "").lower()
        mapping = {"matematico": 0, "carrera": 1, "ingles": 2, "otrocursos": 3, "otrocurso": 3}
        form_index = mapping.get(tipo, 0)
        self.stack_notas.setCurrentIndex(form_index)
    
    def agregar_curso(self):
        index = self.combo_cursos.currentIndex()
        if index < 0:
            QMessageBox.warning(self, "Error", "No hay curso seleccionado.")
            return
        curso = self.combo_cursos.itemData(index)
        # Obtener las notas ingresadas desde el formulario actual
        current_form = self.stack_notas.currentWidget()
        notas = []
        for le in current_form.inputs:
            try:
                nota = float(le.text().strip())
            except ValueError:
                nota = 0.0
            notas.append(nota)
        
        tipo = curso.get("tipo", "").lower()
        if tipo == "matematico":
            curso["nota_examen1"], curso["nota_examen2"], curso["nota_examen3"], curso["nota_tareas"] = notas
        elif tipo == "carrera":
            curso["nota_proyecto1"], curso["nota_proyecto2"], curso["nota_laboratorios"] = notas
        elif tipo == "ingles":
            curso["nota_examen1"], curso["nota_examen2"], curso["nota_laboratorios"], curso["nota_tareas"] = notas
        elif tipo in ["otrocursos", "otrocurso"]:
            curso["nota_trabajo1"], curso["nota_trabajo2"], curso["nota_trabajo3"], curso["nota_tareas"] = notas
        
        if notas:
            curso["nota_total"] = sum(notas) / len(notas)
        else:
            curso["nota_total"] = 0.0
        
        self.cursos_asignados.append(curso)
        display_text = (f"Año: {curso.get('anio')}, Semestre: {curso.get('semestre')} - "
                        f"{curso.get('id')} - {curso.get('nombre')} ({curso.get('tipo')})")
        self.lista_asignados.addItem(display_text)
    
    def borrar_curso_asignado(self):
        item = self.lista_asignados.currentItem()
        if item:
            row = self.lista_asignados.row(item)
            self.lista_asignados.takeItem(row)
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
        
        # Actualizar usuarios.json: buscar el estudiante por ID y verificar que sea de tipo "estudiante"
        path = os.path.join("data", "usuarios.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                usuarios_data = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo leer usuarios.json: {e}")
            return
        
        estudiante_encontrado = False
        for user in usuarios_data.get("users", []):
            if user.get("tipo") == "estudiante" and user.get("id") == id_est:
                estudiante_encontrado = True
                if "cursos_cursados" not in user or not isinstance(user["cursos_cursados"], list):
                    user["cursos_cursados"] = []
                # Agregar cada curso asignado, incluyendo el profesor asignante
                for curso in self.cursos_asignados:
                    curso_asignado = curso.copy()
                    curso_asignado["profe"] = self.profesor_email  # Asignar el profesor
                    user["cursos_cursados"].append(curso_asignado)
                break
        
        if not estudiante_encontrado:
            QMessageBox.warning(self, "Error", "El estudiante no está registrado en usuarios.json.")
            return
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(usuarios_data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Curso asignado al estudiante correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron guardar los cambios: {e}")
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 8px;
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
