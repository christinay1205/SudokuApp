from cmu_112_graphics import *
import copy

class MyApp(App):
    def appStarted(self):
        self.board = self.startBoard()
        self.margin = 10
        self.rows = 9
        self.cols = 9
        self.selection = (-1, -1) #(row, col) of selection, (-1, -1) none
        self.play = copy.deepcopy (self.board)
        self.direction  = (0, 0)
        self.boardsize = 3 # 3x3 sudoku
    
    @staticmethod   
    def startBoard ():
        board=[
    [ 1, 2, 3, 4, 5, 6, 0, 8, 9],
    [ 5, 0, 8, 1, 3, 9, 6, 2, 4],
    [ 4, 9, 6, 8, 7, 2, 1, 5, 3],
    [ 9, 5, 2, 3, 0, 1, 4, 6, 7],
    [ 6, 0, 1, 2, 9, 7, 8, 3, 5],
    [ 3, 8, 7, 5, 6, 4, 0, 9, 1],
    [ 7, 1, 9, 6, 2, 3, 5, 4, 8],
    [ 8, 6, 0, 9, 1, 5, 3, 7, 2],
    [ 2, 3, 5, 7, 4, 8, 9, 1, 6]
        ]
    
        return board

    def mousePressed(self, event):
        #if (self.isGameOver() == False):
        (row, col) = getLocation.getCell(self, event.x, event.y)
        # select this (row, col) unless it is selected
        if (self.selection == (row, col)):
            self.selection = (-1, -1)
        else:
            self.selection = (row, col)

    def keyPressed(self, event):
        num = event.key
        #if (self.isGameOver() == False):
        if (num == 'Up'):      self.direction = (-1, 0)
        elif (num == 'Down'):  self.direction = (1, 0)
        elif (num == 'Left'):  self.direction = (0, -1)
        elif (num == 'Right'): self.direction = (0, 1)
        else: self.direction = (0, 0)
        if (num == 'Backspace'):
            if (self.selection != (-1, -1) and self.board[self.selection[0]][self.selection[1]]==0):
                self.play[self.selection[0]][self.selection[1]]=0
        if (num == '1' or num == '2' or num == '3' or num == '4' or num =='5' or num =='6' or num =='7' or num =='8' or num =='9'):
            if (self.selection != (-1, -1) and self.board[self.selection[0]][self.selection[1]]==0):
                self.play[self.selection[0]][self.selection[1]]=int(num)
        self.moveSelection()

    def moveSelection (self):
        (dx, dy) = self.direction
        (newx, newy) = (self.selection[0]+dx, self.selection[1]+dy)
        if (newx < 0  or newx >= self.rows or newy <0 or newy >= self.cols):
            return
        else:
            self.selection = (newx,newy) 

    def isGameOver(self):
        for row in range (self.rows):
            for col in range (self.cols):
                if (self.play[row][col]==0):
                    return False
        if (CheckSudoku.isLegalSudoku(self,self.play)==True):
            return True
        
    def redrawAll(self, canvas):
        (x0, y0, x1, y1) = getLocation.getCellBounds(self, self.selection[0], self.selection[1])
        canvas.create_rectangle(x0, y0, x1, y1, fill="lightgray")
        drawBoard.drawSudokuBoard(self, canvas, self.width, self.height, self.play, self.margin)
        if (self.isGameOver() == True):
            canvas.create_rectangle(self.margin, self.height/2-25, self.width-self.margin, self.height/2+25, fill = "lightgrey", width = 0)
            canvas.create_text(self.width/2, self.height/2, text = "You Win!", font = 'Cambria 30 bold')

