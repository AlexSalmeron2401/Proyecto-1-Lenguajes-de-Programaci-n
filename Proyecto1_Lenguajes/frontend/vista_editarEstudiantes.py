import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QListWidget, QPushButton, QLabel, QComboBox, 
    QMessageBox
)
from PyQt5.QtCore import Qt

class VentanaEditarEstudiantes(QDialog):
    def __init__(self, profesor_email=None):
        """
        Si 'profesor_email' es None, no se cargan cursos disponibles.
        Si se pasa el correo del profesor, se cargan sus cursos para poder asignarlos al estudiante.
        """
        super().__init__()
        self.setWindowTitle("Editar Estudiante (Agregar o Borrar Cursos)")
        self.setFixedSize(600, 500)
        
        self.profesor_email = profesor_email
        self.estudiante_data = None   # Contendrá la información del estudiante una vez cargado
        self.init_ui()
        self.apply_styles()
        
        # Se habilita la sección de agregar cursos solo si se proporciona profesor_email
        if self.profesor_email:
            self.load_cursos_profesor()
            self.populate_combo_cursos()
        else:
            self.combo_cursos.setEnabled(False)
            self.btn_agregar_curso.setEnabled(False)
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # --- Buscar estudiante por ID ---
        form_buscar = QFormLayout()
        self.input_id_buscar = QLineEdit()
        self.input_id_buscar.setPlaceholderText("Ej: 2019")
        form_buscar.addRow("ID del Estudiante:", self.input_id_buscar)
        
        btn_buscar = QPushButton("Buscar Estudiante")
        btn_buscar.clicked.connect(self.buscar_estudiante)
        
        layout.addLayout(form_buscar)
        layout.addWidget(btn_buscar)
        
        # --- Editar nombre y ver/borrar cursos ---
        form_est = QFormLayout()
        self.input_nombre = QLineEdit()
        form_est.addRow("Nombre del Estudiante:", self.input_nombre)
        layout.addLayout(form_est)
        
        layout.addWidget(QLabel("Cursos Asignados:"))
        self.lista_cursos_asignados = QListWidget()
        layout.addWidget(self.lista_cursos_asignados)
        
        btn_borrar_curso = QPushButton("Borrar Curso Seleccionado")
        btn_borrar_curso.clicked.connect(self.borrar_curso_asignado)
        layout.addWidget(btn_borrar_curso)
        
        # --- Agregar cursos (sin notas) ---
        layout.addWidget(QLabel("Agregar Curso (Profesor):"))
        self.combo_cursos = QComboBox()
        layout.addWidget(self.combo_cursos)
        
        self.btn_agregar_curso = QPushButton("Agregar Curso")
        self.btn_agregar_curso.clicked.connect(self.agregar_curso_nuevo)
        layout.addWidget(self.btn_agregar_curso)
        
        # --- Botones finales ---
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        self.btn_guardar.setEnabled(False)
        btn_layout.addWidget(self.btn_guardar)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addLayout(btn_layout)
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
    
    def buscar_estudiante(self):
        est_id = self.input_id_buscar.text().strip()
        if not est_id:
            QMessageBox.warning(self, "Error", "Ingrese el ID del estudiante.")
            return
        
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
        
        encontrado = False
        for user in data.get("users", []):
            if user.get("tipo") == "estudiante" and user.get("id") == est_id:
                # Verificar que el estudiante tenga asignado al menos un curso de este profesor
                cursos = user.get("cursos_cursados", [])
                if any(curso.get("profe") == self.profesor_email for curso in cursos):
                    self.estudiante_data = user
                    encontrado = True
                else:
                    QMessageBox.information(self, "Info", 
                        "El estudiante no tiene cursos asignados por este profesor.")
                break
        
        if not encontrado:
            QMessageBox.information(self, "Info", 
                "No se encontró un estudiante con ese ID relacionado con este profesor.")
            return
        
        self.input_nombre.setText(self.estudiante_data.get("nombre", ""))
        self.refrescar_lista_cursos()
        self.btn_guardar.setEnabled(True)
    
    def refrescar_lista_cursos(self):
        self.lista_cursos_asignados.clear()
        if not self.estudiante_data:
            return
        for c in self.estudiante_data.get("cursos_cursados", []):
            # Mostrar solo cursos asignados por este profesor
            if c.get("profe") == self.profesor_email:
                item_text = f"{c.get('id')} - {c.get('nombre')} ({c.get('tipo')})"
                self.lista_cursos_asignados.addItem(item_text)
    
    def borrar_curso_asignado(self):
        if not self.estudiante_data:
            QMessageBox.warning(self, "Error", "Debe cargar primero un estudiante.")
            return
        
        item = self.lista_cursos_asignados.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Seleccione un curso para borrarlo.")
            return
        
        texto = item.text()
        curso_id = texto.split(" - ")[0]
        cursos = self.estudiante_data.get("cursos_cursados", [])
        
        new_cursos = [cc for cc in cursos if cc.get("id") != curso_id or cc.get("profe") != self.profesor_email]
        if len(new_cursos) < len(cursos):
            self.estudiante_data["cursos_cursados"] = new_cursos
            self.refrescar_lista_cursos()
            QMessageBox.information(self, "Borrado", "Curso eliminado de la lista en memoria.")
        else:
            QMessageBox.information(self, "Info", "No se encontró ese curso en la lista del estudiante.")
    
    def guardar_cambios(self):
        if not self.estudiante_data:
            QMessageBox.warning(self, "Error", "No hay estudiante cargado.")
            return
        
        nuevo_nombre = self.input_nombre.text().strip()
        if not nuevo_nombre:
            QMessageBox.warning(self, "Error", "El nombre del estudiante no puede estar vacío.")
            return
        
        self.estudiante_data["nombre"] = nuevo_nombre
        
        path = os.path.join("data", "usuarios.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo leer usuarios.json: {e}")
            return
        
        actualizado = False
        for user in data.get("users", []):
            if user.get("tipo") == "estudiante" and user.get("id") == self.estudiante_data.get("id"):
                user["nombre"] = self.estudiante_data.get("nombre", "")
                # Actualizar solo los cursos asignados por este profesor
                user["cursos_cursados"] = [curso for curso in self.estudiante_data.get("cursos_cursados", [])
                                          if curso.get("profe") == self.profesor_email]
                actualizado = True
                break
        
        if not actualizado:
            QMessageBox.warning(self, "Error", "No se encontró el registro del estudiante para actualizar.")
            return
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Cambios guardados correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar la información: {e}")
    
    # --- Métodos para agregar un curso nuevo (sin notas) ---
    def load_cursos_profesor(self):
        self.cursos_info = []
        if not self.profesor_email:
            return
        path = os.path.join("data", "usuarios.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for user in data.get("users", []):
                    if user.get("tipo") == "profesor" and user.get("email") == self.profesor_email:
                        for bloque in user.get("anos", []):
                            anio = bloque.get("anio")
                            semestre = bloque.get("semestre")
                            for c in bloque.get("cursos", []):
                                ccopy = c.copy()
                                ccopy["anio"] = anio
                                ccopy["semestre"] = semestre
                                self.cursos_info.append(ccopy)
                        break
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al cargar cursos del profesor: {e}")
    
    def populate_combo_cursos(self):
        self.combo_cursos.clear()
        for curso in self.cursos_info:
            disp = f"Año: {curso.get('anio')}, Sem: {curso.get('semestre')} - {curso.get('id')} - {curso.get('nombre')} ({curso.get('tipo')})"
            self.combo_cursos.addItem(disp, curso)
    
    def agregar_curso_nuevo(self):
        if not self.estudiante_data:
            QMessageBox.warning(self, "Error", "Primero busque al estudiante que desea editar.")
            return
        
        idx = self.combo_cursos.currentIndex()
        if idx < 0:
            QMessageBox.warning(self, "Error", "No hay curso seleccionado.")
            return
        
        curso = self.combo_cursos.itemData(idx)
        # Se hace una copia y se setean las notas a 0.0
        curso_nuevo = curso.copy()
        tipo = curso_nuevo.get("tipo", "").lower()
        
        if tipo == "matematico":
            curso_nuevo["nota_examen1"] = 0.0
            curso_nuevo["nota_examen2"] = 0.0
            curso_nuevo["nota_examen3"] = 0.0
            curso_nuevo["nota_tareas"]  = 0.0
        elif tipo == "carrera":
            curso_nuevo["nota_proyecto1"]   = 0.0
            curso_nuevo["nota_proyecto2"]   = 0.0
            curso_nuevo["nota_laboratorios"] = 0.0
        elif tipo == "ingles":
            curso_nuevo["nota_examen1"]     = 0.0
            curso_nuevo["nota_examen2"]     = 0.0
            curso_nuevo["nota_laboratorios"]= 0.0
            curso_nuevo["nota_tareas"]      = 0.0
        else:
            curso_nuevo["nota_trabajo1"] = 0.0
            curso_nuevo["nota_trabajo2"] = 0.0
            curso_nuevo["nota_trabajo3"] = 0.0
            curso_nuevo["nota_tareas"]   = 0.0
        
        curso_nuevo["nota_total"] = 0.0
        curso_nuevo["profe"] = self.profesor_email
        
        # Agregarlo a la lista de cursos del estudiante
        cursos_estudiante = self.estudiante_data.get("cursos_cursados", [])
        cursos_estudiante.append(curso_nuevo)
        self.estudiante_data["cursos_cursados"] = cursos_estudiante
        
        self.refrescar_lista_cursos()
        QMessageBox.information(self, "Curso Agregado", 
            "Se agregó el curso con notas en 0.0 al estudiante en memoria. Luego presione 'Guardar Cambios'.")
