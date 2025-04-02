from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class VentanaBorrarEstudiantesCursos(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Borrar Estudiantes de Cursos")
        self.setGeometry(300, 300, 400, 200)
        layout = QVBoxLayout()
        
        label = QLabel("Función para borrar estudiantes de cursos aún no implementada.", self)
        layout.addWidget(label)
        
        btn_cerrar = QPushButton("Cerrar", self)
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)
        
        self.setLayout(layout)