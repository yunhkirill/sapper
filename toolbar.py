from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QComboBox, QPushButton, QLabel
from engine import SapperGame


class ToolBar(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.game = SapperGame(8, 10, 10)
        
        self.gameMode = QComboBox()
        self.gameMode.addItems(["Easy", "Medium", "Hard"])
        font = self.gameMode.font()
        font.setPointSize(16)
        self.gameMode.setFont(font)
        self.gameMode.setFixedSize(110, 30)
        self.addWidget(self.gameMode)
        
        #self.addSpacing(50)
        
        self.markedCellsCounter = QLabel(chr(215) + " = " + str(10))
        font = self.markedCellsCounter.font()
        font.setPointSize(16)
        self.markedCellsCounter.setFont(font)
        self.addWidget(self.markedCellsCounter)
        
                
        self.restartButton = QPushButton("Restart")
        self.restartButton.clicked.connect(self.restartButtonClicked)
        font = self.restartButton.font()
        font.setPointSize(16)
        self.restartButton.setFont(font)
        self.restartButton.setIcon(QIcon('Resources/restart.png'))
        self.restartButton.setFixedSize(90, 42)
        self.addWidget(self.restartButton)


    def changeMarkedCellsCounter(self):
        self.markedCellsCounter.setText(chr(215) + " = " + str(self.game.bombQuantity - self.game.markedCellsQuantity))
    
    
    def restartButtonClicked(self):
        self.game.restartGame()
        self.changeMarkedCellsCounter()
