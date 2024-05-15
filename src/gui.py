from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import main
import sys
import os

class MainWindow(QMainWindow):
    def btnAction(self,dlgTitle,func,minV,maxV):
        self.dlg = QDialog(self)
        self.dlg.setWindowTitle(dlgTitle)

        stVal = round(minV/2)
        self.sliderText = QLabel(str(stVal))
        self.sliderValue = stVal

        sParam = 0
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(minV)
        slider.setMaximum(maxV)
        slider.setSingleStep(1)
        slider.valueChanged.connect(self.sliderChange)

        button = QPushButton("Aplicar")
        button.pressed.connect(lambda: self.imageUpdate(func))

        layout = QVBoxLayout()
        layout.addWidget(self.sliderText)
        layout.addWidget(slider)
        layout.addWidget(button)
        self.dlg.setLayout(layout)

        self.dlg.exec()

    def sliderChange(self,v):
        self.sliderValue = v
        self.sliderText.setText(str(v))
    
    def imageUpdate(self,func):
        caminho = os.path.dirname(os.path.abspath(__file__))
        imgFolder = os.path.dirname(self.imgNome)
        #imgSave = f"{caminho}/../out/TESTE_{os.path.basename(self.imgNome)}"
        imgSave = f"{imgFolder}/NOVO_{os.path.basename(self.imgNome)}"

        main.alterarImg(imgSave,self.pixelsArray,func,self.sliderValue)
        self.img = QPixmap(imgSave)
        self.imgDisplay.setPixmap(self.img)
        self.dlg.close()

    def abrirImagem(self):
        self.imgNome = 'balao.jpg'
        f = QFileDialog()
        f.setNameFilter("Images (*.png *.jpg)")
        if f.exec():
            self.imgNome = f.selectedFiles()[0]

        self.img = QPixmap(self.imgNome)
        self.imgDisplay.setPixmap(self.img)
        self.pixelsArray = main.carregarImg(self.imgNome)

    def __init__(self):
        super().__init__()

        # Procurar imagem
        self.setWindowTitle("Manipulador de Imagem")
        self.sliderValue = 0

        # Imagem
        self.imgDisplay = QLabel(self)
        self.abrirImagem()

        # Botões
        toolBtns = []
        btsBarra = QHBoxLayout()
        btsTxts = ('Abrir','Brilho','Contraste','Cinza')
        for i in range(4):
            toolBtns.append(QPushButton(f"{btsTxts[i]}"))
            btsBarra.addWidget(toolBtns[i])

        # Associando funções para cada botão
        toolBtns[0].pressed.connect(lambda: self.abrirImagem())
        toolBtns[1].pressed.connect(lambda: self.btnAction("Brilho...",main.brilho_soma,-255,255))
        toolBtns[2].pressed.connect(lambda: self.btnAction("Contraste...",main.contraste,-255,255))
        toolBtns[3].pressed.connect(lambda: self.btnAction("Cinza...",main.to_grayscale,1,5))

        layout = QVBoxLayout()
        layout.addLayout(btsBarra)
        layout.addWidget(self.imgDisplay)

        mainWidget = QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)
        self.resize(self.img.width(), self.img.height())
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())