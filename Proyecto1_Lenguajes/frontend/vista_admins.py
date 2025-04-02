from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QDialog
from frontend.vista_agregarDatos import VentanaAgregarDatos

# Importa los nuevos módulos; asegúrate de que las rutas sean correctas.
from frontend.vista_borrarDatos import VentanaBorrarDatos
from frontend.vista_verCursos import VentanaVerCursos
from frontend.vista_agregarEstudiantes import VentanaAgregarEstudiantes
from frontend.vista_estudiantesCursos import VentanaVerEstudiantesCursos

class VentanaPrincipalAdmin(QWidget):
    def __init__(self, partner):
        super().__init__()
        self.partner = partner
        self.setWindowTitle("Ventana Administrador")
        self.setGeometry(100, 100, 600, 500)
        
        layout = QVBoxLayout()
        
        # Mensaje de bienvenida
        label = QLabel(f"Bienvenido, {partner}! Eres un Administrador.", self)
        layout.addWidget(label)
        
        # Botón para abrir la ventana de Agregar Datos
        boton_agregar_datos = QPushButton("Agregar Datos", self)
        boton_agregar_datos.clicked.connect(self.abrir_agregar_datos)
        layout.addWidget(boton_agregar_datos)
        
        # Botón para abrir la ventana de Borrar Información
        boton_borrar_datos = QPushButton("Borrar Información", self)
        boton_borrar_datos.clicked.connect(self.abrir_borrar_datos)
        layout.addWidget(boton_borrar_datos)
        
        # Botón para abrir la ventana de Ver Cursos Impartidos
        boton_ver_cursos = QPushButton("Ver Cursos Impartidos", self)
        boton_ver_cursos.clicked.connect(self.abrir_ver_cursos)
        layout.addWidget(boton_ver_cursos)
        
        # Botón para abrir la ventana de Agregar Estudiante
        boton_agregar_estudiante = QPushButton("Agregar Estudiante", self)
        boton_agregar_estudiante.clicked.connect(self.abrir_agregar_estudiante)
        layout.addWidget(boton_agregar_estudiante)
        
        # Botón para abrir la ventana de Ver Cursos de Estudiantes
        boton_ver_estudiantes = QPushButton("Ver Cursos de Estudiantes", self)
        boton_ver_estudiantes.clicked.connect(self.abrir_ver_estudiantes)
        layout.addWidget(boton_ver_estudiantes)
        
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
    
    def abrir_borrar_datos(self):
        self.borrarDatos = VentanaBorrarDatos()
        self.borrarDatos.exec_()
    
    def abrir_ver_cursos(self):
        self.verCursos = VentanaVerCursos()
        self.verCursos.exec_()
    
    def abrir_agregar_estudiante(self):
        self.agregarEst = VentanaAgregarEstudiantes()
        self.agregarEst.exec_()
    
    def abrir_ver_estudiantes(self):
        self.verEstCursos = VentanaVerEstudiantesCursos()
        self.verEstCursos.exec_()
    
    def logout(self):
        from frontend.vista_login import VentanaLogin
        self.login = VentanaLogin()
        self.login.show()
        self.close()

