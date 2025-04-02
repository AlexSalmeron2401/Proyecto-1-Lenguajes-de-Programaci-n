from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class VentanaEditarEstudiantes(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editar Estudiantes")
        self.setGeometry(300, 300, 400, 200)
        layout = QVBoxLayout()
        
        mensaje = QLabel("Función para editar estudiantes aún no implementada.", self)
        layout.addWidget(mensaje)
        
        btn_cerrar = QPushButton("Cerrar", self)
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)
        
        self.setLayout(layout)
