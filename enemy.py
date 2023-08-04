import mole
from cmu_112_graphics import *
class Enemy(object):
    def __init__(self):
        self.xPos = self.yPos = 0
        self.behavior = 0
        
        '''Behaviors
        0 - idle, do nothing
        1 - mole/player spotted, move towards mole/player
        2 - attacking
        3 - dead, carryable object
        4 - being carried'''
        
        self.health = 10
        self.attackCharge = 0
        self.enemyMoles = []
        self.molesNeeded = 1
        self.attackWarning = False
        self.path = []

    # Engage in attack sequence
    def attack(self, app):
        if self.attackCharge >= 500:
            self.attackWarning = True
        if self.attackCharge >= 1000:
            # Kill all moles in enemy's attack range
            for m in app.player.playerMoles:
                for drow, dcol in [(-1, -1), (-1, 0), (-1, 1), (0, 1), 
                                        (1, 1), (1, 0), (1, -1), (0, -1), (0, 0)]:
                    if (0 <= self.yPos + drow < len(app.cave.cave) and
                        0 <= self.xPos + dcol < len(app.cave.cave[0])):
                        if (m.xPos, m.yPos) == (self.xPos + dcol, self.yPos + drow):
                            app.player.playerMoles.remove(m)
                            break
            for m in app.worldMoles:
                for drow, dcol in [(-1, -1), (-1, 0), (-1, 1), (0, 1), 
                                        (1, 1), (1, 0), (1, -1), (0, -1), (0, 0)]:
                    if (0 <= self.yPos + drow < len(app.cave.cave) and
                        0 <= self.xPos + dcol < len(app.cave.cave[0])):
                        if (m.xPos, m.yPos) == (self.xPos + dcol, self.yPos + drow):
                            app.worldMoles.remove(m)
                            break
            self.attackCharge = 0
            self.behavior = 0
            self.attackWarning = False
        self.attackCharge += app.timerDelay

    def move(self, app):
        if self.behavior == 1:
            if self.path == []:
                self.behavior = 2
            else:
                (self.yPos, self.xPos) = (self.path[0])
                self.path.pop(0)
        elif self.behavior == 4:
            # Make new moles at landing site when dead enemy reaches it
            if (self.xPos, self.yPos) == app.landSite:
                newMoles = []
                for _ in range(5 + len(self.enemyMoles)):
                    newMoles.append(mole.Mole())
                for m in newMoles:
                    m.xPos, m.yPos = app.landSite
                    m.behavior = 2
                    app.worldMoles.append(m)
                app.worldEnemies.remove(self)
            else:
                (self.yPos, self.xPos) = (self.path[0])
                self.path.pop(0)

    def drawEnemy(self, app, canvas):
        if self.behavior < 3:
            color = "purple"
            text = f'{self.health}'
            if self.behavior == 0:
                sprite = app.enemySprites["Idle"]
            else: sprite = app.enemySprites["Attack"]
        else:
            color = "black"
            sprite = app.enemySprites["Dead"]
            text = f'{len(self.enemyMoles)}/{self.molesNeeded}'
        
        if app.mode == "gameplayMode":
            if (self.xPos in range(app.player.xPos - 20, app.player.xPos + 20)
                and self.yPos in range(app.player.yPos - 20, app.player.yPos + 20)):
                xPos = app.width//2 + (self.xPos - app.player.xPos)*20
                yPos = app.height//2 + (self.yPos - app.player.yPos)*20
                if self.attackWarning == True:
                    canvas.create_image(xPos, yPos,
                                        image = ImageTk.PhotoImage(app.attackWarningSprite))
                canvas.create_image(xPos, yPos,
                                    image = ImageTk.PhotoImage(sprite))
                canvas.create_text(xPos - 10, yPos - 20, anchor = "nw",
                                    text = text, font = "System 9 bold",
                                    fill = "red")
        elif app.mode == "mapMode":
            canvas.create_oval(self.xPos*8, self.yPos*8, (self.xPos+1)*8,
                                (self.yPos+1)*8, fill = color, width = 0)
