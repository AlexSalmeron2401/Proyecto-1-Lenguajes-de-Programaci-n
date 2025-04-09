import os
import json
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

# Se importan los módulos reutilizados para editar y ver cursos de estudiantes.
from frontend.vista_estudiantesEditDatosEstudiante import VentanaEditarDatosEstudiante
from frontend.vista_estudiantesVerCursos import VentanaCursos

class VentanaPrincipalVisor(QWidget):
    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        # Se obtiene el email del estudiante desde credenciales.json
        self.estudiante_email = self.obtener_estudiante_email()
        self.estudiante_data = self.obtener_estudiante()
        self.setWindowTitle("Ventana Visor")
        self.setGeometry(100, 100, 600, 500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Mensaje de bienvenida personalizado
        if self.estudiante_data:
            welcome_text = f"Bienvenido, {self.estudiante_data.get('nombre', 'Estudiante')}! Estas son tus opciones."
        else:
            welcome_text = "Bienvenido, Estudiante! No se encontró tu información."
        welcome_label = QLabel(welcome_text, self)
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Botón para editar cursos (usar VentanaEditarDatosEstudiante)
        btn_editar = QPushButton("Editar Mi Información")
        btn_editar.clicked.connect(self.abrir_editar)
        layout.addWidget(btn_editar)
        
        # Botón para ver cursos (usar VentanaVerEstudiantesCursos)
        btn_ver = QPushButton("Ver Mis Cursos")
        btn_ver.clicked.connect(self.abrir_ver)
        layout.addWidget(btn_ver)
        
        self.setLayout(layout)
    
    def obtener_estudiante_email(self):
        """
        Lee el correo del estudiante desde data/credenciales.json.
        Se asume que en credenciales.json se encuentra el email usado para iniciar sesión.
        """
        path = os.path.join("data", "credenciales.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                users = data.get("users", [])
                if users and isinstance(users, list):
                    return users[0].get("email", "").strip()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al leer credenciales: {e}")
        return ""
    
    def obtener_estudiante(self):
        """
        Busca en usuarios.json un usuario de tipo 'estudiante' cuyo email coincida.
        """
        path = os.path.join("data", "usuarios.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for user in data.get("users", []):
                    if user.get("tipo") == "estudiante" and user.get("email", "").strip() == self.estudiante_email:
                        return user
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo leer usuarios.json: {e}")
        return None
    
    def abrir_editar(self):
        """
        Abre la ventana para editar cursos y el nombre del estudiante.
        Se reutiliza VentanaEditarDatosEstudiante.
        """
        if self.estudiante_data:
            ventana = VentanaEditarDatosEstudiante(estudiante_email=self.estudiante_email)
            # No es necesario prellenar input_id_buscar, ya que la ventana carga los datos automáticamente.
            ventana.exec_()
        else:
            QMessageBox.warning(self, "Error", "No se encontró tu registro en usuarios.json.")

    
    def abrir_ver(self):
        """
        Abre la ventana para ver los cursos asignados al estudiante.
        Se reutiliza VentanaVerEstudiantesCursos pasando el email del estudiante.
        """
        if self.estudiante_data:
            ventana_ver = VentanaCursos(self.estudiante_email)
            ventana_ver.exec_()
        else:
            QMessageBox.warning(self, "Error", "No se encontró tu registro en usuarios.json.")
