from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
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
    
    def imageUpdate(self,func):
        imgFolder = os.path.dirname(self.imgNome)
        imgSave = f"{imgFolder}/NOVO_{os.path.basename(self.imgNome)}"

        imgChange = self.pixelsArray[self.imgInd]
        if (self.imgInd < len(self.img) - 1):
            self.img = self.img[0:self.imgInd - 1]
            self.imgInd = len(self.img) - 1
        else: 
            self.imgInd += 1

        if len(self.pListValue) == 0:
            self.pixelsArray.append(main.alterarImg(imgChange,func,self.paramValue))
            main.salvarImg(imgSave,self.pixelsArray[self.imgInd])
        else:
            self.pixelsArray.append(main.alterarImg(imgChange,func,self.pListValue))
            main.salvarImg(imgSave,self.pixelsArray[self.imgInd])

        self.img.append(QPixmap(imgSave))
        self.changeZoom(self.imgZoom)
        self.dlg.close()

    def abrirImagem(self,imgDefault=None):
        if not imgDefault:
            f = QFileDialog()
            f.setNameFilter("Images (*.png *.jpg)")
            if f.exec():
                self.imgNome = f.selectedFiles()[0]
        else:
            self.imgNome = imgDefault

        self.setWindowTitle(f"{os.path.basename(self.imgNome)} - Manipulador de Imagem")
        self.imgZoom = 100
        self.imgInd += 1
        self.img.append(QPixmap(self.imgNome))
        self.imgDisplay.setPixmap(self.img[self.imgInd])
        self.pixelsArray.append(main.carregarImg(self.imgNome))
        self.sttsDim.setText(f"{len(self.pixelsArray[self.imgInd])}x{len(self.pixelsArray[self.imgInd][0])}")
    
    def salvarImagem(self):
        imgFolder = os.path.dirname(self.imgNome)
        imgSave = f"{imgFolder}/{os.path.basename(self.imgNome)}"
        main.salvarImg(imgSave,self.pixelsArray[self.imgInd])

    def imgHistorico(self,mov):
        if mov:
            if self.imgInd < len(self.img) - 1:
                self.imgInd += 1
        elif self.imgInd > 0:
            self.imgInd -= 1
        
        imgFolder = os.path.dirname(self.imgNome)
        imgSave = f"{imgFolder}/NOVO_{os.path.basename(self.imgNome)}"
        main.salvarImg(imgSave,self.pixelsArray[self.imgInd])
        self.changeZoom(self.imgZoom)

    def changeZoom(self,v):
        print(f"{self.imgInd} - {self.img}")

        if (self.imgInd >= 0):
            self.imgZoom = v
            self.zmLabel.setText(f"{v}%")
            nWidth = round(self.img[self.imgInd].size().width() * (v/100))
            nHeight = round(self.img[self.imgInd].size().height() * (v/100))
            self.imgDisplay.setPixmap(self.img[self.imgInd].scaled(nWidth,nHeight))

    def habilitar(self,t):
        if (t == 'zoom'):
            self.zmLabel.setHidden(not self.zmLabel.isHidden())
            self.zmSlider.setHidden(not self.zmSlider.isHidden())

    def sobre(self):
        self.dlg = QDialog(self)
        self.dlg.setWindowTitle("Sobre")

        layout = QVBoxLayout()

        self.lbl = QLabel("Manipulador de imagem v1.0\nPor Ewerton Bramos")
        layout.addWidget(self.lbl)

        self.dlg.setLayout(layout)
        self.dlg.exec()

    def __init__(self):
        super().__init__()

        # Procurar imagem
        self.setWindowTitle("Manipulador de Imagem")
        self.paramValue = 0
        self.pListValue = []
        self.imgZoom = 1

        # Barra de status
        self.sttsBar = QStatusBar(self)
        self.sttsDim = QLabel("0x0")
        self.sttsBar.addWidget(self.sttsDim)
        self.setStatusBar(self.sttsBar)

        # Imagem
        self.pixelsArray = []
        self.img = []
        self.imgInd = -1
        self.imgDisplay = QLabel(self)

        try:
            self.abrirImagem(f"{os.path.dirname(__file__)}/imagem.png")
        except Exception:
            print(f"Não foi possível abrir a imagem padrão: {Exception}")
            self.pixelsArray = []
            self.img = []
            self.imgInd = -1

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

        # Barra de ferramentas
        mnBtns = []
        sbBtns = []
        mnTxts = (
            (
                'Arquivo',(
                    ('Abrir','Abre uma nova imagem'),
                    ('Salvar','Salva as alterações feitas à uma imagem'),
                    ('Sair','Fecha o programa')
                )
            ),
            (
                'Editar',(
                    ('Desfazer','Desfaz alterações'),
                    ('Refazer','Refaz alterações')
                )
            ),
            (
                'Exibir',(
                    ('Zoom','Habilitar ou desabilitar barra de zoom',True),
                )
            ),
            (
                'Sobre',(
                    ('Sobre o manipulador de imagens...','Exibe informações sobre o programa'),
                )
            )
            )
        self.barraFerramentas = self.menuBar()
        for i in range(len(mnTxts)):
            mnBtns.append(self.barraFerramentas.addMenu(mnTxts[i][0]))
            sbBtns.append([])
            for j in range(len(mnTxts[i][1])):
                sbBtns[i].append(QAction(mnTxts[i][1][j][0],self))
                sbBtns[i][j].setStatusTip(mnTxts[i][1][j][1])
                if (len(mnTxts[i][1][j]) > 2):
                    sbBtns[i][j].setCheckable(True)
                    sbBtns[i][j].setChecked(mnTxts[i][1][j][2])
                mnBtns[i].addAction(sbBtns[i][j])
                
        # Associando funções para cada botão de menu
        sbBtns[0][0].triggered.connect(self.abrirImagem)
        sbBtns[0][1].triggered.connect(self.salvarImagem)
        sbBtns[0][2].triggered.connect(sys.exit)
        sbBtns[1][0].triggered.connect(lambda: self.imgHistorico(False))
        sbBtns[1][1].triggered.connect(lambda: self.imgHistorico(True))
        sbBtns[2][0].triggered.connect(lambda: self.habilitar('zoom'))
        sbBtns[3][0].triggered.connect(lambda: self.sobre())

        # Atalhos
        QShortcut(QKeySequence("Ctrl+O"),self).activated.connect(self.abrirImagem)
        QShortcut(QKeySequence("Ctrl+S"),self).activated.connect(self.salvarImagem)
        QShortcut(QKeySequence("Ctrl+Q"),self).activated.connect(sys.exit)
        QShortcut(QKeySequence("Ctrl+Z"),self).activated.connect(lambda: self.imgHistorico(False))
        QShortcut(QKeySequence("Ctrl+Y"),self).activated.connect(lambda: self.imgHistorico(True))

        # Botões de ferramentas
        toolBtns = []
        btsBarra = QHBoxLayout()
        btsTxts = ('EspelharH','EspelharV','Girar','Inverter','Brilho','Contraste','Cinza','Canais','Borrar','Borda')
        for i in range(len(btsTxts)):
            toolBtns.append(QPushButton(f"{btsTxts[i]}"))
            btsBarra.addWidget(toolBtns[i])

        # Associando funções para cada botão de ferramenta
        toolBtns[0].pressed.connect(lambda: self.btnAction("Espelhar horizontalmente...",'espelharH',1,1))
        toolBtns[1].pressed.connect(lambda: self.btnAction("Espelhar verticalmente...",'espelharV',1,1))
        toolBtns[2].pressed.connect(lambda: self.btnAction("Girar...",'girar',1,1))
        toolBtns[3].pressed.connect(lambda: self.btnAction("Inverter...",main.inverter,1,1))
        toolBtns[4].pressed.connect(lambda: self.btnAction("Brilho...",main.brilho_soma,-255,255))
        toolBtns[5].pressed.connect(lambda: self.btnAction("Contraste...",main.contraste,-255,255))
        toolBtns[6].pressed.connect(lambda: self.btnAction("Cinza...",main.to_grayscale,1,5))
        toolBtns[7].pressed.connect(lambda: self.btnAction("Canais...",main.to_channel,1,3,['R','G','B']))
        toolBtns[8].pressed.connect(lambda: self.btnAction("Borrar...",main.blur,1,10))
        toolBtns[9].pressed.connect(lambda: self.btnAction("Borda...",main.sobel,1,1))

        # Adicionar e posicionar elementos na tela
        layout = QVBoxLayout()
        #layout.addLayout(mnBarra)
        layout.addLayout(btsBarra)
        layout.addWidget(self.imgDisplay)
        layout.addLayout(zmBarra)

        mainWidget = QWidget()
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

        if self.imgInd >= 0:
            self.resize(self.img[self.imgInd].width(), self.img[self.imgInd].height())
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())