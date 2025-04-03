import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox, QPushButton,
    QListWidget, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt

class VentanaVerEstudiantesCursos(QDialog):
    def __init__(self, profesor_email):
        super().__init__()
        self.profesor_email = profesor_email
        self.setWindowTitle("Ver Cursos de Estudiantes")
        self.setFixedSize(1280, 400)
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulario para seleccionar al estudiante (solo se muestran los estudiantes con cursos de este profesor)
        form_layout = QFormLayout()
        self.combo_estudiante = QComboBox()
        self.cargar_estudiantes()
        form_layout.addRow("Estudiante:", self.combo_estudiante)
        layout.addLayout(form_layout)
        
        # Botón para cargar cursos asignados al estudiante seleccionado
        self.btn_ver = QPushButton("Ver Cursos")
        self.btn_ver.clicked.connect(self.ver_cursos)
        layout.addWidget(self.btn_ver)
        
        # Lista para mostrar los cursos asignados
        self.lista_cursos = QListWidget()
        layout.addWidget(self.lista_cursos)
        
        self.setLayout(layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #F4F7F6;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QLabel, QFormLayout QLabel {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                color: #333;
            }
            QComboBox {
                font-family: 'Segoe UI', sans-serif;
                font-size: 12pt;
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #ffffff;
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
    
    def cargar_estudiantes(self):
        """
        Carga los estudiantes de usuarios.json que tengan asignado al menos un curso
        impartido por el profesor (según su correo) y los agrega al QComboBox.
        """
        path = os.path.join("data", "usuarios.json")
        self.combo_estudiante.clear()
        estudiantes_filtrados = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for user in data.get("users", []):
                        if user.get("tipo") == "estudiante":
                            # Filtrar: incluir el estudiante solo si tiene al menos un curso con "profe" igual a profesor_email
                            cursos = user.get("cursos_cursados", [])
                            for curso in cursos:
                                if curso.get("profe") == self.profesor_email:
                                    estudiantes_filtrados.append(user)
                                    break
            except json.JSONDecodeError:
                estudiantes_filtrados = []
        if not estudiantes_filtrados:
            QMessageBox.information(self, "Info", "No se encontraron estudiantes con cursos asignados por este profesor.")
        for est in estudiantes_filtrados:
            display_text = f"{est.get('id')} - {est.get('nombre')}"
            self.combo_estudiante.addItem(display_text, est)
    
    def ver_cursos(self):
        """
        Muestra en la lista los cursos asignados al estudiante seleccionado, 
        filtrando solo aquellos cursos asignados por el profesor.
        """
        self.lista_cursos.clear()
        est_data = self.combo_estudiante.currentData()
        if not est_data:
            QMessageBox.warning(self, "Error", "No hay estudiante seleccionado.")
            return
        
        # Filtrar cursos asignados por este profesor
        cursos = [curso for curso in est_data.get("cursos_cursados", []) if curso.get("profe") == self.profesor_email]
        if not cursos:
            QMessageBox.information(self, "Info", "Este estudiante no tiene cursos asignados por este profesor.")
            return
        
        for curso in cursos:
            nombre = curso.get("nombre", "Desconocido")
            curso_id = curso.get("id", "")
            tipo = curso.get("tipo", "")
            # Preparar un string con las notas según el tipo
            notas = []
            if tipo.lower() == "matematico":
                notas = [
                    f"Ex1: {curso.get('nota_examen1', 0.0)}",
                    f"Ex2: {curso.get('nota_examen2', 0.0)}",
                    f"Ex3: {curso.get('nota_examen3', 0.0)}",
                    f"Tareas: {curso.get('nota_tareas', 0.0)}"
                ]
            elif tipo.lower() == "carrera":
                notas = [
                    f"Proy1: {curso.get('nota_proyecto1', 0.0)}",
                    f"Proy2: {curso.get('nota_proyecto2', 0.0)}",
                    f"Lab: {curso.get('nota_laboratorios', 0.0)}"
                ]
            elif tipo.lower() == "ingles":
                notas = [
                    f"Ex1: {curso.get('nota_examen1', 0.0)}",
                    f"Ex2: {curso.get('nota_examen2', 0.0)}",
                    f"Lab: {curso.get('nota_laboratorios', 0.0)}",
                    f"Tareas: {curso.get('nota_tareas', 0.0)}"
                ]
            elif tipo.lower() in ["otrocursos", "otrocurso"]:
                notas = [
                    f"Trab1: {curso.get('nota_trabajo1', 0.0)}",
                    f"Trab2: {curso.get('nota_trabajo2', 0.0)}",
                    f"Trab3: {curso.get('nota_trabajo3', 0.0)}",
                    f"Tareas: {curso.get('nota_tareas', 0.0)}"
                ]
            notas_text = ", ".join(notas) if notas else "Sin notas"
            item_text = f"{curso_id} - {nombre} | Notas: {notas_text}"
            self.lista_cursos.addItem(item_text)

