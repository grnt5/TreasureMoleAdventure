import random
from cmu_112_graphics import *
class Treasure(object):
    def __init__(self):
        self.xPos = self.yPos = 0
        self.molesNeeded = random.randint(1, 30)
        self.treasureMoles = []
        self.behavior = 0
        self.path = []
        '''behavior traits
            0 - idle, do nothing
            1 - being carried, move along path formed by bfs'''
    def drawTreasure(self, app, canvas):
        if app.mode == "gameplayMode":
            if self.xPos in range(app.player.xPos - 20, app.player.xPos + 20) and self.yPos in range(app.player.yPos - 20, app.player.yPos + 20):
                xPos = app.width//2 + (self.xPos - app.player.xPos)*20
                yPos = app.height//2 + (self.yPos - app.player.yPos)*20
                canvas.create_image(xPos, yPos,
                                    image = ImageTk.PhotoImage(app.treasureSprite))
                canvas.create_text(xPos - 10, yPos - 20, anchor = "nw",
                                    text = f'{len(self.treasureMoles)}/{self.molesNeeded}',
                                    font = "System 9 bold", fill = "white")
        elif app.mode == "mapMode":
            canvas.create_oval(self.xPos*8, self.yPos*8, (self.xPos+1)*8, (self.yPos+1)*8, fill = "yellow", width = 0)
    def move(self):
        if self.behavior == 1:
            if self.path == [] or (len(self.path) == 1 and
            self.path[0] == (self.yPos, self.xPos)):
                self.behavior = 0
            else:
                (self.yPos, self.xPos) = (self.path[1])
                self.path.pop(0)