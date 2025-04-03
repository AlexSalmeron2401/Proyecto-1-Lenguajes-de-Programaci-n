import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QListWidget, QPushButton, QLabel, QComboBox, 
    QMessageBox
)
from PyQt5.QtCore import Qt

class VentanaEditarDatosEstudiante(QDialog):
    def __init__(self, estudiante_email):
        """
        Recibe el email del estudiante para cargar sus datos y permitir la edición.
        """
        super().__init__()
        self.estudiante_email = estudiante_email
        self.estudiante_data = None   # Se llenará con los datos del estudiante de usuarios.json
        self.profesores = []          # Lista de profesores (todos) de usuarios.json
        self.cursos_info = []         # Cursos extraídos de la información de cada profesor
        self.cursos_profesor = []     # Cursos del profesor seleccionado (temporal)
        self.setWindowTitle("Editar Mi Información")
        self.setFixedSize(700, 600)
        
        self.init_ui()
        self.apply_styles()
        self.cargar_estudiante()      # Carga los datos del estudiante
        self.cargar_profesores()      # Carga la lista de profesores para elegir cursos
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # --- Encabezado ---
        header = QLabel("Editar Datos Personales y Cursos", self)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # --- Datos Personales ---
        form_personales = QFormLayout()
        self.input_nombre = QLineEdit()
        self.input_email = QLineEdit()
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)
        
        form_personales.addRow("Nombre:", self.input_nombre)
        form_personales.addRow("Correo:", self.input_email)
        form_personales.addRow("Contraseña:", self.input_pass)
        layout.addLayout(form_personales)
        
        # --- Lista de cursos asignados ---
        layout.addWidget(QLabel("Mis Cursos Asignados:", self))
        self.lista_cursos = QListWidget()
        layout.addWidget(self.lista_cursos)
        
        btn_borrar = QPushButton("Borrar Curso Seleccionado")
        btn_borrar.clicked.connect(self.borrar_curso_asignado)
        layout.addWidget(btn_borrar)
        
        # --- Sección para Agregar un nuevo curso ---
        layout.addWidget(QLabel("Agregar Curso Nuevo:", self))
        # Seleccionar profesor
        prof_layout = QFormLayout()
        self.combo_profesor = QComboBox()
        # Agregamos un ítem vacío
        self.combo_profesor.addItem("-- Seleccionar Profesor --", None)
        self.combo_profesor.currentIndexChanged.connect(self.cargar_cursos_profesor)
        prof_layout.addRow("Profesor:", self.combo_profesor)
        # Seleccionar curso del profesor
        self.combo_curso_prof = QComboBox()
        self.combo_curso_prof.addItem("-- Seleccionar Curso --", None)
        prof_layout.addRow("Curso:", self.combo_curso_prof)
        layout.addLayout(prof_layout)
        
        self.btn_agregar_curso = QPushButton("Agregar Curso")
        self.btn_agregar_curso.clicked.connect(self.agregar_curso_nuevo)
        layout.addWidget(self.btn_agregar_curso)
        
        # --- Botones Finales ---
        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        # Se inicia deshabilitado; se activará al cargar la información
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
    
    # ------------------- Carga de Estudiante -------------------
    def cargar_estudiante(self):
        """
        Carga los datos del estudiante (nombre, email, password y cursos) desde usuarios.json.
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
        for user in data.get("users", []):
            if user.get("tipo") == "estudiante" and user.get("email", "").strip().lower() == self.estudiante_email.lower():
                self.estudiante_data = user
                break
        if not self.estudiante_data:
            QMessageBox.warning(self, "Error", "No se encontró tu información en usuarios.json.")
            return
        
        # Llenar campos personales
        self.input_nombre.setText(self.estudiante_data.get("nombre", ""))
        self.input_email.setText(self.estudiante_data.get("email", ""))
        self.input_pass.setText(self.estudiante_data.get("password", ""))
        self.refrescar_lista_cursos()
        # Habilitamos el botón de guardar ya que se cargaron los datos
        self.btn_guardar.setEnabled(True)
    
    def refrescar_lista_cursos(self):
        self.lista_cursos.clear()
        if not self.estudiante_data:
            return
        for c in self.estudiante_data.get("cursos_cursados", []):
            texto = f"{c.get('id')} - {c.get('nombre')} ({c.get('tipo')})"
            self.lista_cursos.addItem(texto)
    
    # ------------------- Borrar Curso -------------------
    def borrar_curso_asignado(self):
        if not self.estudiante_data:
            QMessageBox.warning(self, "Error", "No se cargó la información del estudiante.")
            return
        item = self.lista_cursos.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Seleccione un curso para borrarlo.")
            return
        texto = item.text()
        curso_id = texto.split(" - ")[0]
        old_cursos = self.estudiante_data.get("cursos_cursados", [])
        new_cursos = [cc for cc in old_cursos if cc.get("id") != curso_id]
        self.estudiante_data["cursos_cursados"] = new_cursos
        self.refrescar_lista_cursos()
        QMessageBox.information(self, "Borrado", "Se eliminó el curso de tu lista.")
    
    # ------------------- Guardar Cambios -------------------
    def guardar_cambios(self):
        if not self.estudiante_data:
            QMessageBox.warning(self, "Error", "No se cargó la información del estudiante.")
            return
        
        nuevo_nombre = self.input_nombre.text().strip()
        nuevo_email = self.input_email.text().strip()
        nueva_pass = self.input_pass.text().strip()
        
        if not nuevo_nombre or not nuevo_email or not nueva_pass:
            QMessageBox.warning(self, "Error", "El nombre, el correo y la contraseña no pueden quedar vacíos.")
            return
        
        self.estudiante_data["nombre"] = nuevo_nombre
        self.estudiante_data["email"] = nuevo_email
        self.estudiante_data["password"] = nueva_pass
        
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
        
        # Usar el id del estudiante convertido a cadena para identificarlo de forma única
        estudiante_id = str(self.estudiante_data.get("id")).strip()
        actualizado = False
        for user in data.get("users", []):
            if user.get("tipo") == "estudiante" and str(user.get("id")).strip() == estudiante_id:
                user["nombre"] = self.estudiante_data["nombre"]
                user["email"] = self.estudiante_data["email"]
                user["password"] = self.estudiante_data["password"]
                user["cursos_cursados"] = self.estudiante_data["cursos_cursados"]
                actualizado = True
                break
        
        if not actualizado:
            QMessageBox.warning(self, "Error", "No se encontró tu registro para actualizar.")
            return
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Éxito", "Cambios guardados exitosamente.")
            self.estudiante_email = self.estudiante_data["email"]
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo guardar en usuarios.json: {e}")
    
    # ------------------- Métodos para agregar un curso nuevo (sin notas) -------------------
    def cargar_profesores(self):
        self.profesores = []
        path = os.path.join("data", "usuarios.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for user in data.get("users", []):
                    if user.get("tipo") == "profesor":
                        self.profesores.append(user)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al cargar profesores: {e}")
        
        self.combo_profesor.clear()
        # Agregar ítem vacío para evitar confusiones
        self.combo_profesor.addItem("-- Seleccionar Profesor --", None)
        for prof in self.profesores:
            display_text = f"{prof.get('nombre')} ({prof.get('email')})"
            self.combo_profesor.addItem(display_text, prof)
    
    def cargar_cursos_profesor(self):
        idx = self.combo_profesor.currentIndex()
        prof_data = self.combo_profesor.itemData(idx)
        
        if not prof_data:
            self.combo_curso_prof.clear()
            self.combo_curso_prof.addItem("-- Seleccionar Curso --", None)
            return

        self.cursos_profesor = []
        for bloque in prof_data.get("anos", []):
            anio = bloque.get("anio")
            semestre = bloque.get("semestre")
            for c in bloque.get("cursos", []):
                ccopy = c.copy()
                ccopy["anio"] = anio
                ccopy["semestre"] = semestre
                self.cursos_profesor.append(ccopy)

        self.combo_curso_prof.clear()
        self.combo_curso_prof.addItem("-- Seleccionar Curso --", None)
        for c in self.cursos_profesor:
            disp = f"Año: {c.get('anio')}, Sem: {c.get('semestre')} - {c.get('id')} - {c.get('nombre')} ({c.get('tipo')})"
            self.combo_curso_prof.addItem(disp, c)
    
    def agregar_curso_nuevo(self):
        if not self.estudiante_data:
            QMessageBox.warning(self, "Error", "Primero busque al estudiante que desea editar.")
            return
        
        idx_prof = self.combo_profesor.currentIndex()
        if idx_prof < 0 or self.combo_profesor.itemData(idx_prof) is None:
            QMessageBox.warning(self, "Error", "No has seleccionado un profesor.")
            return
        
        idx_curso = self.combo_curso_prof.currentIndex()
        if idx_curso < 0 or self.combo_curso_prof.itemData(idx_curso) is None:
            QMessageBox.warning(self, "Error", "No has seleccionado un curso del profesor.")
            return
        
        # Obtener datos del profesor seleccionado
        prof_data = self.combo_profesor.itemData(idx_prof)
        
        curso = self.combo_curso_prof.itemData(idx_curso)
        nuevo_curso = curso.copy()
        tipo = nuevo_curso.get("tipo", "").lower()
        
        if tipo == "matematico":
            nuevo_curso["nota_examen1"] = 0.0
            nuevo_curso["nota_examen2"] = 0.0
            nuevo_curso["nota_examen3"] = 0.0
            nuevo_curso["nota_tareas"]  = 0.0
        elif tipo == "carrera":
            nuevo_curso["nota_proyecto1"] = 0.0
            nuevo_curso["nota_proyecto2"] = 0.0
            nuevo_curso["nota_laboratorios"] = 0.0
        elif tipo == "ingles":
            nuevo_curso["nota_examen1"] = 0.0
            nuevo_curso["nota_examen2"] = 0.0
            nuevo_curso["nota_laboratorios"] = 0.0
            nuevo_curso["nota_tareas"] = 0.0
        else:
            nuevo_curso["nota_trabajo1"] = 0.0
            nuevo_curso["nota_trabajo2"] = 0.0
            nuevo_curso["nota_trabajo3"] = 0.0
            nuevo_curso["nota_tareas"] = 0.0
        
        nuevo_curso["nota_total"] = 0.0
        nuevo_curso["profe"] = prof_data.get("email", "desconocido")
        
        lista_cursos_est = self.estudiante_data.get("cursos_cursados", [])
        lista_cursos_est.append(nuevo_curso)
        self.estudiante_data["cursos_cursados"] = lista_cursos_est
        
        self.refrescar_lista_cursos()
        QMessageBox.information(self, "Curso Agregado", 
            "El nuevo curso se agregó a tu lista en memoria. Presiona 'Guardar Cambios' para confirmar.")
        # Reinicializar los combo boxes a sus ítems vacíos
        self.combo_profesor.setCurrentIndex(0)
        self.combo_curso_prof.clear()
        self.combo_curso_prof.addItem("-- Seleccionar Curso --", None)
