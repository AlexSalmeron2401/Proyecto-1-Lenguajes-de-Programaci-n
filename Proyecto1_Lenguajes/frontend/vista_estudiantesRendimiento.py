from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QPushButton, QDialog, QMessageBox,
    QHBoxLayout, QComboBox, QSizePolicy
)
from PyQt5.QtCore import Qt
import os, json, subprocess

# Integración de Matplotlib en PyQt5
try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

class VentanaEstudianteRendimiento(QDialog):
    def __init__(self, estudiante_email):
        super().__init__()
        self.estudiante_email = estudiante_email
        self.estudiante_id = self._obtener_estudiante_id()
        self.datos = {}
        self.setWindowTitle("Rendimiento Histórico Estudiante")
        self.setFixedSize(800, 600)
        self._init_ui()

    def _init_ui(self):
        # Estilos generales
        self.setStyleSheet(
            "QDialog { background: #F5F7FA; }"
            "QLabel#title { color: #2C3E50; font-size:18pt; font-weight:bold; }"
            "QComboBox { padding: 5px; border-radius: 5px; }"
            "QPushButton { background: #27AE60; color: white; padding: 8px; border: none; border-radius: 5px; }"
            "QPushButton:hover { background: #219150; }"
        )

        layout = QVBoxLayout()
        # Título
        title = QLabel("Panel de Rendimiento - Estudiante")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Controles de filtro
        hl = QHBoxLayout()
        self.combo_tipo = QComboBox()
        tipos = ["por_tema", "por_curso", "por_semestre", "por_anio", "historico"]
        self.combo_tipo.addItems(tipos)
        self.combo_tipo.currentTextChanged.connect(self._on_tipo_changed)
        hl.addWidget(QLabel("Vista:"))
        hl.addWidget(self.combo_tipo)

        self.combo_item = QComboBox()
        self.combo_item.currentTextChanged.connect(self._on_item_changed)
        hl.addWidget(QLabel("Elemento:"))
        hl.addWidget(self.combo_item)

        btn = QPushButton("Generar Rendimiento")
        btn.clicked.connect(self._procesar_rendimiento)
        hl.addWidget(btn)
        layout.addLayout(hl)

        # Área de gráficos o mensaje
        if HAS_MPL:
            self.figure = Figure(tight_layout=True)
            self.figure.patch.set_facecolor('#ECF0F1')
            self.canvas = FigureCanvas(self.figure)
            self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            layout.addWidget(self.canvas)
        else:
            warn = QLabel(
                "<b>Matplotlib no instalado.</b><br>" +
                "Ejecuta: pip install matplotlib",
                self
            )
            warn.setAlignment(Qt.AlignCenter)
            warn.setWordWrap(True)
            warn.setStyleSheet("color: #C0392B; font-size:14pt; margin:20px;")
            layout.addWidget(warn)

        self.setLayout(layout)

    def _obtener_estudiante_id(self):
        path = os.path.join("data", "usuarios.json")
        if not os.path.exists(path):
            return None
        try:
            with open(path, encoding="utf-8") as f:
                users = json.load(f).get("users", [])
            for u in users:
                if u.get("tipo") == "estudiante" and u.get("email", "").strip().lower() == self.estudiante_email.strip().lower():
                    return u.get("id")
        except Exception as e:
            print("Error leyendo usuarios.json:", e)
        return None

    def _generar_solicitud(self):
        if not self.estudiante_id:
            QMessageBox.critical(self, "Error", "ID de estudiante no encontrado.")
            return None
        try:
            with open("data/cursoEstudianteProfesor.json", encoding="utf-8") as f:
                raw = json.load(f).get("cursos", {})
            lista, anio, semestre = [], None, None
            # Buscar cursos donde participe este estudiante
            for y, sems in raw.items():
                for sem, cursos in sems.items():
                    for c in cursos:
                        # filtrar estudiantes dentro de curso
                        alumnos = [a for a in c.get("estudiantes", []) if a.get("id") == self.estudiante_id]
                        if alumnos:
                            copia = c.copy()
                            copia["estudiantes"] = alumnos
                            lista.append(copia)
                            if anio is None:
                                anio, semestre = int(y), int(sem)
            sol = {"estudiante": {"anio": anio, "semestre": semestre, "cursos": lista}}
            path = os.path.join("data", "solicitud.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(sol, f, ensure_ascii=False, indent=4)
            return path
        except Exception as e:
            QMessageBox.critical(self, "Error Solicitud", str(e))
            return None

    def _procesar_rendimiento(self):
        sol = self._generar_solicitud()
        if not sol:
            return
        exe = os.path.join("backend", "rendimiento")
        out = os.path.join("data", "rendimiento.json")
        try:
            subprocess.run([exe, sol, out], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error OCaml", e.stderr)
            return
        self._cargar_datos(out)
        self._on_tipo_changed(self.combo_tipo.currentText())

    def _cargar_datos(self, path):
        try:
            with open(path, encoding="utf-8") as f:
                full = json.load(f)
            self.datos = full.get("estudiante", {})
        except Exception as e:
            QMessageBox.critical(self, "Error Leer JSON", str(e))

    def _on_tipo_changed(self, tipo):
        opciones = self._obtener_opciones(tipo)
        self.combo_item.clear()
        self.combo_item.addItems(opciones)
        if opciones:
            self.combo_item.setCurrentIndex(0)

    def _on_item_changed(self, item):
        if HAS_MPL:
            self._dibujar_grafica()

    def _obtener_opciones(self, tipo):
        datos = self.datos.get(tipo, []) or []
        if tipo == "por_semestre":
            opts = [f"Sem {e.get('semestre')}" for e in datos]
        elif tipo == "por_anio":
            opts = [str(e.get('anio')) for e in datos]
        elif tipo == "historico":
            opts = ["Histórico"]
        else:
            opts = [e.get('curso') for e in datos]
        seen = set()
        return [x for x in opts if x not in seen and not seen.add(x)]

    def _dibujar_grafica(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.grid(color='#BDC3C7', linestyle='--', linewidth=0.5)
        tipo = self.combo_tipo.currentText()
        item = self.combo_item.currentText()
        datos = self.datos.get(tipo, []) or []
        x, y = [], []
        # Seleccionar datos según tipo
        if tipo == 'por_tema':
            for e in datos:
                if e.get('curso') == item:
                    for k, v in e.get('temas', {}).items():
                        x.append(k); y.append(v)
        elif tipo == 'por_curso':
            for e in datos:
                if e.get('curso') == item:
                    for k, v in e.get('resumen', {}).items():
                        x.append(k); y.append(v)
        elif tipo == 'por_semestre':
            for e in datos:
                x.append(f"Sem {e.get('semestre')}"); y.append(e.get('promedio', 0))
        elif tipo == 'por_anio':
            for e in datos:
                x.append(str(e.get('anio'))); y.append(e.get('promedio', 0))
        else:  # historico
            hist = datos[0].get('anios', []) if datos else []
            for a in hist:
                x.append(str(a.get('anio'))); y.append(a.get('promedio', 0))
        # Dibujar
        if not x:
            ax.text(0.5, 0.5, 'Sin datos', ha='center', va='center', transform=ax.transAxes, color='#7F8C8D')
            ax.set_xticks([]); ax.set_yticks([])
        else:
            pos = range(len(x))
            ax.plot(pos, y, marker='o', linestyle='-', color='#27AE60', linewidth=2)
            ax.fill_between(pos, y, color='#82E0AA', alpha=0.3)
            ax.set_xticks(pos)
            ax.set_xticklabels(x, rotation=45, ha='right', color='#2C3E50')
        ax.set_title(f"{tipo.replace('_',' ').title()} - {item}", color='#2C3E50')
        ax.set_ylabel("Puntuación", color='#2C3E50')
        self.canvas.draw()
