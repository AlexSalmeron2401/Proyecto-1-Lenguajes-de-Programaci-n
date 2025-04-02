import sys
from PyQt5.QtWidgets import QApplication
from frontend.vista_login import VentanaLogin

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaLogin()
    ventana.show()
    sys.exit(app.exec_())