from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class VentanaPrincipalVisor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Visor")
        self.setGeometry(100, 100, 400, 300)

        # Etiqueta de bienvenida para visores
        label = QLabel("Bienvenido, Visor! Tienes acceso restringido.", self)
        
        # Layout de la ventana
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)