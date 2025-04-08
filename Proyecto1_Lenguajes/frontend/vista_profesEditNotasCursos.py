import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
    QPushButton, QMessageBox, QLabel, QComboBox, QWidget, QScrollArea
)
from PyQt5.QtCore import Qt

def obtener_notas_por_tipo(tipo):
    tipo = tipo.lower()
    if tipo == "matematico":
        return {
            "tema1e1": 0.0,
            "tema2e1": 0.0,
            "tema3e1": 0.0,
            "examen1": 0.0,
            "tema1e2": 0.0,
            "tema2e2": 0.0,
            "tema3e2": 0.0,
            "examen2": 0.0,
            "tema1e3": 0.0,
            "tema2e3": 0.0,
            "tema3e3": 0.0,
            "examen3": 0.0,
            "totalExamenes": 0.0,
            "tareas": 0.0,
            "notaGeneral": 0.0
        }
    elif tipo == "carrera":
        return {
            "tema1p1": 0.0,
            "tema2p1": 0.0,
            "lab1t1": 0.0,
            "proyecto1": 0.0,
            "tema1p2": 0.0,
            "tema2p2": 0.0,
            "lab2t2": 0.0,
            "proyecto2": 0.0,
            "notaGeneralProyectos": 0.0,
            "notaGeneralLabs": 0.0,
            "notaTotal": 0.0
        }
    elif tipo == "ingles":
        return {
            "tema1e1": 0.0,
            "tema2e1": 0.0,
            "tema3e1": 0.0,
            "examen1": 0.0,
            "tema1e2": 0.0,
            "tema2e2": 0.0,
            "tema3e2": 0.0,
            "examen2": 0.0,
            "tema1e3": 0.0,
            "tema2e3": 0.0,
            "tema3e3": 0.0,
            "examen3": 0.0,
            "totalExamenes": 0.0,
            "tareas": 0.0,
            "notaGeneral": 0.0
        }
    elif tipo == "otro":
        return {
            "tema1t1": 0.0,
            "tema2t1": 0.0,
            "trabajo1": 0.0,
            "tema1t2": 0.0,
            "tema2t2": 0.0,
            "trabajo2": 0.0,
            "notaTrabajos": 0.0,
            "notaPresentacion": 0.0,
            "notaTotal": 0.0
        }
    else:
        return {}

