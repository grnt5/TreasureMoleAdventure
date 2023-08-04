import mole
import math
from cmu_112_graphics import*
class Player(object):
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.movement = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.playerMoles = [mole.Mole() for i in range(10)]
        self.throwRadius = 3
        self.direction = "Down"
        self.step = 0

    # Return list of tuples corresponding to x and y positions of moles
    # following the player
    def getPlayerMolePositions(self):
        return [(m.xPos, m.yPos) for m in self.playerMoles]

    def move(self, key, app):
        dy = dx = 0
        if key == "w":
            if self.direction == "Up":
                self.step += 1
            else:
                self.direction = "Up"
                self.step = 0
            dy, dx = self.movement[0]
        elif key == "d":
            if self.direction == "Right":
                self.step += 1
            else:
                self.direction = "Right"
                self.step = 0
            dy, dx = self.movement[1]
        elif key == "s":
            if self.direction == "Down":
                self.step += 1
            else:
                self.direction = "Down"
                self.step = 0
            dy, dx = self.movement[2]
        elif key == "a":
            if self.direction == "Left":
                self.step += 1
            else:
                self.direction = "Left"
                self.step = 0
            dy, dx = self.movement[3]
        self.xPos += dx
        self.yPos += dy
        # return player back to original position if collision detected
        if not ((0 <= self.yPos < app.rows) and (0 <= self.xPos < app.cols)
                and app.cave.cave[self.yPos][self.xPos] == 1):
            self.xPos -= dx
            self.yPos -= dy

    # Throw mole closest to the player
    def throw(self, x, y, app):
        if self.playerMoles != []:
            newX = self.xPos + (x + 10 - app.width//2)//20
            newY = self.yPos + (y + 10 - app.height//2)//20
            closestMole = None
            closestMoleDist = math.inf
            for m in self.playerMoles:
                dist = ((self.xPos - m.xPos)**2 + (self.yPos - m.yPos)**2)**1/2
                if dist < closestMoleDist:
                    closestMole = m
                    closestMoleDist = dist
            closestMole.behavior = 1
            closestMole.path = (newX, newY)
            app.worldMoles.append(closestMole)
            self.playerMoles.remove(closestMole)

    def drawPlayer(self, app, canvas):
        if app.mode == "gameplayMode":
            xPos = app.width//2 
            yPos = app.height//2
            sprite = app.playerSprites[self.direction][self.step%4]
            canvas.create_image(xPos, yPos-10,
                                image = ImageTk.PhotoImage(sprite))
            canvas.create_oval(xPos - 50*self.throwRadius,
                                yPos - 50*self.throwRadius,
                                xPos + 50*self.throwRadius,
                                yPos + 50*self.throwRadius,
                                outline = "white")
        elif app.mode == "mapMode":
            canvas.create_rectangle(self.xPos*8, self.yPos*8, (self.xPos+1)*8,
                                    (self.yPos+1)*8, fill = "red", width = 0)