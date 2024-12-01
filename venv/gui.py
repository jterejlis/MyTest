import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ustawienia okna
        self.setWindowTitle("Moje pierwsze GUI")
        self.setGeometry(100, 100, 500, 500)

        # Tworzenie widgetów
        label = QLabel("MyTest.exe", self)
        button = QPushButton("Kliknij mnie", self)
        #extview = text

        # Połączenie przycisku z akcją
        button.clicked.connect(self.on_button_click)

        # Użycie layoutu
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)

        # Kontener centralny
        container = QWidget()
        container.setLayout(layout)

        # Ustawienie kontenera jako centralnego widgetu
        self.setCentralWidget(container)

    def on_button_click(self):
        self.setWindowTitle("Przycisk kliknięty!")


app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())