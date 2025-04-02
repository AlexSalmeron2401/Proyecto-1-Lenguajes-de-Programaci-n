import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox, QLineEdit,
    QPushButton, QListWidget, QMessageBox
)

class VentanaVerCursos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ver Cursos Impartidos")
        self.setGeometry(250, 250, 500, 400)
        layout = QVBoxLayout()
        
        # En lugar de QLineEdit para año, usamos un QComboBox que se llena con los años disponibles
        form_layout = QFormLayout()
        self.combo_anio = QComboBox()
        self.load_anios()  # Método que carga los años desde el archivo JSON
        form_layout.addRow("Año:", self.combo_anio)
        
        # Para el semestre, un combo box con las opciones "1" y "2"
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
        
        # Botón adicional para ver estudiantes del curso seleccionado
        self.btn_ver_est = QPushButton("Ver Estudiantes")
        self.btn_ver_est.clicked.connect(self.ver_estudiantes)
        layout.addWidget(self.btn_ver_est)
        
        self.setLayout(layout)
    
    def load_anios(self):
        """Carga los años únicos en los que hay cursos desde data/informacion.json y los agrega al combo_anio."""
        path = os.path.join("data", "informacion.json")
        years = set()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    for entry in data.get("informacion", []):
                        year = entry.get("anio")
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
        path = os.path.join("data", "informacion.json")
        if not os.path.exists(path):
            QMessageBox.information(self, "Info", "No hay información guardada.")
            return
        with open(path, "r", encoding="utf-8") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Error", "Error al leer el archivo JSON.")
                return
        
        self.lista_cursos.clear()
        found = False
        for entry in existing.get("informacion", []):
            if entry.get("anio") == anio and entry.get("semestre") == semestre:
                cursos = entry.get("cursos", [])
                if cursos:
                    for curso in cursos:
                        item_text = f"{curso.get('id')} - {curso.get('nombre')} ({curso.get('tipo')})"
                        self.lista_cursos.addItem(item_text)
                    found = True
        if not found:
            QMessageBox.information(self, "Info", "No se encontró información para el año y semestre seleccionados.")
    
    def ver_estudiantes(self, item=None):
        """
        Al seleccionar (o haciendo doble clic en) un curso,
        se muestran los estudiantes que tienen asignado ese curso.
        """
        if item is None:
            item = self.lista_cursos.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Seleccione un curso para ver estudiantes.")
            return
        
        # Se espera que el texto esté en el formato: "ID - Nombre (tipo)"
        course_text = item.text()
        course_id = course_text.split(" - ")[0]
        
        # Leer el archivo de estudiantes
        path = os.path.join("data", "estudiantes.json")
        if not os.path.exists(path):
            QMessageBox.information(self, "Info", "No hay información de estudiantes guardada.")
            return
        
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                QMessageBox.warning(self, "Error", "Error al leer estudiantes.json.")
                return
        
        estudiantes = data.get("estudiantes", [])
        matched = []
        for est in estudiantes:
            for curso in est.get("cursos", []):
                if curso.get("id") == course_id:
                    matched.append(est.get("nombre", "Desconocido"))
                    break
        if matched:
            msg = "Estudiantes que cursaron este curso:\n" + "\n".join(matched)
            QMessageBox.information(self, "Estudiantes", msg)
        else:
            QMessageBox.information(self, "Estudiantes", "No se encontraron estudiantes para este curso.")