class VentanaEditNotas(QDialog):
    def __init__(self, profesor_email):
        """
        Recibe el email del profesor para editar las notas de los estudiantes asignados 
        a sus cursos en el archivo 'cursoEstudianteProfesor.json'. Se espera que dicho 
        archivo tenga la estructura correcta.
        """
        super().__init__()
        self.profesor_email = profesor_email
        self.profesor_id = self.obtener_profesor_id()  # Se obtiene de usuarios.json
        if not self.profesor_id:
            QMessageBox.warning(self, "Error", "No se encontró el profesor en usuarios.json.")
            self.close()
            return
        self.data = {}         # Estructura completa de cursoEstudianteProfesor.json
        self.note_fields = {}  # Referencias a los QLineEdit para cada nota
        self.current_student_assignment = None  # Guarda la asignación del estudiante actual
        self.setWindowTitle("Editar Notas de un Curso")
        self.setFixedSize(800, 600)
        self.init_ui()
        self.apply_styles()
        self.load_data()

    def obtener_profesor_id(self):
        usuarios_path = os.path.join("data", "usuarios.json")
        if os.path.exists(usuarios_path):
            try:
                with open(usuarios_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for user in data.get("users", []):
                    if (user.get("tipo", "").lower() == "profesor" and 
                        user.get("email", "").strip().lower() == self.profesor_email.strip().lower()):
                        return user.get("id")
            except Exception as e:
                print(f"Error al leer usuarios.json: {e}")
        return None

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        header = QLabel("Editar Notas por Curso", self)
        header.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(header)
        
        # ComboBox para seleccionar curso
        form_layout = QFormLayout()
        self.combo_cursos = QComboBox()
        self.combo_cursos.currentIndexChanged.connect(self.course_selected)
        form_layout.addRow("Curso:", self.combo_cursos)
        self.main_layout.addLayout(form_layout)
        
        # ComboBox para seleccionar estudiante
        student_layout = QFormLayout()
        self.combo_estudiantes = QComboBox()
        self.combo_estudiantes.currentIndexChanged.connect(self.student_selected)
        student_layout.addRow("Estudiante:", self.combo_estudiantes)
        self.main_layout.addLayout(student_layout)
        
        # Contenedor para el formulario de notas: usamos un QVBoxLayout dedicado
        self.notes_placeholder = QVBoxLayout()
        self.notes_widget = QWidget()
        self.notes_widget.setLayout(self.notes_placeholder)
        self.main_layout.addWidget(self.notes_widget)
        
        # Botón para guardar cambios
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        btn_layout.addWidget(self.btn_guardar)
        self.main_layout.addLayout(btn_layout)
        
        self.setLayout(self.main_layout)

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
            QLineEdit {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QComboBox {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                padding: 4px;
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

    def load_data(self):
        """
        Carga la estructura desde 'cursoEstudianteProfesor.json' y filtra los cursos 
        donde el campo "profe" coincide con self.profesor_id.
        """
        path = os.path.join("data", "cursoEstudianteProfesor.json")
        self.data = {}
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al leer cursoEstudianteProfesor.json: {e}")
                return
        # Filtrar cursos donde el profesor asignado coincide con nuestro profesor_id.
        filtered_courses = []
        cursos_por_anio = self.data.get("cursos", {})
        for anio, semestres in cursos_por_anio.items():
            for semestre, cursos_list in semestres.items():
                for curso in cursos_list:
                    if curso.get("profe") == self.profesor_id:
                        curso.setdefault("anio", int(anio))
                        curso.setdefault("semestre", int(semestre))
                        filtered_courses.append(curso)
        self.populate_combo_cursos(filtered_courses)

    def populate_combo_cursos(self, courses):
        self.combo_cursos.clear()
        self.combo_cursos.addItem("-- Seleccionar Curso --", None)
        for curso in courses:
            display_text = (f"{curso.get('id')} - {curso.get('nombre')} ({curso.get('tipo')}) - "
                            f"Año: {curso.get('anio')}, Semestre: {curso.get('semestre')}")
            self.combo_cursos.addItem(display_text, curso)

    def course_selected(self):
        self.combo_estudiantes.clear()
        course = self.combo_cursos.currentData()
        if not course:
            return
        # Se espera que course["estudiantes"] sea una lista de asignaciones con la estructura:
        # { "id": <est_id>, "nombre": <est_nombre>, "notas": { ... } }
        estudiantes = course.get("estudiantes", [])
        if not estudiantes:
            QMessageBox.information(self, "Info", "No hay estudiantes asignados a este curso.")
            return
        for est in estudiantes:
            if isinstance(est, dict):
                student_id = est.get("id", "")
                student_name = est.get("nombre", "Desconocido")
                display_text = f"{student_id} - {student_name}"
                self.combo_estudiantes.addItem(display_text, est)
            else:
                # Por si la asignación no es un diccionario, se ignora o se muestra un mensaje.
                QMessageBox.warning(self, "Error", "Asignación de estudiante no válida.")
        # Una vez completado el combo de estudiantes, si hay al menos uno, se carga el formulario de notas.
        if self.combo_estudiantes.count() > 1:
            self.student_selected()

    def student_selected(self):
        self.ver_estudiante()

    def crear_formulario_notas(self, notas_dict):
        layout = QFormLayout()
        self.note_fields = {}
        for key, value in notas_dict.items():
            le = QLineEdit(str(value))
            layout.addRow(f"{key}:", le)
            self.note_fields[key] = le
        return layout

    def populate_formulario_notas(self, curso, student_assignment):
        # Se asume que student_assignment es un diccionario con claves: "id", "nombre", "notas"
        notas = student_assignment.get("notas")
        if notas is None or not isinstance(notas, dict):
            notas = obtener_notas_por_tipo(curso.get("tipo", ""))
            student_assignment["notas"] = notas
        # Si ya existe un formulario, eliminamos su widget para actualizarlo
        if hasattr(self, "form_notas_widget") and self.form_notas_widget:
            self.form_notas_widget.setParent(None)
        form_layout = self.crear_formulario_notas(notas)
        self.form_notas_widget = QWidget()
        self.form_notas_widget.setLayout(form_layout)
        # Limpiar el contenedor de notas antes de agregar el nuevo widget
        while self.notes_placeholder.count():
            item = self.notes_placeholder.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        self.notes_placeholder.addWidget(self.form_notas_widget)

    def ver_estudiante(self):
        student_item = self.combo_estudiantes.currentData()
        course = self.combo_cursos.currentData()
        if student_item and course:
            self.populate_formulario_notas(course, student_item)
        else:
            QMessageBox.warning(self, "Error", "Debe seleccionar un curso y un estudiante.")

    def guardar_cambios(self):
        course = self.combo_cursos.currentData()
        student_item = self.combo_estudiantes.currentData()
        if not course or not student_item:
            QMessageBox.warning(self, "Error", "Debe seleccionar un curso y un estudiante.")
            return
        student_id = student_item.get("id", "")
        nuevas_notas = {}
        for key, le in self.note_fields.items():
            try:
                nuevas_notas[key] = float(le.text().strip())
            except ValueError:
                nuevas_notas[key] = 0.0

        # Acceder a la asignación correcta en self.data
        anio_str = str(course.get("anio"))
        semestre_str = str(course.get("semestre"))
        asignaciones = self.data.get("cursos", {}).get(anio_str, {}).get(semestre_str, [])
        updated = False
        for a in asignaciones:
            if a.get("id") == course.get("id") and a.get("profe") == course.get("profe"):
                # Buscar el estudiante en la lista de asignados
                for est in a.get("estudiantes", []):
                    if est.get("id", "") == student_id:
                        est["notas"] = nuevas_notas
                        updated = True
                        break
                break

        if not updated:
            QMessageBox.warning(self, "Error", "No se encontró el registro del estudiante en el curso.")
            return

        path = os.path.join("data", "cursoEstudianteProfesor.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Los cambios han sido guardados correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron guardar los cambios: {e}")

    def editar_notas(self):
        self.ver_estudiante()

    def ejecutar_guardar(self):
        self.guardar_cambios()
