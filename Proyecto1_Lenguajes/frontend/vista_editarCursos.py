import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QMessageBox
)

class VentanaEditarCursos(QDialog):
    def __init__(self, profesor_email):
        super().__init__()
        self.setWindowTitle("Editar Curso")
        self.setFixedSize(400, 300)
        self.profesor_email = profesor_email  # Correo del profesor para identificar su registro en usuarios.json
        self.init_ui()
        self.apply_styles()
        # Estos serán llenados al buscar el curso
        self.bloque_encontrado = None
        self.indice_curso = None
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulario de búsqueda
        form_busqueda = QFormLayout()
        self.input_anio = QLineEdit()
        self.input_anio.setPlaceholderText("Ej: 2000")
        form_busqueda.addRow("Año:", self.input_anio)
        
        self.input_semestre = QLineEdit()
        self.input_semestre.setPlaceholderText("Ej: 1 o 2")
        form_busqueda.addRow("Semestre:", self.input_semestre)
        
        self.input_curso_id_buscar = QLineEdit()
        self.input_curso_id_buscar.setPlaceholderText("ID del Curso a editar")
        form_busqueda.addRow("ID del Curso:", self.input_curso_id_buscar)
        
        layout.addLayout(form_busqueda)
        
        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_curso)
        layout.addWidget(btn_buscar)
        
        # Formulario de edición (solo se edita nombre e ID)
        form_edicion = QFormLayout()
        self.input_nombre = QLineEdit()
        form_edicion.addRow("Nombre del Curso:", self.input_nombre)
        
        self.input_curso_id_editar = QLineEdit()
        form_edicion.addRow("Nuevo ID del Curso:", self.input_curso_id_editar)
        
        layout.addLayout(form_edicion)
        
        # Botones de Guardar y Cancelar
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_edicion)
        btn_layout.addWidget(btn_guardar)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancelar)
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
    
    def buscar_curso(self):
        """Busca el curso en usuarios.json según año, semestre y ID ingresados."""
        anio_str = self.input_anio.text().strip()
        semestre_str = self.input_semestre.text().strip()
        curso_id = self.input_curso_id_buscar.text().strip()
        
        if not anio_str or not semestre_str or not curso_id:
            QMessageBox.warning(self, "Error", "Ingrese año, semestre y ID del curso para buscar.")
            return
        
        try:
            anio = int(anio_str)
            semestre = int(semestre_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "Año y semestre deben ser numéricos.")
            return
        
        path = os.path.join("data", "usuarios.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                usuarios_data = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo leer usuarios.json: {e}")
            return
        
        curso_encontrado = False
        
        # Buscar el registro del profesor
        for user in usuarios_data.get("users", []):
            if user.get("email") == self.profesor_email and user.get("tipo") == "profesor":
                # Revisar cada bloque en "anos"
                if "anos" in user and isinstance(user["anos"], list):
                    for bloque in user["anos"]:
                        if bloque.get("anio") == anio and bloque.get("semestre") == semestre:
                            # Buscar el curso dentro de este bloque
                            cursos = bloque.get("cursos", [])
                            for idx, curso in enumerate(cursos):
                                if curso.get("id") == curso_id:
                                    # Se encontró el curso: llenamos los campos de edición
                                    self.input_nombre.setText(curso.get("nombre", ""))
                                    self.input_curso_id_editar.setText(curso.get("id", ""))
                                    # Guardamos referencias para actualizar: el bloque y el índice del curso
                                    self.bloque_encontrado = bloque
                                    self.indice_curso = idx
                                    curso_encontrado = True
                                    break
                        if curso_encontrado:
                            break
                break
        
        if curso_encontrado:
            QMessageBox.information(self, "Búsqueda", "Curso encontrado. Modifique los datos y presione Guardar.")
        else:
            QMessageBox.information(self, "Búsqueda", "No se encontró el curso con esos parámetros.")
    
    def guardar_edicion(self):
        """Guarda los cambios realizados en el curso editado."""
        if self.bloque_encontrado is None or self.indice_curso is None:
            QMessageBox.warning(self, "Error", "No se ha cargado un curso para editar.")
            return

        nuevo_nombre = self.input_nombre.text().strip()
        nuevo_id = self.input_curso_id_editar.text().strip()
        if not nuevo_nombre or not nuevo_id:
            QMessageBox.warning(self, "Error", "El nombre y el ID son obligatorios.")
            return

        # Actualizar la información del curso en la referencia obtenida
        self.bloque_encontrado["cursos"][self.indice_curso]["nombre"] = nuevo_nombre
        self.bloque_encontrado["cursos"][self.indice_curso]["id"] = nuevo_id

        # Abrir y actualizar el archivo usuarios.json
        path = os.path.join("data", "usuarios.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                usuarios_data = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo leer usuarios.json: {e}")
            return

        # Actualizamos el bloque del curso en usuarios_data
        profesor_actualizado = False
        try:
            for user in usuarios_data.get("users", []):
                if user.get("email") == self.profesor_email and user.get("tipo") == "profesor":
                    if "anos" in user and isinstance(user["anos"], list):
                        for bloque in user["anos"]:
                            if (bloque.get("anio") == int(self.input_anio.text().strip()) and 
                                bloque.get("semestre") == int(self.input_semestre.text().strip())):
                                # Actualizamos el curso cuyo ID original coincide con el ID de búsqueda
                                for curso in bloque.get("cursos", []):
                                    if curso.get("id") == self.input_curso_id_buscar.text().strip():
                                        curso["nombre"] = nuevo_nombre
                                        curso["id"] = nuevo_id
                                        profesor_actualizado = True
                                        break
                    break
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al actualizar la información: {e}")
            return

        if not profesor_actualizado:
            QMessageBox.warning(self, "Error", "No se encontró el registro del profesor o el curso a editar.")
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(usuarios_data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Guardado", "Curso editado exitosamente.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar los cambios: {e}")