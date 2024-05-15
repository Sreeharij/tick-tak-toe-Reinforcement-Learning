import pygame
import time
import random
import tkinter as tk

WIDTH = 600
HEIGHT = 600

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

gridPos = (75,100)
cellSize = 150
gridSize = cellSize*3

class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.selected = 1
        self.mousePos = None
        self.cells_used = {
                            1:[False,None,WHITE,(0,0)],4:[False,None,WHITE,(0,1)],7:[False,None,WHITE,(0,2)],
                            2:[False,None,WHITE,(1,0)],5:[False,None,WHITE,(1,1)],8:[False,None,WHITE,(1,2)],
                            3:[False,None,WHITE,(2,0)],6:[False,None,WHITE,(2,1)],9:[False,None,WHITE,(2,2)]
                          }

        self.gameOver = False
        self.lastEntered = None
        self.cells_used_no = 0
        self.computer_mode_enabled = False
        print(self.gameOver)

    def run(self):
        while self.running:
            self.events()
            self.draw()
        pygame.quit()
        main()

    def events(self):
        for event in pygame.event.get():
            self.mousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
            if event.type == pygame.KEYDOWN:

            ############# KEYBOARD NAVIGATION ##################
                if event.key == pygame.K_RIGHT and self.selected != 9:
                    self.selected+=1
                if event.key == pygame.K_LEFT and self.selected != 1:
                    self.selected-=1
                if event.key == pygame.K_UP and self.selected not in (1,2,3):
                    self.selected-=3
                if event.key == pygame.K_DOWN and self.selected not in (7,8,9):
                    self.selected+=3

            ############# XO input #########################
                if not self.cells_used[self.selected][0] and (event.key != self.lastEntered):
                    if event.key == pygame.K_x:
                            self.lastEntered = pygame.K_x
                            self.cells_used[self.selected][0] = True
                            self.cells_used[self.selected][1] = 'X'
                            self.cells_used[self.selected][2] = BLUE
                            self.cells_used_no += 1

                    if event.key == pygame.K_o:
                        if not self.computer_mode_enabled:
                                self.lastEntered = pygame.K_o
                                self.cells_used[self.selected][0] = True
                                self.cells_used[self.selected][1] = 'O'
                                self.cells_used[self.selected][2] = GREEN
                                self.cells_used_no += 1

            self.check_grid()
            if self.lastEntered == pygame.K_x:
                self.computer_mode()


    def computer_mode(self):
        if self.computer_mode_enabled:
            self.draw()
            time.sleep(1)
            self.cell = random.randint(1,9)
            while self.cells_used[self.cell][0] == True:
                self.cell = random.randint(1,9)
            self.selected = self.cell
            self.lastEntered = pygame.K_o
            self.cells_used[self.selected][0] = True
            self.cells_used[self.selected][1] = 'O'
            self.cells_used[self.selected][2] = GREEN
            self.cells_used_no += 1
            self.check_grid()



    def check_grid(self):
        ############# CHECKS WINNING CONDITIONS ######################

        if self.cells_used[1][1] == self.cells_used[2][1] == self.cells_used[3][1] != None:
            game_Over(self,self.cells_used[1][1]+" Won!")
        elif self.cells_used[4][1] == self.cells_used[5][1] == self.cells_used[6][1] != None:
            game_Over(self,self.cells_used[4][1]+" Won!")
        elif self.cells_used[7][1] == self.cells_used[8][1] == self.cells_used[9][1] != None:
            game_Over(self,self.cells_used[7][1]+" Won!")
        elif self.cells_used[1][1] == self.cells_used[4][1] == self.cells_used[7][1] != None:
            game_Over(self,self.cells_used[1][1]+" Won!")
        elif self.cells_used[2][1] == self.cells_used[5][1] == self.cells_used[8][1] != None:
            game_Over(self,self.cells_used[2][1]+" Won!")
        elif self.cells_used[3][1] == self.cells_used[6][1] == self.cells_used[9][1] != None:
            game_Over(self,self.cells_used[3][1]+" Won!")
        elif self.cells_used[1][1] == self.cells_used[5][1] == self.cells_used[9][1] != None:
            game_Over(self,self.cells_used[1][1]+" Won!")
        elif self.cells_used[3][1] == self.cells_used[5][1] == self.cells_used[7][1] != None:
            game_Over(self,self.cells_used[3][1]+" Won!")

        if self.cells_used_no == 9:
            game_Over(self,'Draw!')

    def draw(self,winner=None):
        self.window.fill(WHITE)
        if self.computer_mode_enabled:
            self.window.blit(pygame.font.Font('freesansbold.ttf', 30).render('###### Computer Mode #######',True,BLACK), (100,10))
        else:
            self.window.blit(pygame.font.Font('freesansbold.ttf', 30).render('###### 2Player Mode #######',True,BLACK), (100,10))
        if self.gameOver == True:
            heading = pygame.font.Font('freesansbold.ttf', 50).render(winner,True,RED)
            self.window.blit(heading, (100,50))
        else:
            heading = pygame.font.Font('freesansbold.ttf', 50).render('Tick Tak Toe',True,RED)
            self.window.blit(heading, (100,50))

        self.drawGrid(self.window)
        self.drawSelection(self.window,self.cells_used[self.selected][3])
        for block in self.cells_used:
            if self.cells_used[block][0] == True:
                self.drawXO(self.window,self.cells_used[block][3],self.cells_used[block][1],self.cells_used[block][2])
        pygame.display.update()

    def drawSelection(self,window,position):
        pygame.draw.rect(window, RED, (gridPos[0]+position[0]*cellSize, gridPos[1]+position[1]*cellSize, cellSize, cellSize))
        pygame.draw.rect(window, WHITE, (gridPos[0]+position[0]*cellSize+10, gridPos[1]+position[1]*cellSize+10, cellSize-20, cellSize-20))

    def drawXO(self,window,position,letter,color):
        font = pygame.font.Font('freesansbold.ttf', 100)
        text = font.render(letter,True,color)
        window.blit(text, (gridPos[0]+position[0]*cellSize+38,gridPos[1]+position[1]*cellSize+38))


    def drawGrid(self,window):
        pygame.draw.rect(window,BLACK, (gridPos[0], gridPos[1], WIDTH-150, HEIGHT-150), 6)

        for x in range(1,3):
            pygame.draw.line(window, BLACK, (gridPos[0]+(x*cellSize), gridPos[1]), (gridPos[0]+(x*cellSize), gridPos[1]+gridSize),3)
            pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1]+(x*cellSize)), (gridPos[0]+gridSize, gridPos[1]+(x*cellSize)) ,3)

    def mouseOnGrid(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        if self.mousePos[0] >gridPos[0]+gridSize or self.mousePos[1] > gridPos[1]+gridSize:
            return False
        x = (self.mousePos[0]-gridPos[0])//cellSize
        y = (self.mousePos[1]-gridPos[1])//cellSize
        return x+3*y+1

def game_Over(app,winner):
    app.gameOver = True
    app.draw(winner)
    time.sleep(1.5)
    mode = app.computer_mode_enabled
    app = App()
    app.computer_mode_enabled = mode
    app.run()

def main():
    def two_player():
        global app
        root.destroy()
        app = App()
        app.run()
    def computer():
        global app
        root.destroy()
        app = App()
        app.computer_mode_enabled = True
        app.run()
    global root
    root = tk.Tk()
    root.geometry('600x400')
    root.config(bg='cadet blue')
    tk.Button(root,text="2p MODE ",width=20,height=2,font=("Ariel",17),bg='powder blue',command = two_player).place(x=170,y=60)
    pc = tk.Button(root,text="Vs Computer",width=20,height=2,font=("Ariel",17),bg='powder blue',command = computer)
    pc.place(x=170,y=160)
    pc.focus()
    root.mainloop()


if __name__=="__main__":
    main()
