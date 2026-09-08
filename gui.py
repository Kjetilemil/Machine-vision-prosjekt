import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow



def create_window():
    window = QMainWindow()
    window.setWindowTitle("Prosjekt gruppe 6")
    window.resize(400, 300)
    return window




def run_window():
    app = QApplication(sys.argv)
    window = create_window()
    window.show()
    sys.exit(app.exec())
