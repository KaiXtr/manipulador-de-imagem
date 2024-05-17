from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import main
import sys
import os

class MainWindow(QMainWindow):
    def btnAction(self,dlgTitle,func,minV,maxV,lblTxts=[]):
        self.dlg = QDialog(self)
        self.dlg.setWindowTitle(dlgTitle)

        if minV == maxV:
            self.imageUpdate(func)
            return

        stVal = round((maxV + minV)/2)
        self.paramValue = stVal
        self.pListValue = []

        button = QPushButton("Aplicar")
        button.pressed.connect(lambda: self.imageUpdate(func))

        layout = QVBoxLayout()

        if len(lblTxts) == 0:
            self.paramText = QLabel(str(stVal))
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setValue(stVal)
            slider.setRange(minV,maxV)
            slider.setSingleStep(1)
            slider.valueChanged.connect(self.sliderChange)

            layout.addWidget(self.paramText)
            layout.addWidget(slider)
        else:
            self.pListValue = [0,0,0]
            labels = []
            checkboxes = []
            sublyts = []
            lyts = []

            for i in range(minV,maxV + 1):
                trueI = i - minV
                checkboxes.append(QCheckBox())
                checkboxes[trueI].setChecked(False)
                labels.append(QLabel(lblTxts[trueI]))

                lyts.append(QHBoxLayout())
                lyts[trueI].addWidget(checkboxes[trueI])
                lyts[trueI].addWidget(labels[trueI])

                sublyts.append(QWidget())
                sublyts[trueI].setLayout(lyts[trueI])
                layout.addWidget(sublyts[trueI])

            checkboxes[0].toggled.connect(lambda: self.checkboxChange(0))
            checkboxes[1].toggled.connect(lambda: self.checkboxChange(1))
            checkboxes[2].toggled.connect(lambda: self.checkboxChange(2))

        layout.addWidget(button)
        self.dlg.setLayout(layout)
        self.dlg.exec()

    def sliderChange(self,v):
        self.paramValue = v
        self.paramText.setText(str(v))

    def checkboxChange(self,i):
        if self.sender().isChecked():
            self.pListValue[i] = 1
        else:
            self.pListValue[i] = 0
        print(self.pListValue)
    
    def imageUpdate(self,func):
        imgFolder = os.path.dirname(self.imgNome)
        imgSave = f"{imgFolder}/NOVO_{os.path.basename(self.imgNome)}"

        if len(self.pListValue) == 0:
            self.pixelsArray = main.alterarImg(self.pixelsArray,func,self.paramValue)
            main.salvarImg(imgSave,self.pixelsArray)
        else:
            self.pixelsArray = main.alterarImg(self.pixelsArray,func,self.pListValue)
            main.salvarImg(imgSave,self.pixelsArray)
        
        if (self.imgInd < len(self.img) - 1):
            self.img = self.img[0:self.imgInd + 1]
        self.imgInd += 1
        self.img.append(QPixmap(imgSave))
        self.changeZoom(self.imgZoom)
        self.dlg.close()

    def abrirImagem(self,imgDefault=None):
        if imgDefault == None:
            f = QFileDialog()
            f.setNameFilter("Images (*.png *.jpg)")
            if f.exec():
                self.imgNome = f.selectedFiles()[0]
        else:
            self.imgNome = imgDefault

        self.imgZoom = 100
        self.imgInd += 1
        self.img.append(QPixmap(self.imgNome))
        self.imgDisplay.setPixmap(self.img[self.imgInd])
        self.pixelsArray = main.carregarImg(self.imgNome)
    
    def salvarImagem(self):
        imgFolder = os.path.dirname(self.imgNome)
        imgSave = f"{imgFolder}/{os.path.basename(self.imgNome)}"
        main.salvarImg(imgSave,self.pixelsArray)

    def imgHistorico(self,mov):
        if mov:
            if self.imgInd < len(self.img) - 1:
                self.imgInd += 1
        elif self.imgInd > 0:
            self.imgInd -= 1
        
        self.changeZoom(self.imgZoom)

    def changeZoom(self,v):
        self.imgZoom = v
        self.zmLabel.setText(f"{v}%")
        nWidth = round(self.img[self.imgInd].size().width() * (v/100))
        nHeight = round(self.img[self.imgInd].size().height() * (v/100))
        self.imgDisplay.setPixmap(self.img[self.imgInd].scaled(nWidth,nHeight))

    def __init__(self):
        super().__init__()

        # Procurar imagem
        self.setWindowTitle("Manipulador de Imagem")
        self.paramValue = 0
        self.pListValue = []
        self.imgZoom = 1

        # Imagem
        self.img = []
        self.imgInd = -1
        self.imgDisplay = QLabel(self)
        self.abrirImagem('src/imagem.png')

        # Botões de menu
        mnBtns = []
        mnBarra = QHBoxLayout()
        btsTxts = ('Abrir','Salvar','Desfazer','Refazer')
        for i in range(len(btsTxts)):
            mnBtns.append(QPushButton(f"{btsTxts[i]}"))
            mnBarra.addWidget(mnBtns[i])
        
        # Associando funções para cada botão de menu
        mnBtns[0].pressed.connect(self.abrirImagem)
        mnBtns[1].pressed.connect(self.salvarImagem)
        mnBtns[2].pressed.connect(lambda: self.imgHistorico(False))
        mnBtns[3].pressed.connect(lambda: self.imgHistorico(True))

        # Botões de ferramentas
        toolBtns = []
        btsBarra = QHBoxLayout()
        btsTxts = ('Brilho','Contraste','Cinza','Canais','Borrar','Borda')
        for i in range(len(btsTxts)):
            toolBtns.append(QPushButton(f"{btsTxts[i]}"))
            btsBarra.addWidget(toolBtns[i])

        # Associando funções para cada botão de ferramenta
        toolBtns[0].pressed.connect(lambda: self.btnAction("Brilho...",main.brilho_soma,-255,255))
        toolBtns[1].pressed.connect(lambda: self.btnAction("Contraste...",main.contraste,-255,255))
        toolBtns[2].pressed.connect(lambda: self.btnAction("Cinza...",main.to_grayscale,1,5))
        toolBtns[3].pressed.connect(lambda: self.btnAction("Canais...",main.to_channel,1,3,['R','G','B']))
        toolBtns[4].pressed.connect(lambda: self.btnAction("Borrar...",main.blur,1,10))
        toolBtns[5].pressed.connect(lambda: self.btnAction("Borda...",main.sobel,1,1))

        # Barra de zoom
        self.zmLabel = QLabel('1%')
        self.zmSlider = QSlider(Qt.Orientation.Horizontal)
        self.zmSlider.setMinimum(1)
        self.zmSlider.setMaximum(1000)
        self.zmSlider.setSingleStep(1)
        self.zmSlider.valueChanged.connect(self.changeZoom)

        zmBarra = QHBoxLayout()
        zmBarra.addWidget(self.zmLabel)
        zmBarra.addWidget(self.zmSlider)

        # Adicionar e posicionar elementos na tela
        layout = QVBoxLayout()
        layout.addLayout(mnBarra)
        layout.addLayout(btsBarra)
        layout.addWidget(self.imgDisplay)
        layout.addLayout(zmBarra)

        mainWidget = QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)
        self.resize(self.img[self.imgInd].width(), self.img[self.imgInd].height())
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())