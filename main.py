from cmu_112_graphics import *
import cave
import player
import treasure
import enemy
import mole
import random
import time
#################################################
# Start Mode
#################################################

# Draw start screen
def startMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "#765745", 
                            width = 0)
    canvas.create_image(app.width//2, app.height//8 + 50, 
                        image = ImageTk.PhotoImage(app.logo))
    canvas.create_rectangle(app.width//4, 2*app.height//5, 3*app.width//4,
                            2*app.height//5 + 100, width = 5, outline = "white")
    canvas.create_text(app.width//2, 2*app.height//5 + 50, anchor = "center",
                        text = "Play", fill = "white", font = "System 32 bold")
    canvas.create_rectangle(app.width//4, 3*app.height//5, 3*app.width//4,
                            3*app.height//5 + 100, width = 5, outline = "white")
    canvas.create_text(app.width//2, 3*app.height//5 + 50, anchor = "center",
                        text = "How to Play", fill = "white",
                        font = "System 32 bold")

# Change modes based on which button is clicked
def startMode_mousePressed(app, event):
    buttonPressed = startMode_getButtonPressed(app, event.x, event.y)
    if buttonPressed == "Play":
        app.timer = time.time()
        app.mode = "gameplayMode"
    elif buttonPressed == "How to Play":
        app.mode = "howToPlayMode"

# Return string representing which button the player clicks
# If no button is clicked, return an empty string
def startMode_getButtonPressed(app, x, y):
    if (x < app.width//4 or x > 3*app.width//4 or y < 2*app.height//5 or
        2*app.height//5 + 100 < y < 3*app.height//5 or y > 3*app.height//5 + 100):
        return ""
    elif 2*app.height//5 <= y <= 2*app.height//5 + 100: return "Play"
    else: return "How to Play"

#################################################
# How to Play Mode
#################################################

# Draw how to play screen
def howToPlayMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, 
                            fill = "tan4", 
                            width = 0)
    canvas.create_text(app.width//2, 30, anchor = "center", 
                        text = "How to Play",
                        font = "System 48 bold", fill = "maroon")
    canvas.create_text(10, app.height/16, anchor = "nw", text = "Controls",
                        font = "System 32 bold underline")
    canvas.create_text(10, app.height/16 + 50, anchor = "nw", text = 
                        ("Use the WASD keys to move through the"
                        " cave.\n\n"
                        "Click on a tile within the miner's throwing radius"
                        " to throw a mole\n"
                        "at that tile.\n\n"
                        "Press the F key to call moles back.\n\n"
                        "Press the M key to view the"
                        " map.\n\n"
                        "Press the P key to pause the game.")
                        , font = "System 16")
    canvas.create_text(10, app.height/2, anchor = "nw", text = "Objective",
                        font = "System 32 bold underline")
    canvas.create_text(10, app.height/2 + 50, anchor = "nw", text =
                        "Move through the cave to find the scattered "
                        "treasure.\n\n"
                        "Attack enemies by throwing your moles at them, but"
                        " make sure to keep\n"
                        "your moles out of the way of their attacks or they'll"
                        " die. If they all die, it's game over.\n\n"
                        "When you defeat an enemy, throw your moles at it"
                        " to have them carry it to\n"
                        "your base to make more moles.\n\n"
                        "Throw your moles at treasure to have them carry it"
                        " back to your base.\nCollect all the treasure to beat"
                        " the game. Try going for a best time."
                        , font = "System 16")
    canvas.create_text(app.width/2, 15*app.height/16, anchor = "center",
                        text = "Press any key to return to the menu.",
                        font = "System 32 bold")

def howToPlayMode_keyPressed(app, event):
    app.mode = "startMode"

#################################################
# Gameplay Mode
#################################################

def gameplayMode_timerFired(app):

    # Check if the player has reached a win or lose condition
    # Player wins if all treasure is collected
    if len(app.worldTreasure) == 0:
        app.win = True
        app.timer = time.time() - app.timer
        app.mode = "gameOverMode"
    else:
        # Player loses if all moles are dead or they can't make enough moles
        # to carry the largest treasure on the map
        treasureMoleLen = 0
        for t in app.worldTreasure:
            treasureMoleLen += len(t.treasureMoles)
        enemyMoleLen = 0
        for e in app.worldEnemies:
            enemyMoleLen += len(e.enemyMoles)
        if (len(app.player.playerMoles) + len(app.worldMoles) +
            treasureMoleLen + enemyMoleLen == 0):
            app.lose = True
            app.loseCondition = 0
            app.mode = "gameOverMode"
        else:
            maxWeight = 0
            for t in app.worldTreasure:
                if t.molesNeeded > maxWeight:
                    maxWeight = t.molesNeeded
            
            if (len(app.player.playerMoles) + len(app.worldMoles) +
                treasureMoleLen + len(app.worldEnemies)*5 < maxWeight):
                app.lose = True
                app.loseCondition = 1
                app.mode = "gameOverMode"

    # Manage enemy movements and behaviors
    for e in app.worldEnemies:
        # Check if any moles are in the enemy's view if they are idle
        if e.behavior == 0:
            for m in app.player.playerMoles:           
                for i in range(0, 4):
                    for drow, dcol in [(-1, -1), (-1, 0), (-1, 1), (0, 1), 
                                            (1, 1), (1, 0), (1, -1), (0, -1)]:
                        if (0 <= e.yPos + drow*i < len(app.cave.cave) and
                            0 <= e.xPos + dcol*i < len(app.cave.cave[0])):
                            if (m.xPos, m.yPos) == (e.xPos + dcol*i, e.yPos + drow*i):
                                e.behavior = 1
                                e.path = gameplayMode_bfsPath(app, e, (m.xPos, m.yPos))
            for m in app.worldMoles:
                for i in range(1, 4):
                    for drow, dcol in [(-1, -1), (-1, 0), (-1, 1), (0, 1), 
                                            (1, 1), (1, 0), (1, -1), (0, -1)]:
                        if (0 <= e.yPos + drow*i < len(app.cave.cave) and
                            0 <= e.xPos + dcol*i < len(app.cave.cave[0])):
                            if (m.xPos, m.yPos) == (e.xPos + dcol*i, e.yPos + drow*i):
                                e.behavior = 1
                                e.path = gameplayMode_bfsPath(app, e, (m.xPos, m.yPos))
        # Have the enemy die if they reach 0 health
        if e.behavior < 3 and e.health <= 0:
            e.behavior = 3
            e.attackWarning = False
        # Have the dead mole be carried to base if enough moles are carrying it
        if e.behavior == 3 and len(e.enemyMoles) >= e.molesNeeded:
            e.behavior = 4
            e.path = gameplayMode_bfsPath(app, e, app.landSite)
        # Stop dead enemy from moving if not enough moles are carrying it
        elif e.behavior == 4 and len(e.enemyMoles) < e.molesNeeded:
            e.path = []
            e.behavior = 3
        # Move enemy
        e.move(app)
        # Engage in attack sequence 
        # if an attacking enemy reaches its destination
        if e.behavior == 2:
            e.attack(app)

    # Move each mole in some direction based on behavior
    for m in app.player.playerMoles:
        m.move(app)
    for m in app.worldMoles:
        m.move(app)
        for e in app.worldEnemies:
            if (m.yPos, m.xPos) == (e.yPos, e.xPos):
                # Attack enemy if touching it and return mole to player
                if e.behavior < 3: 
                    e.health -= 1
                    m.behavior = 0
                    app.player.playerMoles.append(m)
                    app.worldMoles.remove(m)
                # Carry enemy if the enemy is dead
                elif e.behavior == 3:
                    e.enemyMoles.append(m)
                    app.worldMoles.remove(m)
        # Carry treasure if touching it
        if (m.xPos, m.yPos) in app.worldTreasurePositions:
            for t in app.worldTreasure:
                if (t.xPos, t.yPos) == (m.xPos, m.yPos):
                    m.behavior = 3
                    t.treasureMoles.append(m)
                    app.worldMoles.remove(m)

    newWorldTreasure = []
    for t in app.worldTreasure:
        # Have treasure be carried if enough moles are carrying it
        if t.behavior == 0 and len(t.treasureMoles) >= t.molesNeeded:
            t.behavior = 1
            t.path = gameplayMode_bfsPath(app, t, app.landSite)
            newWorldTreasure.append(t)
        elif t.behavior == 1:
            # Stop treasure from moving
            # if there are not enough moles carrying it
            if len(t.treasureMoles) < t.molesNeeded:
                t.behavior = 0
                t.path = []
                newWorldTreasure.append(t)
            else:
                t.move()
                # Remove treasure from world if it has reached the landsite
                if (t.xPos, t.yPos) == app.landSite:
                    for m in t.treasureMoles:
                        m.xPos, m.yPos = t.xPos, t.yPos
                        m.behavior = 2
                        app.worldMoles.append(m)
                else: newWorldTreasure.append(t)
        else: newWorldTreasure.append(t)
    app.worldTreasure = copy.copy(newWorldTreasure)

def gameplayMode_mousePressed(app, event):
    # Throw mole if destination in player's throwing radius
    if distFromCenter(app, event.x, event.y) <= app.player.throwRadius*50:
        app.player.throw(event.x, event.y, app)

def gameplayMode_keyPressed(app, event):
    # Toggle shortcuts on and off
    if event.key == "0":
        app.shortCuts = not app.shortCuts
    # Shortcut keys for demonstrating features
    if app.shortCuts:
        # Remove all enemies and pre-existing treasure
        # Make one treasure in player's position
        # Demonstrates carrying treasure and winning condition
        if event.key == "1":
            app.worldEnemies = []
            app.worldTreasure = [treasure.Treasure()]
            (app.worldTreasure[0].xPos, app.worldTreasure[0].yPos) = (app.player.xPos, app.player.yPos)
            app.worldTreasurePositions = [(t.xPos, t.yPos) for t in app.worldTreasure]
            app.worldTreasure[0].molesNeeded = 1
        # Move enemy to player's position
        # Demonstrates attacking enemies, carrying enemies, making moles
        # and lose condition 0 (all moles dead)
        elif event.key == "2":
            if app.worldEnemies == []:
                app.worldEnemies.append(enemy.Enemy())
            (app.worldEnemies[0].xPos, app.worldEnemies[0].yPos) = (app.player.xPos, app.player.yPos)
        # Change a treasures "weight" (molesNeeded) to an impossible weight
        # (not found in normal gameplay)
        # Demonstrates lose condition 1 (not enough moles to beat the game)
        elif event.key == "3":
            app.worldTreasure[0].molesNeeded = 1000

    # Change modes if a certain key is pressed
    if event.key == 'm':
        app.mode = "mapMode"
    elif event.key == 'p':
        app.mode = "pauseMode"
    # move player
    elif event.key in {'w', 'a', 's', 'd'}:
        app.player.move(event.key, app)
    # call moles not in player's mole list if they are within player's throw radius
    elif event.key == 'f':
        newWorldMoles = []
        for m in app.worldMoles:
            if (distFromCenter(app, app.width//2 + (m.xPos - app.player.xPos)*20, app.height//2 + (m.yPos - app.player.yPos)*20) <= app.player.throwRadius*50):
                m.behavior = 0
                app.player.playerMoles.append(m)
            else:
                newWorldMoles.append(m)
        app.worldMoles = copy.copy(newWorldMoles)
        for t in app.worldTreasure:
            if (distFromCenter(app, app.width//2 + (t.xPos - app.player.xPos)*20, app.height//2 + (t.yPos - app.player.yPos)*20) <= app.player.throwRadius*50):
                for m in t.treasureMoles:
                    m.behavior = 0
                    app.player.playerMoles.append(m)
                    t.treasureMoles.remove(m)
        for e in app.worldEnemies:
            if (distFromCenter(app, app.width//2 + (e.xPos - app.player.xPos)*20, app.height//2 + (e.yPos - app.player.yPos)*20) <= app.player.throwRadius*50):
                for m in e.enemyMoles:
                    m.behavior = 0
                    app.player.playerMoles.append(m)
                    e.enemyMoles.remove(m)

# Return list of tuples representing nodes on the cave's node map an object
# must travel through to reach a destination (through BFS pathfinding)
def gameplayMode_bfsPath(app, obj, destination):
    Q = [(obj.yPos, obj.xPos)]
    V = {(obj.yPos, obj.xPos)}
    P = {}
    while Q != []:
        currentNode = Q[0]
        if currentNode == (destination[1], destination[0]):
            finalPath = [currentNode]
            while currentNode != (obj.yPos, obj.xPos):
                finalPath.append(P[currentNode])
                currentNode = P[currentNode]
            return finalPath[::-1]
        for neighbor in app.cave.nodeMap[currentNode]:
            if neighbor not in V:
                V.add(neighbor)
                Q.append(neighbor)
            if neighbor not in P:
                P[neighbor] = currentNode
        Q.pop(0)
    return [(obj.yPos, obj.xPos)]

# Redraw game
def gameplayMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height,
                            fill = app.stoneColor, width = 0)
    app.cave.drawCave(app, canvas)

    # draw landsite
    if (app.landSite[0] in range(app.player.xPos - 20, app.player.xPos + 20)
        and app.landSite[1] in
        range(app.player.yPos - 20, app.player.yPos + 20)):
                    xPos = (app.width//2 +
                    (app.landSite[0] - app.player.xPos)*20)
                    yPos = (app.height//2 +
                    (app.landSite[1] - app.player.yPos)*20)
                    canvas.create_image(xPos, yPos,
                                        image = ImageTk.PhotoImage(app.landSiteSprite))
                    canvas.create_oval(xPos - 15, yPos - 15,
                                        xPos + 15, yPos + 15,
                                        outline = "white")

    # draw moles
    for m in app.player.playerMoles:
        m.drawMole(app, canvas)
    for m in app.worldMoles:
        m.drawMole(app, canvas)

    # draw enemies
    for e in app.worldEnemies:
        e.drawEnemy(app, canvas)

    # draw treasure
    for t in app.worldTreasure:
        t.drawTreasure(app, canvas)
    
    # draw player
    app.player.drawPlayer(app, canvas)

    # UI updates
    treasureMoleLen = 0
    for t in app.worldTreasure:
        treasureMoleLen += len(t.treasureMoles)
    enemyMoleLen = 0
    for e in app.worldEnemies:
        enemyMoleLen += len(e.enemyMoles)
    canvas.create_rectangle(0, 0, 250, 100, fill = app.stoneColor, width = 0)
    canvas.create_text(0, 0, anchor = "nw",
                        text = f'{len(app.player.playerMoles)}/{len(app.player.playerMoles) + len(app.worldMoles) + treasureMoleLen + enemyMoleLen} Moles',
                        fill = "white", font = 'System 20 bold')
    canvas.create_text(0, 50, anchor = "nw",
                        text = f'Treasure Left: {len(app.worldTreasure)}',
                        fill = "white", font = 'System 20 bold')

#################################################
# Map Mode
#################################################

# Return to game
def mapMode_keyPressed(app, event):
    app.mode = "gameplayMode"

# Draw the game from the map view
def mapMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "tan4",
                            width = 0)

    app.cave.drawCave(app, canvas)
    app.player.drawPlayer(app, canvas)

    # draw landsite in map mode
    canvas.create_oval(app.landSite[0]*8, app.landSite[1]*8,
                        (app.landSite[0]+1)*8, (app.landSite[1]+1)*8,
                        fill = "cyan", width = 0)

    # draw moles
    for m in app.player.playerMoles:
        m.drawMole(app, canvas)
    for m in app.worldMoles:
        m.drawMole(app, canvas)

    # draw treasure
    for t in app.worldTreasure:
        t.drawTreasure(app, canvas)

    # UI
    treasureMoleLen = 0
    for t in app.worldTreasure:
        treasureMoleLen += len(t.treasureMoles)
    enemyMoleLen = 0
    for e in app.worldEnemies:
        enemyMoleLen += len(e.enemyMoles)
    canvas.create_text(0, 0, anchor = "nw",
                        text = f'{len(app.player.playerMoles)}/{len(app.player.playerMoles) + len(app.worldMoles) + treasureMoleLen + enemyMoleLen} Moles',
                        fill = "white", font = 'System 20 bold')
    canvas.create_text(0, 50, anchor = "nw",
                        text = f'Treasure Left: {len(app.worldTreasure)}',
                        fill = "white", font = 'System 20 bold')

#################################################
# Pause Mode
#################################################

# Draw pause screen
def pauseMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height,
                            fill = "light gray", width = 0)
    canvas.create_text(app.width//2, app.height//8, anchor = "center",
                        text = "Paused", 
                        font = "System 48 bold")
    canvas.create_rectangle(app.width//4, 2*app.height//5, 3*app.width//4,
                            2*app.height//5 + 100, width = 5)
    canvas.create_text(app.width//2, 2*app.height//5 + 50, anchor = "center",
                        text = "Continue", font = "System 32 bold")
    canvas.create_rectangle(app.width//4, 3*app.height//5, 3*app.width//4,
                            3*app.height//5 + 100, width = 5)
    canvas.create_text(app.width//2, 3*app.height//5 + 50, anchor = "center",
                        text = "Quit", font = "System 32 bold")

# Change modes if a button on the pause screen is pressed
def pauseMode_mousePressed(app, event):
    buttonPressed = pauseMode_getButtonPressed(app, event.x, event.y)
    if buttonPressed == "Continue":
        app.mode = "gameplayMode"
    elif buttonPressed == "Quit":
        appStarted(app)

# Return string representing which button the player clicks
# If no button is clicked, return an empty string
def pauseMode_getButtonPressed(app, x, y):
    if (x < app.width//4 or x > 3*app.width//4 or y < 2*app.height//5 or
        2*app.height//5 + 100 < y < 3*app.height//5 or y > 3*app.height//5 + 100):
        return ""
    elif 2*app.height//5 <= y <= 2*app.height//5 + 100: return "Continue"
    else: return "Quit"

#################################################
# Game Over Mode
#################################################

# Draw game over screen
def gameOverMode_redrawAll(app, canvas):
    if app.win:
        color = "light goldenrod"
        minutes = int(app.timer//60)
        seconds = int(app.timer%60)
        message = f"Congratulations! You won!\n You beat the game in {minutes}:{seconds//10}{seconds%10}"
    elif app.lose:
        color = "white"
        if app.loseCondition == 0:
            message = "All your moles died... Game over"
        elif app.loseCondition == 1:
            message = "You don't have enough moles\nto collect all the treasure... Game over"
    canvas.create_rectangle(0, 0, app.width, app.height, fill = color, width = 0)
    canvas.create_text(app.width//2, 350, anchor = "center", text = f'{message}'
                        '\nPress any key to return to the menu.',
                        font = 'System 32 bold')

# Return to start screen
def gameOverMode_keyPressed(app, event):
    appStarted(app)

#################################################
# Main App
#################################################

def appStarted(app):
    app.mode = "startMode"

    # Gameplay Mode Properties

    #app cave properties
    app.rows = app.cols = 100
    app.mapComplexity = 4
    app.cave = cave.Cave(app.rows, app.cols, app.mapComplexity)
    app.airColor = "#574a41"
    app.stoneColor = "#2c2825"

    #app player properties
    xPos, yPos = randomSpawn(app)
    app.player = player.Player(xPos, yPos)

    #moles
    for m in app.player.playerMoles:
        (m.xPos, m.yPos) = (app.player.xPos, app.player.yPos)
    app.worldMoles = []

    #treasure
    app.worldTreasure = [treasure.Treasure() for _ in range(20)]
    for t in app.worldTreasure:
        (t.xPos, t.yPos) = randomSpawn(app)
    app.worldTreasurePositions = [(t.xPos, t.yPos) for t in app.worldTreasure]
    
    #enemies
    app.worldEnemies = [enemy.Enemy() for _ in range(10)]
    for e in app.worldEnemies:
        (e.xPos, e.yPos) = randomSpawn(app)

    #images
    initImages(app)

    #misc
    app.timerDelay = 50
    app.landSite = (app.player.xPos, app.player.yPos)
    app.win = False
    app.lose = False
    app.loseCondition = None
    '''About lose conditions:
        None - The player hasn't lost yet
        0 - All moles have died
        1 - The player can't make enough moles to carry the largest treasure
        on the map'''
    app.timer = 0
    app._root.resizable(False, False)
    app.shortCuts = False

def initImages(app):

    # Player sprites
    playerSpriteSheet = "assets/playerSpriteSheet.png"
    app.playerSpriteSheet = app.loadImage(playerSpriteSheet)
    app.playerSpriteSheet = app.scaleImage(app.playerSpriteSheet, 1.5)
    app.playerSpriteHeight, app.playerSpriteWidth = app.playerSpriteSheet.size
    app.playerSprites = {}
    for direction in ["Up0", "Right1", "Down2", "Left3"]:
        index = int(direction[-1:])
        newDir = direction[:-1]
        topLeftY = index * app.playerSpriteHeight / 4
        botRightY = (index+1) * app.playerSpriteHeight / 4
        tempSprites = []
        for j in range(4):
            topLeftX = j * app.playerSpriteWidth / 4
            botRightX = (j + 1) * app.playerSpriteWidth / 4
            sprite = app.playerSpriteSheet.crop((topLeftX, topLeftY, botRightX, botRightY))
            tempSprites.append(sprite)
        app.playerSprites[newDir] = copy.copy(tempSprites)

    # Mole sprites
    moleSpriteSheet = "assets/moleSpriteSheet.png"
    app.moleSpriteSheet = app.loadImage(moleSpriteSheet)
    app.moleSpriteHeight, app.moleSpriteWidth = app.moleSpriteSheet.size
    app.moleSprites = {}
    for direction in ["Down0", "Right1", "Left2", "Up3"]:
        index = int(direction[-1:])
        newDir = direction[:-1]
        topLeftY = index * app.moleSpriteHeight / 4
        botRightY = (index+1) * app.moleSpriteHeight / 4
        tempSprites = []
        for j in range(4):
            topLeftX = j * app.moleSpriteWidth / 4
            botRightX = (j + 1) * app.moleSpriteWidth / 4
            sprite = app.moleSpriteSheet.crop((topLeftX, topLeftY, botRightX, botRightY))
            tempSprites.append(sprite)
        app.moleSprites[newDir] = copy.copy(tempSprites)

    # Treasure sprite
    app.treasureSprite = app.loadImage("assets/treasureSprite.png")

    # Enemy sprites
    enemySpriteSheet = "assets/enemySpriteSheet.png"
    app.enemySpriteSheet = app.loadImage(enemySpriteSheet)
    app.enemySprites = {}
    for behavior in ["Idle0", "Attack1", "Dead2"]:
        index = int(behavior[-1:])
        newBehavior = behavior[:-1]
        sprite = app.enemySpriteSheet.crop((index*20, 0,
                                            (index + 1)*20,
                                            20))
        app.enemySprites[newBehavior] = sprite
    app.attackWarningSprite = app.loadImage("assets/attackWarningSprite.png")

    # Land site sprite
    app.landSiteSprite = app.loadImage("assets/landSiteSprite.png")

    app.logo = app.loadImage("assets/logo.png")

# return x and y coordinates on cave map not occupied by a "0" on the
# generated cave
def randomSpawn(app):
    x, y = random.randint(0, app.cols-1), random.randint(0, app.rows-1)
    while app.cave.cave[y][x] != 1:
        x, y = random.randint(0, app.cols-1), random.randint(0, app.rows-1)
    return (x, y)

# return distance of mouse when clicked from player position in zoomed-in mode (always center of the canvas)
def distFromCenter(app, x, y):
    return int(((x - app.width//2)**2 + (y-app.height//2)**2)**(1/2))

def play():
    runApp(width = 800, height = 800)
play()