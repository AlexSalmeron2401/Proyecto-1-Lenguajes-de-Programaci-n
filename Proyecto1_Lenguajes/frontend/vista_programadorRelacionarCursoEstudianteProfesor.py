import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QComboBox, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

class VentanaProgramadorRelacionarCursoEstudianteProfesor(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Relacionar Curso a Estudiante - Vista Programador")
        self.setFixedSize(600, 500)
        self.init_ui()
        self.apply_styles()
        self.load_data()  # Carga la información desde los archivos

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header = QLabel("Relacionar Curso a Estudiante", self)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        # Formulario con dos ComboBox: uno para estudiantes y otro para cursos
        form_layout = QFormLayout()
        self.combo_estudiantes = QComboBox()
        form_layout.addRow("Estudiante:", self.combo_estudiantes)

        self.combo_cursos = QComboBox()
        form_layout.addRow("Curso:", self.combo_cursos)

        layout.addLayout(form_layout)

        # Botón para asignar el curso
        self.btn_asignar = QPushButton("Asignar Curso")
        self.btn_asignar.clicked.connect(self.asignar_curso)
        layout.addWidget(self.btn_asignar)

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
            QComboBox {
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

    def load_data(self):
        """
        Carga la información de cursos y estudiantes desde:
          - Los cursos se obtienen desde 'cursoProfesor.json'.
          - Los estudiantes se obtienen de 'usuarios.json' (filtrando solo a los de tipo "estudiante").
        """
        # Cargar cursos desde cursoProfesor.json
        cursos_path = os.path.join("data", "cursoProfesor.json")
        self.cursos = []
        if os.path.exists(cursos_path):
            try:
                with open(cursos_path, "r", encoding="utf-8") as f:
                    data_cursos = json.load(f)
                    self.cursos = data_cursos.get("cursos", [])
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al leer cursoProfesor.json: {e}")
        else:
            QMessageBox.warning(self, "Error", "No se encontró el archivo cursoProfesor.json.")

        # Cargar estudiantes desde usuarios.json
        usuarios_path = os.path.join("data", "usuarios.json")
        self.estudiantes = []
        if os.path.exists(usuarios_path):
            try:
                with open(usuarios_path, "r", encoding="utf-8") as f:
                    data_usuarios = json.load(f)
                    for user in data_usuarios.get("users", []):
                        if user.get("tipo", "").lower() == "estudiante":
                            self.estudiantes.append(user)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al leer usuarios.json: {e}")
        else:
            QMessageBox.warning(self, "Error", "No se encontró el archivo usuarios.json.")

        self.populate_combo_estudiantes()
        self.populate_combo_cursos(self.cursos)

    def populate_combo_estudiantes(self):
        self.combo_estudiantes.clear()
        for est in self.estudiantes:
            display_text = f"{est.get('id')} - {est.get('nombre')}"
            self.combo_estudiantes.addItem(display_text, est)

    def populate_combo_cursos(self, cursos):
        self.combo_cursos.clear()
        self.combo_cursos.addItem("-- Seleccionar Curso --", None)
        for curso in cursos:
            display_text = (f"{curso.get('id')} - {curso.get('nombre')} ({curso.get('tipo')}) - "
                            f"Año: {curso.get('anio')}, Semestre: {curso.get('semestre')}")
            self.combo_cursos.addItem(display_text, curso)

    def obtener_notas_por_tipo(self, tipo):
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
                "totaTotal": 0.0
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

    def asignar_curso(self):
        """
        Asigna el curso seleccionado al estudiante y actualiza el archivo cursoEstudianteProfesor.json.
        Se actualiza:
          - En el estudiante (clave "cursos_cursados"), se añade el curso (con campo "profe" y diccionario "notas").
          - En el curso, se añade el estudiante a la lista "estudiantes".
        La salida esperada es similar a:
        {
            "cursos": {
                "2020": {
                    "1": [
                        { curso asignado con estudiantes, etc. }
                    ]
                }
            }
        }
        """
        estudiante = self.combo_estudiantes.currentData()
        curso = self.combo_cursos.currentData()

        if not estudiante or not curso:
            QMessageBox.warning(self, "Error", "Debe seleccionar un estudiante y un curso.")
            return

        # Preparar la asignación para el estudiante
        nuevo_curso_est = curso.copy()
        asignacion_est = {
            "id": nuevo_curso_est.get("id"),
            "nombre": nuevo_curso_est.get("nombre"),
            "tipo": nuevo_curso_est.get("tipo"),
            "anio": nuevo_curso_est.get("anio"),
            "semestre": nuevo_curso_est.get("semestre"),
            "profe": nuevo_curso_est.get("profe"),
            "notas": self.obtener_notas_por_tipo(nuevo_curso_est.get("tipo", ""))
        }

        # Actualizar la asignación en el estudiante: agregar a "cursos_cursados"
        if "cursos_cursados" not in estudiante or not isinstance(estudiante["cursos_cursados"], list):
            estudiante["cursos_cursados"] = []
        if any(c.get("id") == asignacion_est.get("id") and c.get("profe") == asignacion_est.get("profe")
               for c in estudiante["cursos_cursados"]):
            QMessageBox.information(self, "Info", "El estudiante ya tiene asignado este curso con ese profesor. Se actualizarán las notas a 0.0.")
            for i, c in enumerate(estudiante["cursos_cursados"]):
                if c.get("id") == asignacion_est.get("id") and c.get("profe") == asignacion_est.get("profe"):
                    estudiante["cursos_cursados"][i]["notas"] = asignacion_est["notas"]
                    break
        else:
            estudiante["cursos_cursados"].append(asignacion_est)

        # Actualizar la asignación en el curso en cursoEstudianteProfesor.json
        asignaciones_path = os.path.join("data", "cursoEstudianteProfesor.json")
        if os.path.exists(asignaciones_path):
            try:
                with open(asignaciones_path, "r", encoding="utf-8") as f:
                    asignaciones_data = json.load(f)
            except json.JSONDecodeError:
                asignaciones_data = {"cursos": {}}
        else:
            asignaciones_data = {"cursos": {}}

        anio_str = str(nuevo_curso_est.get("anio"))
        semestre_str = str(nuevo_curso_est.get("semestre"))
        if anio_str not in asignaciones_data["cursos"]:
            asignaciones_data["cursos"][anio_str] = {}
        if semestre_str not in asignaciones_data["cursos"][anio_str]:
            asignaciones_data["cursos"][anio_str][semestre_str] = []

        asignaciones_semestre = asignaciones_data["cursos"][anio_str][semestre_str]
        found_in_asignaciones = False
        for a in asignaciones_semestre:
            if a.get("id") == nuevo_curso_est.get("id") and a.get("profe") == nuevo_curso_est.get("profe"):
                # Verificar duplicados en la lista de estudiantes asignados
                if "estudiantes" not in a or not isinstance(a["estudiantes"], list):
                    a["estudiantes"] = []
                if any(est.get("id") == estudiante.get("id") for est in a["estudiantes"]):
                    QMessageBox.information(self, "Info", "La asignación ya existe en cursoEstudianteProfesor.json.")
                    return
                else:
                    a.setdefault("estudiantes", []).append({
                        "id": estudiante.get("id"),
                        "nombre": estudiante.get("nombre"),
                        "notas": asignacion_est["notas"]
                    })
                found_in_asignaciones = True
                break
        if not found_in_asignaciones:
            asignacion = nuevo_curso_est.copy()
            asignacion["estudiantes"] = [{
                "id": estudiante.get("id"),
                "nombre": estudiante.get("nombre"),
                "notas": asignacion_est["notas"]
            }]
            asignaciones_semestre.append(asignacion)

        try:
            with open(asignaciones_path, "w", encoding="utf-8") as f:
                json.dump(asignaciones_data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Curso asignado correctamente al estudiante y actualizado en el curso.")
            print("Nueva estructura de cursoEstudianteProfesor.json:")
            print(json.dumps(asignaciones_data, indent=4, ensure_ascii=False))
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudieron guardar los cambios: {e}")
