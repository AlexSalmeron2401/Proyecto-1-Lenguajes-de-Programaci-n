import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QListWidget, QPushButton, QMessageBox, QLabel, QComboBox, QStackedWidget
)
# Importa las clases definidas en tu módulo OOP (ajusta la ruta según corresponda)
from frontend.clases_informacion import CursoMatematico, CursoCarrera, CursoIngles, CursoOtros

# Diálogo para agregar un curso detallado
class VentanaAgregarCursoDetallado(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Curso Detallado")
        self.setGeometry(250, 250, 400, 300)
        
        self.layout = QVBoxLayout()
        
        # Formulario de datos comunes: Tipo, Nombre e ID
        form_layout = QFormLayout()
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Matemático", "Carrera", "Inglés", "Otros"])
        form_layout.addRow("Tipo de Curso:", self.combo_tipo)
        
        self.input_nombre = QLineEdit()
        form_layout.addRow("Nombre del Curso:", self.input_nombre)
        
        self.input_id = QLineEdit()
        form_layout.addRow("ID del Curso:", self.input_id)
        
        self.layout.addLayout(form_layout)
        
        # Área para ingresar campos específicos, usando un QStackedWidget
        self.stacked = QStackedWidget()
        
        # --- Para Curso Matemático ---
        self.widget_matematico = QDialog()
        mat_layout = QFormLayout()
        self.input_mat_ex1 = QLineEdit()
        mat_layout.addRow("Nota Examen 1:", self.input_mat_ex1)
        self.input_mat_ex2 = QLineEdit()
        mat_layout.addRow("Nota Examen 2:", self.input_mat_ex2)
        self.input_mat_ex3 = QLineEdit()
        mat_layout.addRow("Nota Examen 3:", self.input_mat_ex3)
        self.input_mat_tareas = QLineEdit()
        mat_layout.addRow("Nota Tareas:", self.input_mat_tareas)
        self.input_mat_total = QLineEdit()
        mat_layout.addRow("Nota Total:", self.input_mat_total)
        self.widget_matematico.setLayout(mat_layout)
        self.stacked.addWidget(self.widget_matematico)
        
        # --- Para Curso Carrera ---
        self.widget_carrera = QDialog()
        car_layout = QFormLayout()
        self.input_car_proy1 = QLineEdit()
        car_layout.addRow("Nota Proyecto 1:", self.input_car_proy1)
        self.input_car_proy2 = QLineEdit()
        car_layout.addRow("Nota Proyecto 2:", self.input_car_proy2)
        self.input_car_lab = QLineEdit()
        car_layout.addRow("Nota Laboratorios:", self.input_car_lab)
        self.input_car_total = QLineEdit()
        car_layout.addRow("Nota Total:", self.input_car_total)
        self.widget_carrera.setLayout(car_layout)
        self.stacked.addWidget(self.widget_carrera)
        
        # --- Para Curso Inglés ---
        self.widget_ingles = QDialog()
        ing_layout = QFormLayout()
        self.input_ing_ex1 = QLineEdit()
        ing_layout.addRow("Nota Examen 1:", self.input_ing_ex1)
        self.input_ing_ex2 = QLineEdit()
        ing_layout.addRow("Nota Examen 2:", self.input_ing_ex2)
        self.input_ing_lab = QLineEdit()
        ing_layout.addRow("Nota Laboratorios:", self.input_ing_lab)
        self.input_ing_tareas = QLineEdit()
        ing_layout.addRow("Nota Tareas:", self.input_ing_tareas)
        self.input_ing_total = QLineEdit()
        ing_layout.addRow("Nota Total:", self.input_ing_total)
        self.widget_ingles.setLayout(ing_layout)
        self.stacked.addWidget(self.widget_ingles)
        
        # --- Para Curso Otros ---
        self.widget_otros = QDialog()
        otros_layout = QFormLayout()
        self.input_otros_trab1 = QLineEdit()
        otros_layout.addRow("Nota Trabajo 1:", self.input_otros_trab1)
        self.input_otros_trab2 = QLineEdit()
        otros_layout.addRow("Nota Trabajo 2:", self.input_otros_trab2)
        self.input_otros_trab3 = QLineEdit()
        otros_layout.addRow("Nota Trabajo 3:", self.input_otros_trab3)
        self.input_otros_tareas = QLineEdit()
        otros_layout.addRow("Notas Tareas:", self.input_otros_tareas)
        self.input_otros_total = QLineEdit()
        otros_layout.addRow("Nota Total:", self.input_otros_total)
        self.widget_otros.setLayout(otros_layout)
        self.stacked.addWidget(self.widget_otros)
        
        self.layout.addWidget(self.stacked)
        
        # Conecta el cambio en el combo para actualizar el stacked widget
        self.combo_tipo.currentIndexChanged.connect(self.stacked.setCurrentIndex)
        
        # Botones de Aceptar y Cancelar
        botones_layout = QHBoxLayout()
        btn_ok = QPushButton("Aceptar")
        btn_ok.clicked.connect(self.aceptar)
        botones_layout.addWidget(btn_ok)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        botones_layout.addWidget(btn_cancel)
        self.layout.addLayout(botones_layout)
        
        self.setLayout(self.layout)
    
    def aceptar(self):
        nombre = self.input_nombre.text().strip()
        id_curso = self.input_id.text().strip()
        if not nombre or not id_curso:
            QMessageBox.warning(self, "Error", "Nombre e ID son obligatorios.")
            return
        tipo_index = self.combo_tipo.currentIndex()
        try:
            if tipo_index == 0:  # Matemático
                nota_ex1 = float(self.input_mat_ex1.text().strip())
                nota_ex2 = float(self.input_mat_ex2.text().strip())
                nota_ex3 = float(self.input_mat_ex3.text().strip())
                nota_tareas = float(self.input_mat_tareas.text().strip())
                nota_total = float(self.input_mat_total.text().strip())
                self.curso = CursoMatematico(
                    nombre=nombre, id=id_curso,
                    nota_examen1=nota_ex1, nota_examen2=nota_ex2, nota_examen3=nota_ex3,
                    nota_tareas=nota_tareas, nota_total=nota_total
                )
            elif tipo_index == 1:  # Carrera
                nota_proy1 = float(self.input_car_proy1.text().strip())
                nota_proy2 = float(self.input_car_proy2.text().strip())
                nota_lab = float(self.input_car_lab.text().strip())
                nota_total = float(self.input_car_total.text().strip())
                self.curso = CursoCarrera(
                    nombre=nombre, id=id_curso,
                    nota_proyecto1=nota_proy1, nota_proyecto2=nota_proy2,
                    nota_laboratorios=nota_lab, nota_total=nota_total
                )
            elif tipo_index == 2:  # Inglés
                nota_ex1 = float(self.input_ing_ex1.text().strip())
                nota_ex2 = float(self.input_ing_ex2.text().strip())
                nota_lab = float(self.input_ing_lab.text().strip())
                nota_tareas = float(self.input_ing_tareas.text().strip())
                nota_total = float(self.input_ing_total.text().strip())
                self.curso = CursoIngles(
                    nombre=nombre, id=id_curso,
                    nota_examen1=nota_ex1, nota_examen2=nota_ex2,
                    nota_laboratorios=nota_lab, nota_tareas=nota_tareas,
                    nota_total=nota_total
                )
            elif tipo_index == 3:  # Otros
                nota_trab1 = float(self.input_otros_trab1.text().strip())
                nota_trab2 = float(self.input_otros_trab2.text().strip())
                nota_trab3 = float(self.input_otros_trab3.text().strip())
                notas_tareas = float(self.input_otros_tareas.text().strip())
                nota_total = float(self.input_otros_total.text().strip())
                self.curso = CursoOtros(
                    nombre=nombre, id=id_curso,
                    nota_trabajo1=nota_trab1, nota_trabajo2=nota_trab2, nota_trabajo3=nota_trab3,
                    notas_tareas=notas_tareas, nota_total=nota_total
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

# Ventana principal para agregar información por año (y semestre)
class VentanaAgregarDatos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Información - Por Año")
        self.setGeometry(200, 200, 500, 400)
        
        self.cursos_detallados = []  # Lista de objetos Curso (detallados)
        
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
        botones_layout = QHBoxLayout()
        btn_ok = QPushButton("Aceptar")
        btn_ok.clicked.connect(self.aceptar)
        botones_layout.addWidget(btn_ok)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        botones_layout.addWidget(btn_cancel)
        layout.addLayout(botones_layout)
        
        self.setLayout(layout)
    
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
            QMessageBox.warning(self, "Error", "Debe agregar al menos un curso detallado.")
            return
        
        try:
            self.anio = int(anio_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "El año debe ser numérico.")
            return
        
        self.semestre = int(self.combo_semestre.currentText())
        self.write_json()
        self.accept()
    
    def get_data(self):
        """Retorna un diccionario con la información del año, semestre y los cursos detallados."""
        return {
            "anio": self.anio,
            "semestre": self.semestre,
            "cursos": [curso.to_dict() for curso in self.cursos_detallados]
        }
    
    def write_json(self):
        """Escribe la información en data/informacion.json."""
        data_to_save = self.get_data()
        path = os.path.join("data", "informacion.json")
        
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = {"informacion": []}
        else:
            existing = {"informacion": []}
        
        existing["informacion"].append(data_to_save)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=4, ensure_ascii=False)
