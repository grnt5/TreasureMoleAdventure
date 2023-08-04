from cmu_112_graphics import *
class Mole(object):
    def __init__(self):
        self.xPos = self.yPos = 50
        self.pos = (self.xPos, self.yPos)
        self.behavior = 0
        '''behaviors
            0 - follow player
            1 - follow throwing path
            2 - do nothing
            3 - carrying'''
        self.path = []
        self.direction = "Down"
        self.step = 0

    def move(self, app):
        # Only move if not idle
        if self.behavior != 2:
            if self.behavior == 0: destination = (app.player.xPos, app.player.yPos)
            elif self.behavior == 1: destination = self.path
            if len(destination) > 0:
                dy = 0
                dx = 0
                if self.xPos < destination[0]:
                    dx += 1
                    if self.direction == "Right":
                        self.step += 1
                    else:
                        self.direction = "Right"
                        self.step = 0
                elif self.xPos > destination[0]:
                    dx -= 1
                    if self.direction == "Left":
                        self.step += 1
                    else:
                        self.direction = "Left"
                        self.step = 0
                newX = self.xPos + dx
                if self.inBounds(app, newX, self.yPos, destination):
                    self.xPos = newX
                # stop moving if moving into a wall
                elif self.behavior == 1: 
                    self.path = ()
                    self.behavior = 2
                if self.yPos < destination[1]:
                    dy += 1
                    if self.direction == "Down":
                        self.step += 1
                    else:
                        self.direction = "Down"
                        self.step = 0
                elif self.yPos > destination[1]:
                    dy -= 1
                    if self.direction == "Up":
                        self.step += 1
                    else:
                        self.direction = "Up"
                        self.step = 0
                newY = self.yPos + dy
                if self.inBounds(app, self.xPos, newY, destination):
                    self.yPos = newY
                elif self.behavior == 1: 
                   self.path = ()
                   self.behavior = 2
                if self.behavior == 1:
                    #Stop moving if destination reached
                    if (self.xPos, self.yPos) == self.path:
                        self.path = ()
                        self.behavior = 2

    # Return True if the mole is not colliding with a wall or another mole
    # Return False otherwise
    def inBounds(self, app, x, y, destination):
        if self.behavior == 0:
            if not ((app.cave.cave[y][x] == 0 or 
            (x == destination[0] and y == destination[1]) or 
            (x, y) in app.player.getPlayerMolePositions())):
                return True
        elif self.behavior == 1:
            return not app.cave.cave[y][x] == 0
        return False

    def drawMole(self, app, canvas):
        sprite = app.moleSprites[self.direction][self.step%4]
        if app.mode == "gameplayMode":
            if (self.xPos in range(app.player.xPos - 20, app.player.xPos + 20)
                and self.yPos in range(app.player.yPos - 20, app.player.yPos + 20)):
                xPos = app.width//2 + (self.xPos - app.player.xPos)*20
                yPos = app.height//2 + (self.yPos - app.player.yPos)*20
                
                # Indicator if being idle
                if self.behavior == 2:
                    canvas.create_oval(xPos - 7, yPos - 7, xPos + 7, yPos + 7,
                                        fill = "magenta", width = 0)
                canvas.create_image(xPos, yPos-10,
                                    image = ImageTk.PhotoImage(sprite))
        elif app.mode == "mapMode":
            canvas.create_oval(self.xPos*8 + 2, self.yPos*8 + 2,
                                (self.xPos+1)*8 - 2, (self.yPos+1)*8 - 2,
                                fill = "navyBlue", width = 0)