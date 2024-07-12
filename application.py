import sys

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QWidget
from field import SapperField
from toolbar import ToolBar
from engine import SapperGame


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sapper')
        self.setFixedSize(QSize(322, 320))

        self.layout = QVBoxLayout()
        
        self.toolbar = ToolBar()
        self.field = SapperField(self.toolbar)
        
        self.toolbar.restartButton.clicked.connect(self.field.buildField)
        self.toolbar.gameMode.currentIndexChanged.connect(self.changeGameMode)

        self.layout.addLayout(self.toolbar) 
        self.layout.addLayout(self.field)      

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)
        self.show()
        
    
    def changeGameMode(self, index):
        if index == 0:
            self.setFixedSize(QSize(322, 320))
            self.toolbar.game = SapperGame(8, 10, 10)
        elif index == 1:
            self.setFixedSize(QSize(562, 500))
            self.toolbar.game = SapperGame(14, 18, 40)
        else:
            self.setFixedSize(QSize(746, 682))
            self.toolbar.game = SapperGame(20, 24, 99)
        self.field.buildField()
        self.toolbar.changeMarkedCellsCounter()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
