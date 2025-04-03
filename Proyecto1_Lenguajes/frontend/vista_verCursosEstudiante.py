import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt

class VentanaCursos(QDialog):
    def __init__(self, estudiante_email):
        """
        Recibe el email del estudiante que ha iniciado sesión y muestra
        los cursos asignados junto con las notas.
        """
        super().__init__()
        self.estudiante_email = estudiante_email
        self.estudiante_data = None
        self.setWindowTitle("Mis Cursos y Notas")
        self.setFixedSize(700, 500)
        self.init_ui()
        self.cargar_estudiante()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        header = QLabel("Mis Cursos y Notas", self)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        self.lista_cursos = QListWidget()
        layout.addWidget(self.lista_cursos)
        
        self.setLayout(layout)
    
    def cargar_estudiante(self):
        """
        Busca en usuarios.json el registro del estudiante cuyo email coincide.
        """
        path = os.path.join("data", "usuarios.json")
        if not os.path.exists(path):
            QMessageBox.warning(self, "Error", "No existe el archivo usuarios.json.")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo leer usuarios.json: {e}")
            return
        
        # Buscar el estudiante (comparación ignorando mayúsculas y espacios)
        for user in data.get("users", []):
            if user.get("tipo") == "estudiante" and user.get("email", "").strip().lower() == self.estudiante_email.strip().lower():
                self.estudiante_data = user
                break
        
        if not self.estudiante_data:
            QMessageBox.information(self, "Info", "No se encontró tu información en usuarios.json.")
            return
        
        self.refrescar_lista()
    
    def refrescar_lista(self):
        """
        Muestra en el QListWidget los cursos asignados al estudiante con sus notas.
        """
        self.lista_cursos.clear()
        if not self.estudiante_data:
            return
        
        cursos = self.estudiante_data.get("cursos_cursados", [])
        if not cursos:
            self.lista_cursos.addItem("No tienes cursos asignados.")
            return
        
        for curso in cursos:
            # Extraer información básica
            id_curso = curso.get("id", "Desconocido")
            nombre = curso.get("nombre", "Sin Nombre")
            tipo = curso.get("tipo", "N/A").lower()
            
            # Preparar el string de notas según el tipo de curso
            notas = []
            if tipo == "matematico":
                notas = [
                    f"Ex1: {curso.get('nota_examen1', 0.0)}",
                    f"Ex2: {curso.get('nota_examen2', 0.0)}",
                    f"Ex3: {curso.get('nota_examen3', 0.0)}",
                    f"Tareas: {curso.get('nota_tareas', 0.0)}",
                    f"Total: {curso.get('nota_total', 0.0)}"
                ]
            elif tipo == "carrera":
                notas = [
                    f"Proy1: {curso.get('nota_proyecto1', 0.0)}",
                    f"Proy2: {curso.get('nota_proyecto2', 0.0)}",
                    f"Lab: {curso.get('nota_laboratorios', 0.0)}",
                    f"Total: {curso.get('nota_total', 0.0)}"
                ]
            elif tipo == "ingles":
                notas = [
                    f"Ex1: {curso.get('nota_examen1', 0.0)}",
                    f"Ex2: {curso.get('nota_examen2', 0.0)}",
                    f"Lab: {curso.get('nota_laboratorios', 0.0)}",
                    f"Tareas: {curso.get('nota_tareas', 0.0)}",
                    f"Total: {curso.get('nota_total', 0.0)}"
                ]
            else:  # Otros
                notas = [
                    f"Trab1: {curso.get('nota_trabajo1', 0.0)}",
                    f"Trab2: {curso.get('nota_trabajo2', 0.0)}",
                    f"Trab3: {curso.get('nota_trabajo3', 0.0)}",
                    f"Tareas: {curso.get('nota_tareas', 0.0)}",
                    f"Total: {curso.get('nota_total', 0.0)}"
                ]
            notas_text = ", ".join(notas)
            item_text = f"{id_curso} - {nombre} ({tipo.capitalize()}) | Notas: {notas_text}"
            self.lista_cursos.addItem(item_text)
