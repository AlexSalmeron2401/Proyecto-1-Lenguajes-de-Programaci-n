import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt

class VentanaCursos(QDialog):
    def __init__(self, estudiante_email):
        """
        Recibe el email del estudiante y muestra (en modo sólo lectura)
        los cursos asignados (tomados desde cursoEstudianteProfesor.json) junto con
        la información del curso y las notas del estudiante.
        """
        super().__init__()
        self.estudiante_email = estudiante_email
        self.student_id = self.obtener_estudiante_id()
        if not self.student_id:
            QMessageBox.warning(self, "Error", "No se encontró información del estudiante en usuarios.json.")
            self.close()
            return
        self.filtered_courses = []  # Cursos asignados al estudiante
        self.data = {}  # Estructura completa del archivo cursoEstudianteProfesor.json
        self.setWindowTitle("Mis Cursos y Notas")
        self.setFixedSize(800, 600)
        self.init_ui()
        self.load_data()
        self.populate_combo_cursos()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        header = QLabel("Mis Cursos y Notas", self)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # ComboBox para seleccionar el curso asignado
        self.combo_cursos = QComboBox()
        self.combo_cursos.currentIndexChanged.connect(self.course_changed)
        main_layout.addWidget(self.combo_cursos)
        
        # Formulario para mostrar los detalles del curso
        form_layout = QFormLayout()
        self.le_id = QLineEdit()
        self.le_id.setReadOnly(True)
        form_layout.addRow("ID:", self.le_id)
        
        self.le_nombre = QLineEdit()
        self.le_nombre.setReadOnly(True)
        form_layout.addRow("Nombre:", self.le_nombre)
        
        self.le_tipo = QLineEdit()
        self.le_tipo.setReadOnly(True)
        form_layout.addRow("Tipo:", self.le_tipo)
        
        self.le_profe = QLineEdit()
        self.le_profe.setReadOnly(True)
        form_layout.addRow("Profesor (ID):", self.le_profe)
        
        self.le_anio = QLineEdit()
        self.le_anio.setReadOnly(True)
        form_layout.addRow("Año:", self.le_anio)
        
        self.le_semestre = QLineEdit()
        self.le_semestre.setReadOnly(True)
        form_layout.addRow("Semestre:", self.le_semestre)
        
        self.te_notas = QTextEdit()
        self.te_notas.setReadOnly(True)
        form_layout.addRow("Notas:", self.te_notas)
        
        main_layout.addLayout(form_layout)
        
        # Botón de Cerrar
        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.clicked.connect(self.close)
        main_layout.addWidget(self.btn_cerrar)
        
        self.setLayout(main_layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #F4F7F6;
            }
            QLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                color: #333;
            }
            QLineEdit, QComboBox, QTextEdit {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                padding: 4px;
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
    
    def obtener_estudiante_id(self):
        """
        Busca en usuarios.json el estudiante cuyo email coincide
        y retorna su ID.
        """
        path = os.path.join("data", "usuarios.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for user in data.get("users", []):
                if user.get("tipo", "").lower() == "estudiante" and \
                   user.get("email", "").strip().lower() == self.estudiante_email.strip().lower():
                    return user.get("id")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar usuarios.json: {e}")
        return None

    def load_data(self):
        """
        Carga la información del archivo 'cursoEstudianteProfesor.json'
        y filtra los cursos en los que el estudiante está asignado.
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
        else:
            QMessageBox.warning(self, "Error", "No se encontró el archivo cursoEstudianteProfesor.json.")
            return

        self.filtered_courses = []
        cursos_por_anio = self.data.get("cursos", {})
        for anio, semestres in cursos_por_anio.items():
            for semestre, cursos_list in semestres.items():
                for curso in cursos_list:
                    estudiantes = curso.get("estudiantes", [])
                    for asignacion in estudiantes:
                        # Cada asignación se espera que sea un diccionario con las claves "id", "nombre" y "notas"
                        if isinstance(asignacion, dict) and asignacion.get("id") == self.student_id:
                            # Aseguramos que el curso tenga las claves "anio" y "semestre"
                            curso.setdefault("anio", int(anio))
                            curso.setdefault("semestre", int(semestre))
                            self.filtered_courses.append(curso)
                            break

    def populate_combo_cursos(self):
        self.combo_cursos.clear()
        self.combo_cursos.addItem("-- Seleccionar Curso --", None)
        if not self.filtered_courses:
            self.combo_cursos.addItem("No tienes cursos asignados", None)
            return
        for curso in self.filtered_courses:
            display_text = (f"{curso.get('id')} - {curso.get('nombre')} ({curso.get('tipo').capitalize()}) | "
                            f"Profe: {curso.get('profe')} | Año: {curso.get('anio')}, Semestre: {curso.get('semestre')}")
            self.combo_cursos.addItem(display_text, curso)
    
    def course_changed(self):
        """
        Cuando el usuario selecciona un curso del combo, actualizar
        los campos de información del curso y las notas.
        """
        curso = self.combo_cursos.currentData()
        if not curso:
            self.le_id.clear()
            self.le_nombre.clear()
            self.le_tipo.clear()
            self.le_profe.clear()
            self.le_anio.clear()
            self.le_semestre.clear()
            self.te_notas.clear()
            return

        # Actualizar campos de información
        self.le_id.setText(str(curso.get("id", "")))
        self.le_nombre.setText(curso.get("nombre", ""))
        self.le_tipo.setText(curso.get("tipo", "").capitalize())
        self.le_profe.setText(str(curso.get("profe", "")))
        self.le_anio.setText(str(curso.get("anio", "")))
        self.le_semestre.setText(str(curso.get("semestre", "")))
        
        # Buscar las notas de la asignación del estudiante en el curso
        notas = {}
        for asignacion in curso.get("estudiantes", []):
            # Se asume que cada asignación es un diccionario con las claves "id", "nombre", y "notas"
            if isinstance(asignacion, dict) and asignacion.get("id") == self.student_id:
                notas = asignacion.get("notas", {})
                break
        if not notas:
            self.te_notas.setPlainText("Sin notas")
        else:
            # Formatear las notas para mostrar (cada línea: clave: valor)
            notas_text = "\n".join([f"{k}: {v}" for k, v in notas.items()])
            self.te_notas.setPlainText(notas_text)

    def showEvent(self, event):
        super().showEvent(event)
        # Llenar el combo de cursos cuando se muestre la ventana
        self.populate_combo_cursos()

# Nota: Este módulo se invoca desde otro, por lo que no se incluye el bloque if __name__ == '__main__'
