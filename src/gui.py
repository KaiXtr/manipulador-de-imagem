from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
import main
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Procurar imagem
        imgNome = 'balao.jpg'
        f = QFileDialog()
        f.setNameFilter("Images (*.png *.jpg)")
        if f.exec():
            imgNome = f.selectedFiles()[0]
        print(imgNome)

        self.setWindowTitle("Manipulador de Imagem")

        # Botões
        toolBtns = []
        btsBarra = QHBoxLayout()
        for i in range(3):
            toolBtns.append(QPushButton(f"{i + 1}"))
            btsBarra.addWidget(toolBtns[i])

        toolBtns[i].pressed.connect(self.close)

        # Imagem
        label = QLabel(self)
        img = QPixmap(imgNome)
        label.setPixmap(img)

        layout = QVBoxLayout()
        layout.addLayout(btsBarra)
        layout.addWidget(label)

        mainWidget = QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)
        self.resize(img.width(), img.height())
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())