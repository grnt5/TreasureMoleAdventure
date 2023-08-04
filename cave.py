import copy
import random
class Cave(object):
    def __init__(self, rows, cols, complexity):
        self.rows = rows
        self.cols = cols
        self.complexity = complexity
        self.cave = self.generateCave(rows, cols, complexity)
        self.nodeMap = self.generateNodeMap(self.cave)

    # Return 2D list of generated cave through Prim's Algorithm and
    # Cell Automata with bordered edges
    def generateCave(self, rows, cols, complexity):
        cave = [[0]*cols for _ in range(rows)]
        startRow = random.randint(0, (rows-1)//2)*2 + 1
        startCol = random.randint(0, (cols-1)//2)*2 + 1
        cave[startRow][startCol] = 1
        wallsToCheck = []

        # Prim's algorithm
        for drow, dcol in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if 0 <= startRow + drow < rows and 0 <= startCol + dcol < cols:
                wallsToCheck.append((startRow + drow, startCol + dcol))
        while wallsToCheck != []:
            wall = wallsToCheck[random.randint(0, len(wallsToCheck) - 1)]
            wallCount = 0
            passageCount = 0
            for drow, dcol in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if 0 <= wall[0] + drow < rows and 0 <= wall[1] + dcol < cols:
                    if cave[wall[0] + drow][wall[1] + dcol] == 0:
                        wallCount += 1
                    else: passageCount += 1
            if passageCount == 1:
                cave[wall[0]][wall[1]] = 1
                for drow, dcol in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    if 0 <= wall[0] + drow < rows and 0 <= wall[1] + dcol < cols and cave[wall[0] + drow][wall[1] + dcol] == 0:
                        wallsToCheck.append((wall[0] + drow, wall[1] + dcol))
            wallsToCheck.remove(wall)
        for _ in range(2):
            for row in range(rows):
                for col in range(cols):
                    passageCount = 0
                    if cave[row][col] == 1:
                        for drow, dcol in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                            if (0 <= row + drow < rows and
                                0 <= col + dcol < cols and
                                (cave[row + drow][col + dcol] == 1 or
                                cave[row + drow][col + dcol] == 2)):
                                passageCount += 1
                        if passageCount == 1: cave[row][col] = 2
            for row in range(rows):
                for col in range(cols):
                    if cave[row][col] == 2: cave[row][col] = 0

        # Cell Automata
        for _ in range(complexity):
            copyCave = copy.deepcopy(cave)
            for row in range(rows):
                for col in range(cols):
                    neighborSum = 0
                    for drow, dcol in [(-1, -1), (-1, 0), (-1, 1), (0, 1), 
                                        (1, 1), (1, 0), (1, -1), (0, -1)]:
                        if 0 <= row + drow < rows and 0 <= col + dcol < cols:
                            neighborSum += cave[row+drow][col+dcol]
                    if cave[row][col] == 1:
                        if neighborSum >= 3: copyCave[row][col] = 1
                    else:
                        if neighborSum >= 5: copyCave[row][col] = 1
            cave = copy.deepcopy(copyCave)
        for col in range(cols):
            cave[0][col] = 0
            cave[rows - 1][col] = 0
        for row in range(rows):
            cave[row][0] = 0
            cave[row][cols - 1] = 0
        return cave

    # Return dictionary representing node graph corresponding to cave tiles
    def generateNodeMap(self, cave):
        rows = len(cave)
        cols = len(cave[0])
        nodeMap = {}
        for row in range(rows):
            for col in range(cols):
                if cave[row][col] == 1:
                    neighborSet = set()
                    for (dx, dy) in [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1),
                                    (-1, 1), (-1, 0), (-1, -1)]:
                        if (0 <= row+dy < len(cave) and 
                            0 <= col+dx < len(cave) and 
                            cave[row+dy][col+dx] == 1):
                            neighborSet.add((row+dy, col+dx))
                    nodeMap[(row, col)] = copy.copy(neighborSet)
        return nodeMap

    def drawCave(self, app, canvas):
        if app.mode == "gameplayMode":
            playerX, playerY = app.player.xPos, app.player.yPos
            for row in range(playerY - 20, playerY + 20):
                for col in range(playerX - 20, playerX + 20):
                    if 0 <= row < app.rows and 0 <= col < app.cols:
                        xPos = app.width//2 + (col - playerX)*20
                        yPos = app.height//2 + (row - playerY)*20
                        if self.cave[row][col] == 1:
                            canvas.create_rectangle(xPos - 10, yPos - 10,
                                                    xPos + 10, yPos + 10,
                                                    fill = app.airColor,
                                                    width = 0)
                        else:
                            canvas.create_rectangle(xPos - 10, yPos - 10,
                                                    xPos + 10, yPos + 10,
                                                    fill = app.stoneColor,
                                                    width = 0)
        elif app.mode == "mapMode":
            for row in range(app.rows):
                for col in range(app.cols):
                    if self.cave[col][row] == 1:
                        canvas.create_rectangle(row*8, col*8,
                                                (row+1)*8, (col+1)*8,
                                                fill = app.airColor, width = 0)
                    else:
                        canvas.create_rectangle(row*8, col*8,
                                                (row+1)*8, (col+1)*8,
                                                fill = app.stoneColor, width = 0)