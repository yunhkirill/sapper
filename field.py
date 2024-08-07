import os

from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QGridLayout


class ClickedLabel(QLabel):
    clicked = pyqtSignal(QEvent)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.clicked.emit(event)


class SapperField(QGridLayout):
    def __init__(self, toolbar):
        super().__init__()
        self.toolbar = toolbar
        self.setContentsMargins(5, 5, 5, 5)
        #self.setSpacing(3)
        self.buildField()
        
    
    def buildField(self):
        while self.count():
            child = self.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.cellList = []
        for y in range(self.toolbar.game.cellHeightQuantity):
            cellRow = []
            for x in range(self.toolbar.game.cellWidthQuantity):
                cell = ClickedLabel(objectName = str(y) + "-" + str(x))
                cell.setFixedSize(30, 30)
                if x % 2 == y % 2:               
                    cell.setStyleSheet('background-color: #B9DD77')
                else:
                    cell.setStyleSheet('background-color: #A2D149')
                cell.clicked.connect(self.cellWasClicked)
                self.addWidget(cell, y, x)
                cellRow.append(cell)
            self.cellList.append(cellRow)
    
    
    def changeField(self):
        for y in range(self.toolbar.game.cellHeightQuantity):
            for x in range(self.toolbar.game.cellWidthQuantity):
                if self.toolbar.game.field[y][x].visibilityState:
                    if self.toolbar.game.field[y][x].value != 0:
                        font = self.cellList[y][x].font()
                        font.setPointSize(30)
                        self.cellList[y][x].setFont(font)
                        self.cellList[y][x].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                        self.cellList[y][x].setText(str(self.toolbar.game.field[y][x].value))
                    else:
                        self.cellList[y][x].setText("")
                    if y % 2 == x % 2:
                        self.cellList[y][x].setStyleSheet('background-color: #E5C29F')
                    else:
                        self.cellList[y][x].setStyleSheet('background-color: #DEB887')
                elif self.toolbar.game.field[y][x].markState:
                    font = self.cellList[y][x].font()
                    font.setPointSize(30)
                    self.cellList[y][x].setFont(font)
                    self.cellList[y][x].setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                    self.cellList[y][x].setText(chr(215))
                elif not self.toolbar.game.field[y][x].markState:
                    self.cellList[y][x].setText('')
                    
                        
    def cellWasClicked(self, event):
        if self.toolbar.game.gameOver:
            return
        
        cell = self.sender()
        heightIndex, widthIndex = map(int, cell.objectName().split('-'))
        if event.button() == Qt.MouseButton.LeftButton:
            if self.toolbar.game.firstMoveState:
                self.toolbar.game.startGame(heightIndex, widthIndex)
            else:
                self.toolbar.game.selectCell(heightIndex, widthIndex)

            if self.toolbar.game.gameOver:
                self.drawBomb(heightIndex, widthIndex)
            else:
                self.toolbar.changeMarkedCellsCounter()
                self.changeField()

        elif event.button() == Qt.MouseButton.RightButton:
            if not self.toolbar.game.firstMoveState:
                self.toolbar.game.markCell(heightIndex, widthIndex)
                self.toolbar.changeMarkedCellsCounter()
                self.changeField()
    
    
    def drawBomb(self, heightIndex, widthIndex):
        self.cellList[heightIndex][widthIndex].setScaledContents(True)
        self.cellList[heightIndex][widthIndex].setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), 'Resources/bomb.png')))  
