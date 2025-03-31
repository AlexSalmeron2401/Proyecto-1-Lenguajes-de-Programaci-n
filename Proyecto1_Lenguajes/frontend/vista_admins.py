from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QDialog
from frontend.vista_agregarDatos import VentanaAgregarDatos

# Se importará la ventana de borrar datos desde el módulo que crearemos a continuación.
class VentanaPrincipalAdmin(QWidget):
    def __init__(self, partner):
        super().__init__()
        self.partner = partner
        self.setWindowTitle("Ventana Administrador")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # Mensaje de bienvenida
        label = QLabel(f"Bienvenido, {partner}! Eres un Administrador.", self)
        layout.addWidget(label)
        
        # Botón para abrir la ventana de Agregar Datos
        boton_agregar_datos = QPushButton("Agregar Datos", self)
        boton_agregar_datos.clicked.connect(self.abrir_agregar_datos)
        layout.addWidget(boton_agregar_datos)
        
        # Nuevo botón para abrir la ventana de Borrar Información
        boton_borrar_datos = QPushButton("Borrar Información", self)
        boton_borrar_datos.clicked.connect(self.abrir_borrar_datos)
        layout.addWidget(boton_borrar_datos)
        
        # Botón para hacer Logout
        boton_logout = QPushButton("Logout", self)
        boton_logout.clicked.connect(self.logout)
        layout.addWidget(boton_logout)
        
        self.setLayout(layout)
    
    def abrir_agregar_datos(self):
        self.agregarDatos = VentanaAgregarDatos()
        if self.agregarDatos.exec_() == QDialog.Accepted:
            data = self.agregarDatos.get_data()
            print("Información agregada:", data)
        # Se puede mantener la ventana abierta según se requiera.
    
    def abrir_borrar_datos(self):
        from frontend.vista_borrarDatos import VentanaBorrarDatos
        self.borrarDatos = VentanaBorrarDatos()
        self.borrarDatos.exec_()
    
    def logout(self):
        from frontend.vista_login import VentanaLogin
        self.login = VentanaLogin()
        self.login.show()
        self.close()