class drawBoard(MyApp):
    def drawSudokuBoard(self, canvas, width, height, board, margin):
        drawBoard.drawVertLines(self, canvas, width, height, board, margin)
        drawBoard.drawHorizLines(self, canvas, width, height, board, margin)
        drawBoard.drawNum(self, canvas, width, height, board, margin)

    def drawVertLines(self, canvas, width, height, board, margin):
        #vertical boxed lines
        vstartx1 = margin
        vendx1 = width-margin
        blockwidth = int((vendx1-vstartx1)/self.boardsize)
        cellwidth = int(blockwidth/self.boardsize)
        for incx in range (vstartx1, vendx1+blockwidth, blockwidth):
            canvas.create_line(incx, margin, incx, height-margin, width = 5)
            for incxthin in range (incx, incx+blockwidth, cellwidth):
                canvas.create_line(incxthin, margin, incxthin, height-margin, width = 1)
    
        #horizontal boxed lines
    def drawHorizLines(self, canvas, width, height, board, margin):
        hstarty1 = margin
        hendy  = height-margin
        blockheight = int((hendy-hstarty1)/self.boardsize)
        cellheight = int(blockheight/self.boardsize)
        for incy in range (hstarty1, hendy+blockheight, blockheight):
            canvas.create_line(margin, incy, width-margin, incy, width = 5)
            for incythin in range (incy, incy+blockheight, cellheight):
                canvas.create_line(margin, incythin, width-margin, incythin, width = 1)
        
        #fill in the text
    def drawNum(self, canvas, width, height, board, margin):
        blockwidth = int((width-2*margin)/self.boardsize)
        blockheight = int((height-2*margin)/self.boardsize)
        cellwidth = int(blockwidth/self.boardsize)
        cellheight = int(blockheight/self.boardsize)
        for boardx in range (len(board)): #loop over the rows
            for boardy in range (len(board[0])): #loop over the columns
                blockx = int(margin+cellwidth/2+cellwidth*boardx)
                blocky = int(margin+cellheight/2+cellheight*boardy)
                
                if (self.board[boardy][boardx]==0 and self.play[boardy][boardx]!=0):
                    if (CheckSudoku.isLegalSudoku(self,self.play)==False):
                        fill = "red" #bug: its red for all proceeding numbers until sudoku is legal
                    else: fill = "midnightblue"
                else:
                    fill = "black"
                #center the text near thick boxed lines 
                if (board[boardy][boardx] !=0):
                    if (boardx != 0 and boardy !=0 and boardx%self.boardsize == 0 and boardy%self.boardsize == 0):
                        canvas.create_text(blockx+3,blocky+3, text=str(board[boardy][boardx]), fill = fill, font='Cambria 25')
                    elif (boardx != 0 and boardx%self.boardsize == 0):
                        canvas.create_text(blockx+3,blocky, text=str(board[boardy][boardx]), fill = fill, font='Cambria 25')
                    elif (boardy != 0 and boardy%self.boardsize == 0):
                        canvas.create_text(blockx,blocky+3, text=str(board[boardy][boardx]), fill = fill, font='Cambria 25')
                    else:
                        canvas.create_text(blockx,blocky, text=str(board[boardy][boardx]), fill = fill, font='Cambria 25')

class getLocation(MyApp):
    def pointInGrid(self, x, y):
        # return True if (x, y) is inside the grid defined by self.
        return ((self.margin <= x <= self.width-self.margin) and
                (self.margin <= y <= self.height-self.margin))

    def getCell(self, x, y):
        # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
        if (not getLocation.pointInGrid(self, x, y)):
            return (-1, -1)
        blockwidth  = self.width - 2*self.margin
        blockheight = self.height - 2*self.margin
        cellwidth  = blockwidth / self.cols
        cellheight = blockheight / self.rows
        row = int((y - self.margin) / cellheight)
        col = int((x - self.margin) / cellwidth)
        return (row, col)

    def getCellBounds(self, row, col):
        # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        blockwidth  = self.width - 2*self.margin
        blockheight = self.height - 2*self.margin
        columnwidth = blockwidth / self.cols
        rowheight = blockheight / self.rows
        x0 = self.margin + col * columnwidth
        x1 = self.margin + (col+1) * columnwidth
        y0 = self.margin + row * rowheight
        y1 = self.margin + (row+1) * rowheight
        return (x0-1, y0-1, x1-1, y1-1)

class CheckSudoku(MyApp):
    def areLegalValues(self, values):
        if (len(values) != 9):
            return False
        if (max(values)>9 or min(values)<0):
            return False
        for i in range (1,10):
            if (values.count(i)>1):
                return False
        return True

    def isLegalRow(self, board, row):
        a = board[row]
        return CheckSudoku.areLegalValues(self, a)

    def isLegalCol(self, board, col):
        a = []
        for index in range (len(board)):
            a.append(board[index][col])
        return CheckSudoku.areLegalValues(self, a)

    def isLegalBlock(self, board, block):
        row = block//self.boardsize*self.boardsize
        col = (block-row)*self.boardsize
        a = []
        for r in range (self.boardsize):
            for c in range (self.boardsize):
                a.append(board[row+r][col+c])
        return CheckSudoku.areLegalValues(self, a)

    def isLegalSudoku(self, board):
        for r in range (len(board)):
            if (CheckSudoku.isLegalRow(self, board, r)==False):
                return False
            if (CheckSudoku.isLegalCol(self, board, r)==False):
                return False
            if (CheckSudoku.isLegalBlock(self, board, r)==False):
                return False
        return True


MyApp(width=600, height=600)