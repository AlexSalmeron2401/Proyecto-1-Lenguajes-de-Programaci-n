import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt

class VentanaVerCursos(QDialog):
    def __init__(self, profesor_email):
        super().__init__()
        self.setWindowTitle("Ver Cursos Impartidos")
        self.setFixedSize(500, 400)
        self.profesor_email = profesor_email
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulario para seleccionar año y semestre, basado en el profesor
        form_layout = QFormLayout()
        self.combo_anio = QComboBox()
        self.load_anios()  # Carga los años disponibles del profesor desde usuarios.json
        form_layout.addRow("Año:", self.combo_anio)
        
        self.combo_semestre = QComboBox()
        self.combo_semestre.addItems(["1", "2"])
        form_layout.addRow("Semestre:", self.combo_semestre)
        
        layout.addLayout(form_layout)
        
        # Botón para cargar cursos
        self.btn_ver = QPushButton("Ver Cursos")
        self.btn_ver.clicked.connect(self.ver_cursos)
        layout.addWidget(self.btn_ver)
        
        # Lista para mostrar los cursos
        self.lista_cursos = QListWidget()
        self.lista_cursos.itemDoubleClicked.connect(self.ver_estudiantes)
        layout.addWidget(self.lista_cursos)
        
        # Botón para ver estudiantes (función no implementada)
        self.btn_ver_est = QPushButton("Ver Estudiantes")
        self.btn_ver_est.clicked.connect(self.ver_estudiantes)
        layout.addWidget(self.btn_ver_est)
        
        self.setLayout(layout)
    
    def apply_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #F4F7F6;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            QFormLayout QLabel {
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
                background-color: #fff;
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
    
    def load_anios(self):
        """Carga los años únicos en los que el profesor tiene cursos desde usuarios.json."""
        path = os.path.join("data", "usuarios.json")
        years = set()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for user in data.get("users", []):
                        if user.get("email") == self.profesor_email and user.get("tipo") == "profesor":
                            for bloque in user.get("anos", []):
                                year = bloque.get("anio")
                                if year:
                                    years.add(year)
            except json.JSONDecodeError:
                pass
        years = sorted(years)
        self.combo_anio.clear()
        for y in years:
            self.combo_anio.addItem(str(y), y)
    
    def ver_cursos(self):
        """Carga y muestra en la lista los cursos del año y semestre seleccionados."""
        try:
            anio = int(self.combo_anio.currentData())
        except (ValueError, TypeError):
            QMessageBox.warning(self, "Error", "Seleccione un año válido.")
            return
        semestre = int(self.combo_semestre.currentText())
        
        path = os.path.join("data", "usuarios.json")
        cursos_list = []
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Buscar el profesor y recorrer su lista de "anos"
                    for user in data.get("users", []):
                        if user.get("email") == self.profesor_email and user.get("tipo") == "profesor":
                            for bloque in user.get("anos", []):
                                if bloque.get("anio") == anio and bloque.get("semestre") == semestre:
                                    for curso in bloque.get("cursos", []):
                                        item_text = f"{curso.get('id')} - {curso.get('nombre')} ({curso.get('tipo')})"
                                        cursos_list.append(item_text)
                            break
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Error", "Error al leer el archivo JSON.")
                return
        
        self.lista_cursos.clear()
        if cursos_list:
            for item in cursos_list:
                self.lista_cursos.addItem(item)
        else:
            QMessageBox.information(self, "Info", "No se encontró información para el año y semestre seleccionados.")
    
    def ver_estudiantes(self, item=None):
        """
        Función para ver estudiantes asignados a un curso.
        Dado que esta funcionalidad aún no se implementa, se mostrará un mensaje informativo.
        """
        QMessageBox.information(self, "Estudiantes", "Función todavía no implementada para ver estudiantes.")
