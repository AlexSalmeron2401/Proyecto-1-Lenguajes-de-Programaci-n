from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class VentanaPrincipalAdmin(QWidget):
    def __init__(self, partner):
        super().__init__()
        self.setWindowTitle("Ventana Administrador")
        self.setGeometry(100, 100, 400, 300)

        # Etiqueta de bienvenida
        label = QLabel(f"Bienvenido, {partner}! Eres un Administrador.", self)
        
        # Botón para agregar datos (como semestres, materias, etc.)
        boton_agregar_datos = QPushButton("Agregar Datos", self)
        boton_agregar_datos.clicked.connect(self.agregar_datos)

        # Layout de la ventana
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(boton_agregar_datos)
        self.setLayout(layout)

    def agregar_datos(self):
        # Aquí puedes abrir una ventana secundaria o un formulario para ingresar datos.
        print("Función para agregar datos llamada")
