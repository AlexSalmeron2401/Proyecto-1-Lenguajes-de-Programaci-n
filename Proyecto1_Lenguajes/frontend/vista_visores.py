from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class VentanaPrincipalVisor(QWidget):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.setWindowTitle("Ventana Visor")
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        # Mensaje de bienvenida personalizado
        welcome_label = QLabel(f"Bienvenido, {self.nombre}! Tienes acceso restringido.", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        self.setLayout(layout)
