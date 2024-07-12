from random import randint

class Cell:
    def __init__(self, value = 0, visibilityState = False, markState = False):
        self.value = value
        self.visibilityState = visibilityState
        self.markState = markState


class Field:
    def __init__(self, cellHeightQuantity, cellWidthQuantity, bombQuantity):
        self.__cellHeightQuantity = cellHeightQuantity
        self.__cellWidthQuantity = cellWidthQuantity
        self.__bombQuantity = bombQuantity
        self.__field = [[Cell() for i in range(cellWidthQuantity)] for j in range(cellHeightQuantity)]
        self.markedCellsQuantity = 0


    @property
    def field(self):
        return self.__field


    @property
    def cellHeightQuantity(self):
        return self.__cellHeightQuantity


    @property
    def cellWidthQuantity(self):
        return self.__cellWidthQuantity
     
     
    @property
    def bombQuantity(self):
        return self.__bombQuantity
    
    
    def clearField(self):
        self.__field = [[Cell() for i in range(self.__cellWidthQuantity)] for j in range(self.__cellHeightQuantity)]


    def __str__(self):
        result = ""
        for row in self.__field:
            for cell in row:
                result += str(cell.value) #if (cell.visibilityState == True) else "?" 
                result += "\t"
            result += "\n"
        return result


