from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QPushButton, QDialog, QMessageBox,
    QHBoxLayout, QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt
import os
import json
import subprocess

# Integración de Matplotlib en PyQt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VentanaRendimientoHistorico(QDialog):
    def __init__(self, profesor_email):
        super().__init__()
        self.profesor_email = profesor_email
        self.profesor_id = self.obtener_profesor_id()
        self.datos = {}
        self.setWindowTitle("Rendimiento Histórico")
        self.setFixedSize(800, 600)
        self.init_ui()

    def init_ui(self):
        # Estilos del diálogo
        self.setStyleSheet("""
            QDialog { background: #F5F7FA; }
            QLabel#title { color: #2C3E50; }
            QComboBox { padding: 5px; border-radius: 5px; }
            QPushButton { background: #3498DB; color: white; padding: 8px; border: none; border-radius: 5px; }
            QPushButton:hover { background: #2980B9; }
        """)

        layout = QVBoxLayout(self)

        # Título
        title = QLabel("Panel de Rendimiento")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:20pt; font-weight:bold; margin:15px;")
        layout.addWidget(title)

        # Controles
        filtros = QHBoxLayout()
        filtros.setSpacing(10)

        self.combo_tipo = QComboBox()
        tipos = ["por_tema", "por_curso", "por_semestre", "por_anio", "historico"]
        self.combo_tipo.addItems(tipos)
        self.combo_tipo.currentTextChanged.connect(self.on_tipo_changed)
        filtros.addWidget(QLabel("Vista:"))
        filtros.addWidget(self.combo_tipo)

        self.combo_item = QComboBox()
        self.combo_item.currentTextChanged.connect(self.on_item_changed)
        filtros.addWidget(QLabel("Elemento:"))
        filtros.addWidget(self.combo_item)

        btn = QPushButton("Generar Rendimiento")
        btn.clicked.connect(self.procesar_rendimiento)
        filtros.addWidget(btn)

        layout.addLayout(filtros)

        # Canvas
        self.figure = Figure(tight_layout=True)
        self.figure.patch.set_facecolor('#ECF0F1')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.canvas)

        # Inicializar opciones
        self.on_tipo_changed(self.combo_tipo.currentText())

    def obtener_profesor_id(self):
        path = "data/usuarios.json"
        if not os.path.exists(path):
            return None
        try:
            with open(path, encoding="utf-8") as f:
                users = json.load(f).get("users", [])
            for u in users:
                tipo = u.get("tipo", "").strip().lower()
                email = u.get("email", "").strip().lower()
                if tipo == "profesor" and email == self.profesor_email.strip().lower():
                    return u.get("id")
        except Exception as e:
            print("Error leyendo usuarios:", e)
        return None

    def procesar_rendimiento(self):
        if not self.profesor_id:
            QMessageBox.critical(self, "Error", "ID de profesor no encontrado.")
            return
        sol_path = self.generar_solicitud()
        if not sol_path:
            return
        exe = os.path.join("backend", "rendimiento")
        out = os.path.join("data", "rendimiento.json")
        try:
            subprocess.run([exe, sol_path, out], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error OCaml", e.stderr)
            return
        self.cargar_datos(out)
        self.on_tipo_changed(self.combo_tipo.currentText())

    def generar_solicitud(self):
        try:
            with open("data/cursoEstudianteProfesor.json", encoding="utf-8") as f:
                raw = json.load(f)
            lista = []
            anio = semestre = None
            for y, sems in raw.get("cursos", {}).items():
                for s, cs in sems.items():
                    for c in cs:
                        if str(c.get("profe")) == str(self.profesor_id):
                            lista.append(c)
                            if anio is None:
                                anio, semestre = int(y), int(s)
            sol = {"estudiante": {"anio": anio, "semestre": semestre, "cursos": lista}}
            path = "data/solicitud.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(sol, f, ensure_ascii=False, indent=4)
            return path
        except Exception as e:
            QMessageBox.critical(self, "Error Solicitud", str(e))
            return None

    def cargar_datos(self, path):
        try:
            with open(path, encoding="utf-8") as f:
                full = json.load(f)
            self.datos = full.get("profesor", {})
        except Exception as e:
            QMessageBox.critical(self, "Error Leer JSON", str(e))

    def on_tipo_changed(self, tipo):
        elementos = self.obtener_opciones(tipo)
        self.combo_item.clear()
        self.combo_item.addItems(elementos)

    def on_item_changed(self, item):
        self.dibujar_grafica()

    def obtener_opciones(self, tipo):
        datos = self.datos.get(tipo, []) or []
        opciones = []
        if tipo == "por_semestre":
            opciones = [f"Sem {e.get('semestre')}" for e in datos]
        elif tipo == "por_anio":
            opciones = [str(e.get('anio')) for e in datos]
        elif tipo == "historico":
            opciones = ["Histórico"]
        else:
            opciones = [e.get('curso') or e.get('id') for e in datos]
        seen = set()
        return [x for x in opciones if x not in seen and not seen.add(x)]

    def dibujar_grafica(self):
        tipo = self.combo_tipo.currentText()
        item = self.combo_item.currentText()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.grid(color='#BDC3C7', linestyle='--', linewidth=0.5)
        datos = self.datos.get(tipo, []) or []
        x, y = [], []
        if tipo == "por_semestre":
            for e in datos:
                x.append(f"Sem {e.get('semestre')}")
                y.append(e.get('promedio', 0))
        elif tipo == "por_anio":
            for e in datos:
                x.append(str(e.get('anio')))
                y.append(e.get('promedio', 0))
        elif tipo == "historico":
            if datos:
                for a in datos[0].get('anios', []):
                    x.append(str(a.get('anio')))
                    y.append(a.get('promedio', 0))
        elif tipo == "por_curso":
            for e in datos:
                if e.get('curso') == item:
                    for k, v in e.get('resumen', {}).items():
                        x.append(k)
                        y.append(v)
        else:  # por_tema
            for e in datos:
                if e.get('curso') == item:
                    for k, v in e.get('temas', {}).items():
                        x.append(k)
                        y.append(v)
        if not x:
            ax.text(0.5, 0.5, 'Sin datos', ha='center', va='center', transform=ax.transAxes, color='#7F8C8D')
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            pos = list(range(len(x)))
            ax.plot(pos, y, marker='o', linestyle='-', linewidth=2)
            ax.fill_between(pos, y, alpha=0.3)
            ax.set_xticks(pos)
            ax.set_xticklabels(x, rotation=45, ha='right', color='#2C3E50')
        ax.set_title(f"{tipo.replace('_',' ').title()} - {item}", color='#34495E')
        ax.set_ylabel("Puntuación", color='#34495E')
        self.canvas.draw()