class SapperGame(Field):
    def __init__(self, cellHeightQuantity, cellWidthQuantity, bombQuantity):
        super().__init__(cellHeightQuantity, cellWidthQuantity, bombQuantity)
        self.firstMoveState = True
        self.gameOver = False

    
    def restartGame(self):
        super().clearField()
        self.firstMoveState = True
        self.gameOver = False
        self.markedCellsQuantity = 0


    def startGame(self, firstMoveHeight, firstMoveWidth):
        self.firstMoveState = False
        self.__generateRandomBombs(firstMoveHeight, firstMoveWidth)
        self.__defineEmptyCells()
        self.selectCell(firstMoveHeight, firstMoveWidth)
        print(self)
            
    
    def selectCell(self, heightIndex, widthIndex):
        if self.field[heightIndex][widthIndex].visibilityState:
            return 
        
        if self.field[heightIndex][widthIndex].value == -1:
            self.field[heightIndex][widthIndex].visibilityState = True
            self.gameOver = True
        elif self.field[heightIndex][widthIndex].value == 0:
            start = (heightIndex, widthIndex)
            connectedEmptyCells = set()
            connectedEmptyCells = self.__selectConnectedEmptyCells(start, connectedEmptyCells)
            self.__makeNearbyCellsVisible(connectedEmptyCells)
        else:
            self.field[heightIndex][widthIndex].visibilityState = True
            self.__makeCellUnmarked(heightIndex, widthIndex)
            
                
    def markCell(self, heightIndex, widthIndex):
        if not self.field[heightIndex][widthIndex].visibilityState:
            if self.field[heightIndex][widthIndex].markState:
                self.field[heightIndex][widthIndex].markState = False
                self.markedCellsQuantity -= 1
            else:
                self.field[heightIndex][widthIndex].markState = True
                self.markedCellsQuantity += 1


    def __generateRandomBombs(self, firstMoveHeight, firstMoveWidth):
        bombQuantityCopy = self.bombQuantity
        while (bombQuantityCopy != 0):
            randomHeight = randint(0, self.cellHeightQuantity - 1)
            randomWidth = randint(0, self.cellWidthQuantity - 1)
            if self.field[randomHeight][randomWidth].value == 0 and randomHeight != firstMoveHeight and randomWidth != firstMoveWidth:
                self.field[randomHeight][randomWidth].value = -1
                bombQuantityCopy -= 1
    
    
    def __defineEmptyCells(self):
        for i in range(self.cellHeightQuantity):
            for j in range(self.cellWidthQuantity):
                if self.field[i][j].value == 0:
                    self.field[i][j].value = self.__countNearbyBombs(i, j)
    
    
    def __countNearbyBombs(self, heightIndex, widthIndex):
        getValue = lambda x: x.value
        if heightIndex == 0 and widthIndex == 0:
            return list(map(getValue, self.field[1][:2])).count(-1) + (self.field[0][1].value == -1)

        elif heightIndex == 0 and widthIndex == self.cellWidthQuantity - 1:
            return list(map(getValue, self.field[1][-1:-3:-1])).count(-1) + (self.field[0][widthIndex - 1].value == -1)

        elif heightIndex == self.cellHeightQuantity - 1 and widthIndex == 0:
            return list(map(getValue, self.field[heightIndex - 1][:2])).count(-1) + (self.field[heightIndex][1].value == -1)
        
        elif heightIndex == self.cellHeightQuantity - 1 and widthIndex == self.cellWidthQuantity - 1:
            return list(map(getValue, self.field[heightIndex - 1][-1:-3:-1])).count(-1) + (self.field[heightIndex][widthIndex - 1].value == -1)

        elif heightIndex == 0:
            return list(map(getValue, self.field[1][widthIndex - 1 : widthIndex + 2])).count(-1) + (self.field[0][widthIndex - 1].value == -1) + (self.field[0][widthIndex + 1].value == -1)

        elif widthIndex == 0:
            return list(map(getValue, self.field[heightIndex + 1][:2])).count(-1) + list(map(getValue, self.field[heightIndex - 1][:2])).count(-1) + (self.field[heightIndex][widthIndex + 1].value == -1)

        elif heightIndex == self.cellHeightQuantity - 1:
            return list(map(getValue, self.field[heightIndex - 1][widthIndex - 1 : widthIndex + 2])).count(-1) + (self.field[heightIndex][widthIndex - 1].value == -1) + (self.field[heightIndex][widthIndex + 1].value == -1)

        elif widthIndex == self.cellWidthQuantity - 1:
            return list(map(getValue, self.field[heightIndex + 1][-1:-3:-1])).count(-1) + list(map(getValue, self.field[heightIndex - 1][-1:-3:-1])).count(-1) + (self.field[heightIndex][widthIndex - 1].value == -1)

        else:
            return list(map(getValue, self.field[heightIndex + 1][widthIndex - 1 : widthIndex + 2])).count(-1) + list(map(getValue, self.field[heightIndex - 1][widthIndex - 1 : widthIndex + 2])).count(-1) + (self.field[heightIndex][widthIndex - 1].value == -1) + (self.field[heightIndex][widthIndex + 1].value == -1)
    
    
    def __selectConnectedEmptyCells(self, start, connectedEmptyCells):
        connectedEmptyCells.add(start)
        self.field[start[0]][start[1]].visibilityState = True
        self.__makeCellUnmarked(start[0], start[1])
    
        nearbyCells = [(start[0] + 1, start[1]), (start[0] - 1, start[1]), (start[0], start[1] + 1), (start[0], start[1] - 1), (start[0] + 1, start[1] - 1), (start[0] - 1, start[1] - 1), (start[0] + 1, start[1] + 1), (start[0] - 1, start[1] + 1)]

        for nextCell in nearbyCells:
            if 0 <= nextCell[0] < self.cellHeightQuantity and 0 <= nextCell[1] < self.cellWidthQuantity:
                if nextCell not in connectedEmptyCells and self.field[nextCell[0]][nextCell[1]].value == 0:
                    self.__selectConnectedEmptyCells(nextCell, connectedEmptyCells)
        
        return connectedEmptyCells
    
    
    def __makeNearbyCellsVisible(self, connectedEmptyCells):
        for start in connectedEmptyCells:
            nearbyCells = [(start[0] + 1, start[1]), (start[0] - 1, start[1]), (start[0], start[1] + 1), (start[0], start[1] - 1), (start[0] + 1, start[1] - 1), (start[0] - 1, start[1] - 1), (start[0] + 1, start[1] + 1), (start[0] - 1, start[1] + 1)]
            for nextCell in nearbyCells:
                if 0 <= nextCell[0] < self.cellHeightQuantity and 0 <= nextCell[1] < self.cellWidthQuantity:
                    self.field[nextCell[0]][nextCell[1]].visibilityState = True
                    self.__makeCellUnmarked(nextCell[0], nextCell[1])
    
    
    def __makeCellUnmarked(self, heightIndex, widthIndex):
        if self.field[heightIndex][widthIndex].markState:
            self.field[heightIndex][widthIndex].markState = False
            self.markedCellsQuantity -= 1
    
    
    def __str__(self):
        return super().__str__()