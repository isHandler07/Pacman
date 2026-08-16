import pygame
import math
import random

pygame.init()

h = 1056 #height 33x32
w = 960 #width 30x32

x = 467 #default positions
y = 800
scale = 30
screen = pygame.display.set_mode([w, h])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
cellSize = 32
tick = 0
pacmanImages = []
gamestate = "menu"
level = 1
dotCount = 0
energizerCount = 0
start = True
for i in range(1,3):
    pacmanImages.append(pygame.transform.scale(pygame.image.load(f'PacmanImages/{i}.png'), (scale, scale)))
pacmanImage = pygame.transform.scale(pygame.image.load(f'PacmanImages/1.png'), (50, 50))
redGhostImage = pygame.transform.scale(pygame.image.load(f'GhostImages/redGhost.png'), (scale, scale))
pinkGhostImage = pygame.transform.scale(pygame.image.load(f'GhostImages/pinkGhost.png'), (scale, scale))
orangeGhostImage = pygame.transform.scale(pygame.image.load(f'GhostImages/orangeGhost.png'), (scale, scale))
blueGhostImage = pygame.transform.scale(pygame.image.load(f'GhostImages/blueGhost.png'), (scale, scale))
frightenedGhostImage = pygame.transform.scale(pygame.image.load(f'GhostImages/frightenedGhost.png'), (scale, scale))
whiteGhostImage = pygame.transform.scale(pygame.image.load(f'GhostImages/whiteGhost.png'), (scale, scale))
partialImages =[frightenedGhostImage, whiteGhostImage]
gameoverImage = pygame.transform.scale(pygame.image.load(f'GameoverImage/Gameover.png'), (960, 550))
pauseButtonImage = pygame.transform.scale(pygame.image.load(f'Pause/PauseButton.png'), (27, 45))
pauseMenuImage = pygame.transform.scale(pygame.image.load(f'Pause/PauseMenu.png'), (960, 550))
menuScreenImage = pygame.transform.scale(pygame.image.load(f'Menu/MenuScreen.png'), (960, 550))
controlsImage = pygame.transform.scale(pygame.image.load(f'Menu/ControlScreen.png'), (960, 550))
highScore = 0

#30x31
maze = [
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 2, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 2, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 0, 3, 3, 0, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 0, 3, 3, 0, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 3, 3, 3, 4, 4, 3, 3, 3, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 3, 3, 3, 3, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 2, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 2, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
]

class PriorityQueue :
    def __init__(self) :
        self.queue = []
    
    def enqueue(self, item, priority) :
        self.queue.append((priority, item))
        self.queue.sort()

    def dequeue(self) :
        item = self.queue.pop(0)[1]
        return item

    def notEmpty(self) :
        if len(self.queue) == 0 :
            return False
        else :
            return True

class Sprite :
    def __init__(self, x, y, direction, species) :
        self.x = x #x position
        self.y = y #y position
        self.direction = direction #direction
        self.species = species #Pacman or ghost

class Pacman(Sprite) :
    def __init__(self) :
        super().__init__(467, 800, [0, 0], "Pacman") #inherits sprite class
        self.newDirection = [0, 0] #desired direction entered by user
        self.speed = 2 #Pacman speed
        self.scale = 30 #Pacman scale
        self.score = 0 #Pacman score
        self.lives = 3 #Pacman lives
    
    def drawPacman(self, tick) :
        if self.direction == [1, 0] or self.direction == [0,0] : #right
            screen.blit(pacmanImages[tick // 15], (self.x, self.y))
        elif self.direction == [-1, 0] : #left
            screen.blit(pygame.transform.rotate(pacmanImages[tick // 15], 180), (self.x, self.y))
        elif self.direction == [0, -1] : #up
            screen.blit(pygame.transform.rotate(pacmanImages[tick // 15], 90), (self.x, self.y))
        elif self.direction == [0, 1] : #down
            screen.blit(pygame.transform.rotate(pacmanImages[tick // 15], -90), (self.x, self.y))

    def resetPosition(self) :
        self.x = 467
        self.y = 800
        self.direction = [0, 0]
        self.newDirection = [0, 0]

class Ghost(Sprite) :
    def __init__(self, x, y, direction, type, buffer):
        super().__init__(x, y, direction, "Ghost") #inherits sprite class
        self.type = type #ghost type
        self.mode = "scatter" #ghost mode (chase,scatter,frightened)
        self.buffer = buffer #ghost scatter mode buffer
        self.startTime = pygame.time.get_ticks() + self.buffer #ghost change in mode timestamp
        self.partial = False #end of frightened mode is False
        self.frightenedSpeed = 1 #speed when in frightened mode
        self.frightenedScale = 31
        self.chaseSpeed = 1.5 #speed when in chase or scatter mode
        self.chaseScale = 30.5
        self.speed = self.chaseSpeed #set speed as chaseSpeed
        self.scale = self.chaseScale

    def drawGhost(self, ghostImage, partialImages, tick) :
        if self.mode != "frightened" : #mode in scatter or chase
            screen.blit(ghostImage, (self.x, self.y)) #draw that ghost's specific image
        elif self.mode == "frightened" and self.partial == False : #mode in frightened
            screen.blit(partialImages[0], (self.x, self.y)) #draw frightened image
        else : #mode in end of frightened
            #change between images to create flashing animation
            screen.blit(partialImages[tick // 15], (self.x, self.y))

    def findTarget(self, Pacman, Ghosts, cellSize, maze) :
        #red target position
        targetX = Pacman.x + (Pacman.scale//2) #default target is Pacman position,
        targetY = Pacman.y + (Pacman.scale//2) #if own target position not available
        if self.type == "pink" : #type pink
            #4 tiles in front of Pacman's current direction is target position
            ptargetX = (Pacman.x + Pacman.scale//2) + (Pacman.direction[0])*128
            ptargetY = (Pacman.y + Pacman.scale//2) + (Pacman.direction[1])*128
            cell = [int(ptargetX // cellSize), int(ptargetY // cellSize)] #cell where target position is
            #is target position possible i.e. not a maze wall
            if 0 < ptargetX < 960 and 0 < ptargetY < 992 and maze[cell[1]][cell[0]] != 3 :
                targetX = ptargetX #becomes target position if possible
                targetY = ptargetY
        elif self.type == "blue" : #type blue
            #uses red ghost and mirrored offset from Pac-man to give target position
            ptargetX = Pacman.x + (Pacman.scale//2) + (Pacman.direction[0])*64
            ptargetY = Pacman.y + (Pacman.scale//2) + (Pacman.direction[1])*64
            ptargetX = 2*(targetX - (Ghosts[0].x + self.scale//2)) + Ghosts[0].x #Ghosts[0] is red ghost
            ptargetY = 2*(targetY - (Ghosts[0].y + self.scale//2)) + Ghosts[0].y
            cell = [int(ptargetX // cellSize), int(ptargetY // cellSize)] #cell where target position is
            #is target position possible i.e. not a maze wall
            if 0 < ptargetX < 960 and 0 < ptargetY < 992 and maze[cell[1]][cell[0]] != 3 :
                targetX = ptargetX #becomes target position if possible
                targetY = ptargetY
        elif self.type == "orange" : #if type is orange
            changeX = self.x - Pacman.x #difference in ghost and pacman x
            changeY = self.y - Pacman.y #difference in ghost and pacman y
            distance = math.sqrt((changeX*changeX)+(changeY*changeY)) #distance apart
            if self.mode != "frightened" and distance < 256 : #if within a certain distance (8 tiles)
                self.mode = "scatter" #mode becomes scatter
                targetX = 80 #bottom left corner
                targetY = 912
        return targetX, targetY #returns the targetPosition
    
    def findDirection(self, maze, cellSize, targetX, targetY) :
        #making shortest path
        centreX = self.x + (self.scale//2) #Ghost centre position
        centreY = self.y + (self.scale//2)
        startCell = [int(centreX // cellSize), int(centreY // cellSize)] #Cell where ghost is
        endCell = [int(targetX // cellSize), int(targetY // cellSize)] #Cell where target is
        rows = len(maze) #number of rows of cells in maze list
        columns = len(maze[0]) #number of columns of cells in maze list
        #stores the shortest distance from a cell in the maze to the startCell
        distances = [[float('inf')] * columns for i in range(rows)] #creates a list of same dimensions as maze
        #stores the previous cell in order to get to that cell in the maze (helps recreate shortest path)
        previousPositions = [[None] * columns for i in range(rows)] #creates a list of same dimensions as maze
        queue = PriorityQueue() #makes a queue where priority is not FIFO but which cell has shortest distance
        queue.enqueue(startCell, 0) #enqueues the start cell
        #stores the distance as 0 in the distances list with indexes as cell values
        distances[startCell[1]][startCell[0]] = 0
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]] #list of directions
        while queue.notEmpty() : #if there are still cells to visit
            #current cell becomes cell which has most priority so shortest distance from startCell in queue
            currentCell = queue.dequeue()
            if currentCell == endCell : #if currentCell is same as endCell destination has been reached,
                break #so break from loop no longer need to find path.
            for direction in directions : #iterates through every direction
                #finds neighbouring cell to current cell in that direction
                neighbour = [currentCell[0] + direction[0], currentCell[1] + direction[1]]
                #checks if neighbour is possible, i.e. not a maze wall and within maze bounds
                if 0 <= neighbour[0] < columns and 0 <= neighbour[1] < rows and maze[neighbour[1]][neighbour[0]] != 3 : 
                    #this is the distance from startCell to neighbourCell
                    newDistance = distances[currentCell[1]][currentCell[0]] + 1            
                    #checks if this is less than currently stored distance for that same cell
                    if newDistance < distances[neighbour[1]][neighbour[0]] : #if it is:
                        #set new distance for this neighbour cell in distances list
                        distances[neighbour[1]][neighbour[0]] = newDistance
                        #set previous position for the neighbour cell as current cell as path comes from current cell
                        previousPositions[neighbour[1]][neighbour[0]] = [currentCell[0], currentCell[1]]
                        queue.enqueue(neighbour, newDistance) #enqueue this cell/node to priority queue to keep making path
        #recreating path
        path = [] #empty list to make path
        currentCell = endCell #start from end cell
        #if the ghost is not already at the target position or at the start of the path
        while currentCell != startCell and previousPositions[currentCell[1]][currentCell[0]] is not None :
            path.append(currentCell) #append cell to path
            currentCell = previousPositions[currentCell[1]][currentCell[0]] #change current cell to previous cell
        if len(path) > 0: #if the path is still an empty list
            neighbour = path[len(path)-1] #finds first neighbour cell from startCell
            direction = [neighbour[0] - startCell[0], neighbour[1] - startCell[1]] #optimal direction
            reverseDirection = [-self.direction[0], -self.direction[1]] #finds reverse direction of current direction
            if direction == reverseDirection : #if optimal is travelling backwards
                for d in directions: #iterate through all directions
                    if d != reverseDirection : #if this direction does not equal reverse
                        neighbour = [startCell[0] + d[0], startCell[1] + d[1]] #finds neighbour
                        #checks if this direction is possible, i.e. does not send Ghost through a wall
                        if 0 <= neighbour[0] < columns and 0 <= neighbour[1] < rows and maze[neighbour[1]][neighbour[0]] != 3 :
                            direction = d #if not then this becomes optimal direction
                            break #break from for loop after finding a possible direction biased towards right, left, up, down
        else : #if path is empty because ghost is already at target
            direction = [0,0] #ghost does not move i.e. collided with Pacman
        return direction #returns optimal direction
    
    def moveGhost(self, Pacman, Ghosts, maze, cellSize) :
        if Pacman.direction != [0, 0] : #round only starts when Pacman starts moving/user needs to enter an arrow key
            targetX, targetY = self.findTarget(Pacman, Ghosts, cellSize, maze) #find target position for that Ghost
            direction = self.direction #set direction
            if self.mode == "chase" : #if mode is chase
                #find direction for shortest path to target position
                direction = self.findDirection(maze, cellSize, targetX, targetY)
            elif self.mode == "scatter" : #if mode is scatter
                if self.type == "red" : #if type is red ghost
                    targetX = 880 # target is top right corner
                    targetY = 80
                elif self.type == "pink" : #if type is pink
                    targetX = 80 # target is top left corner
                    targetY = 80
                elif self.type == "blue" : #if type is blue
                    targetX = 880 # target is bottom right corner
                    targetY = 912
                elif self.type == "orange" : #if type is orange
                    targetX = 80 # target is bottom left corner
                    targetY = 912
                #find direction for shortest path to target position
                direction = self.findDirection(maze, cellSize, targetX, targetY)
                changeX = self.x - targetX #difference in ghost and target x
                changeY = self.y - targetY #difference in ghost and target y
                distance = math.sqrt((changeX*changeX)+(changeY*changeY)) #distance apart
                if distance < 192 : #if distance is less than this (6 tiles)
                    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]] #list of directions
                    reverseDirection = [-self.direction[0], -self.direction[1]] #reverse direction to current direction
                    possibleDirections = [] #empty list
                    for direction in directions : #goes through directions list
                        # if that direction is possible and it is not the same as reverse direction
                        if checkWallCollisions(self, cellSize, maze, direction, self.x, self.y) and reverseDirection != direction :
                            possibleDirections.append(direction) #add this direction then to the possible directions list
                    direction = random.choice(possibleDirections) #choose a random direction from the possible directions
            elif self.mode == "frightened" : #if the mode is frightened
                directions = [[1, 0], [-1, 0], [0, 1], [0, -1]] #list of directions
                reverseDirection = [-self.direction[0], -self.direction[1]] #reverse direction to current direction
                possibleDirections = [] #empty list
                for direction in directions : #goes through directions list
                    # if that direction is possible and it is not the same as reverse direction and ghost is not trying to enter the tunnel
                    if checkWallCollisions(self, cellSize, maze, direction, self.x, self.y) and reverseDirection != direction and 0 < self.x < 930 :
                        possibleDirections.append(direction) #add this direction then to the possible directions list
                if len(possibleDirections) == 0 :
                    direction = reverseDirection #if no other possible direction then make ghost go in reverse(happens in tunnel only)
                else : #otherwise
                    direction = random.choice(possibleDirections) #choose a random direction from the possible directions
                self.speed = self.frightenedSpeed #change Ghost speed to frightened speed
                self.scale = self.frightenedScale 
            if checkWallCollisions(self, cellSize, maze, direction, self.x, self.y) : #checks if this direction is possible
                self.direction = direction #set this to the current direction
                self.x = self.x + self.direction[0] * self.speed #change x position
                self.y = self.y + self.direction[1] * self.speed #change y position
            else : #if not ghost moves in its current direction
                self.x = self.x + self.direction[0] * self.speed #change x position
                self.y = self.y + self.direction[1] * self.speed #change y position

    def findMode(self) :
        currentTime = pygame.time.get_ticks() #current timestamp
        time = currentTime - self.startTime #how long Pacman has been in that mode
        if time >= 5000 and self.mode == "scatter" : #scatter mode lasts for 5 secs
            self.mode = "chase" #then change to chase
            self.startTime = pygame.time.get_ticks() #reset timestamp for new mode
        elif time >= 20000 and self.mode == "chase" : #chase lasts for 20 secs
            self.mode = "scatter" #then change to scatter
            self.startTime = pygame.time.get_ticks() #reset timestamp for new mode
        elif time >= 15000 and self.mode == "frightened" : #frightened lasts for 15 secs
            self.mode = "scatter" #then change mode to scatter
            self.speed = self.chaseSpeed #change speed of ghost back to chase
            self.scale = self.chaseScale
            self.partial = False #partial becomes False again as mode has ended
            self.startTime = pygame.time.get_ticks() #reset timestamp for new mode
        elif time >= 12000 and self.mode == "frightened" :
            self.partial = True #partial becomes True as end of frightened

    def resetPosition(self) :
        if self.type == "red" : #for red Ghost
            self.x = 384 #default x
            self.y = 448 #default y
        elif self.type == "pink" : #for pink Ghost
            self.x = 544 #default x
            self.y = 448 #default y
        elif self.type == "blue" : #for blue Ghost
            self.x = 384 #default x
            self.y = 512 #default y
        elif self.type == "orange" : #for orange Ghost
            self.x = 544 #default x
            self.y = 512 #default y
        self.mode = "scatter" #changes the mode to scatter as this is initial Ghost mode
        self.startTime = pygame.time.get_ticks() + 5000 #changes timestamp as mode changed
        self.speed = self.chaseSpeed #changes speed back to chaseSpeed
        self.scale = self.chaseScale

def checkGhostCollisions(Pacman, Ghosts, cellSize, score, gamestate) :
    for Ghost in Ghosts : #iterates through Ghosts list
        centreGX = Ghost.x + Ghost.scale//2 #gets the centre x position of the ghost
        centreGY = Ghost.y + Ghost.scale//2 #gets the centre y position of the ghost
        cellG = [int(centreGX//cellSize), int(centreGY//cellSize)] #finds corresponding cell
        centrePX = Pacman.x + Pacman.scale//2 #gets the centre x position of the Pacman
        centrePY = Pacman.y + Pacman.scale//2 #gets the centre y position of the Pacman
        cellP = [int(centrePX//cellSize), int(centrePY//cellSize)] #finds corresponding cell
        if cellG == cellP : #checks if cells are equal to each other
            if Ghost.mode != "frightened" : #if the ghost mode is not frightened
                Pacman.lives -= 1 #decrease life count
                if Pacman.lives == 0 : #if life count is 0 screen becomes gameover
                    gamestate = "gameover"
                    break
                #reset the round
                Pacman.resetPosition() #reset Pacman's positions
                for Ghost in Ghosts :
                    Ghost.resetPosition() #reset Ghost's positions
                break
            else : # if ghost mode is frightened
                score += 200 #score increments by 200
                Ghost.resetPosition() #reset that ghost's position as it has collides
    return score, gamestate #returns score and gamestate (as these can change)

def drawGameOver(gameoverImage) :
    screen.blit(gameoverImage, (0, 250))
        
def drawMaze(maze, cellSize):
    for indexY in range(len(maze)): # X index in maze 2D list
        for indexX in range(len(maze[indexY])): # Y index in maze 2D list
            x = indexX * cellSize # x coordinate
            y = indexY * cellSize # y coordinate
            cell = maze[indexY][indexX] # cell in maze
            if cell == 1:  # Dot
                pygame.draw.circle(screen, 'white', (x + cellSize // 2, y + cellSize // 2), 4)
            elif cell == 2:  # Energizer
                pygame.draw.circle(screen, 'white', (x + cellSize // 2, y + cellSize // 2), 8)
            elif cell == 3:  # Wall
                pygame.draw.rect(screen, 'blue', (x, y, cellSize, cellSize))
            elif cell == 4: # Ghost Wall
                pygame.draw.rect(screen, (0, 255, 255), (x, y, cellSize, cellSize))

def checkDotsCollision(Sprite, cellSize, maze) :
    centreX = Sprite.x + (Sprite.scale//2) #Pacman centre position
    centreY = Sprite.y + (Sprite.scale//2)
    indexX = centreX // cellSize #index of where Pacman's centre is,
    indexY = centreY // cellSize #dots collected when Pacman's centre is over dot
    if maze[indexY][indexX] == 1 : #checks if this index has a dot
        maze[indexY][indexX] = 0 #get rid of dot from maze
        return maze, "dot" #return new maze and type of item
    elif maze[indexY][indexX] == 2 : #checks if this index has an energizer
        maze[indexY][indexX] = 0 #get rid of energizer from maze
        return maze, "energizer" #return new maze and type of item
    else : #does not collide with any item
        return maze, None #returns same maze and None as no item collected
    
def scoring(Pacman, cellSize, maze, Ghosts, dotCount, energizerCount, level, start) :
    score = Pacman.score #gets score as Pacman score
    if Pacman.direction != [0,0] : #only starts collecting dots if Pacman starts moving
        maze, type = checkDotsCollision(Pacman, cellSize, maze) #checks if Pacman has collided with an item
        if type == "dot" : #if item is dot
            dotCount += 1 #increment dot count as dot collected
            score += 10 #increment score by 10 as dot collected
            #check if all items have been collected now that another one has
            level, maze, dotCount, energizerCount, start = newLevel(level, Pacman, Ghosts, dotCount, energizerCount, maze, start)
        elif type == "energizer" : #if item is energizer
            energizerCount += 1 #increment energizer count as energizer collected
            score += 50 #increment score by 50 as energizer collected
            enableEnergizer(Ghosts) #enable the energizer powerup
            #check if all items have been collected now that another one has
            level, maze, dotCount, energizerCount, start = newLevel(level, Pacman, Ghosts, dotCount, energizerCount, maze, start)
    return maze, score, dotCount, energizerCount, level, start #returns values

def enableEnergizer(Ghosts) :
    for Ghost in Ghosts : #iterates over Ghosts list
        Ghost.mode = "frightened" #ghost mode is in frightened
        Ghost.partial = False #start of powerup so partial should be False
        Ghost.startTime = pygame.time.get_ticks() #timestamp to when this mode started

def scoreUpdate(score):
    scoreText = font.render(f'Score: {score}', True, 'white')
    screen.blit(scoreText, (450, 1000))

def checkWallCollisions(Sprite, cellSize, maze, direction, x, y) :
    nextXL = x #left x of sprite
    nextXR = x + Sprite.scale #right x of sprite
    nextYU = y #top y of sprite
    nextYD = y + Sprite.scale #bottom y of sprite
    speed = Sprite.speed #speed sprite
    if direction == [1, 0] : #right
        nextXL += speed #x coordinates change to the right
        nextXR += speed
    elif direction == [-1, 0] : #left
        nextXL -= speed #x coordinates change to the left
        nextXR -= speed
    elif direction == [0, -1] : #up
        nextYU -= speed #y coordinates change up
        nextYD -= speed
    elif direction == [0, 1] : #y coordinates change down
        nextYU += speed
        nextYD += speed
    indexXL = int(nextXL // cellSize) #maze coordinate for left x
    indexXR = int(nextXR // cellSize) #maze coordinate for right x
    indexYU = int(nextYU // cellSize) #maze coordinate for top y
    indexYD = int(nextYD // cellSize) #maze coordinate for bottom y
    if Sprite.species == "Pacman" or (Sprite.species == "Ghost" and Sprite.mode == "frightened") :
        #checking if any of the corners of the Sprite touch the ghost door for that direction
        if nextXL < 960 and maze[indexYU][indexXL] == 4 : #top left corner
            return False
        elif nextXR < 960 and maze[indexYU][indexXR] == 4 : #top right corner
            return False
        elif nextXL < 960 and maze[indexYD][indexXL] == 4 : #bottom left corner
            return False
        elif nextXR < 960 and maze[indexYD][indexXR] == 4 : #bottom right corner
            return False
    #checking if any of the corners of Sprite touch the maze walls for that direction
    if nextXL < 960 and maze[indexYU][indexXL] == 3 : #tope left corner
        return False
    elif nextXR < 960 and maze[indexYU][indexXR] == 3 : #top right corner
        return False
    elif nextXL < 960 and maze[indexYD][indexXL] == 3 : #bottom left corner
        return False
    elif nextXR < 960 and maze[indexYD][indexXR] == 3 : #bottom right corner
        return False
    else :
        return True #if none of these corners touch a maze wall then it is a possible direction

def moveEntity(Sprite, cellSize, maze) :
    x = Sprite.x #x position of sprite
    y = Sprite.y #y position of sprite
    newDirection = Sprite.newDirection #desired direction of sprite
    direction = Sprite.direction #current direction of sprite
    if newDirection != direction: #if they are distinct check newDirection
        #if its valid i.e. no maze wall in this direction
        if checkWallCollisions(Sprite, cellSize, maze, newDirection, x, y):
            direction = newDirection #set direction as desired direction
    nextX = x + direction[0] * Sprite.speed #next possible position
    nextY = y + direction[1] * Sprite.speed
    #checks if current direction is valid
    if checkWallCollisions(Sprite, cellSize, maze, direction, x, y):
        #if valid Sprite's position become next possible position
        x = nextX
        y = nextY
        if nextX >= 930 : #if tunnel is used in the right entrance
            x = 0 #teleport to the left
        elif nextX <= 0 : #if tunnel is used in the left entrance
            x = 930 #teleport to the right
    #if both current and desired direction not valid then sprite does not move,
    #moves when a desired direction entered by the user is valid
    return x, y, direction

def drawLives(lives, pacmanImage) :
    x = 50 #x position of first life
    y = 1000 #y position of first life
    for i in range(lives) : #runs for how many lives there are
        screen.blit(pacmanImage, (x, y)) #draw one life
        x += 60 #increments the x position of the life to be drawn by 60

def newLevel(level, Pacman, Ghosts, dotCount, energizerCount, maze, start) :
    if dotCount >= 220 and energizerCount >= 4 : #checks if all items have been collected
        level += 1 #increase level by 1 for other modules to use
        dotCount = 0 #reset these counts for new level
        energizerCount = 0
        start = True #new round is starting
        maze = resetMaze(Pacman, Ghosts) #resets maze and ghost and Pacman's positions
        increasingDifficulty(level, Pacman, Ghosts) #makes the new level harder
    return level, maze, dotCount, energizerCount, start #returns values

def resetMaze(Pacman, Ghosts) :
    Pacman.resetPosition() #resets Pacman's position
    for Ghost in Ghosts : #iterates through Ghost list
        Ghost.resetPosition() #resets each ghosts position
    maze = [
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 2, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 2, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 0, 3, 3, 0, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 0, 3, 3, 0, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 3, 3, 3, 4, 4, 3, 3, 3, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 3, 3, 3, 3, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3], 
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3],
[3, 3, 2, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 1, 3, 3, 3, 3, 2, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
] #changes maze to initial layout
    return maze

def increasingDifficulty(level, Pacman, Ghosts) :
    if level % 3 == 0 and Pacman.lives < 3 : #every 3 levels
        Pacman.lives += 1 #lives increases by 1 as a reward for the player
    for Ghost in Ghosts : #iterates through ghost list
        if Ghost.speed < Pacman.speed : #makes sure maximum ghost speed is the same as Pacman's
            Ghost.chaseSpeed += 0.1 #increments current ghost speed by 0.1
            Ghost.chaseScale -= 0.1

def drawPauseButton(pauseButtonImage) :
    screen.blit(pauseButtonImage, (900, 10))

def pauseButton(position, gamestate, Pacman) :
    x = position[0] #gets the x-coordinate from where mouse click was
    y = position[1] #gets the y-coordinate as well
    #checks when in gamestate play that the pause button is clicked by using pause button boundaries
    if 900 < x < 927 and 10 < y < 55 and gamestate == "play" :
        gamestate = "pause" #changes gamestate to pause as button is clicked
    #checks when in gamestate Pause that the pause button is clicked by using pause button boundaries
    elif 900 < x < 927 and 10 < y < 55 and gamestate == "pause" :
        gamestate = "play" #changes gamestate to play as button is clicked
        Pacman.direction = [0, 0] #makes direction reset so sprites only reset when player clicks an arrow key
        Pacman.newDirection = [0, 0]
    return gamestate #returns resulting gamestate

def drawPauseMenu(pauseMenuImage) :
    screen.blit(pauseMenuImage, (0, 250))

def menuButton(position, gamestate) :
    x = position[0] #gets the x-coordinate from where mouse click was
    y = position[1] #gets the y-coordinate as well
    #checks when in gamestate Pause that the menu button is clicked by using menu button boundaries
    if 735 < x < 860 and 635 < y < 760 and gamestate == "pause" :
        gamestate = "menu" #changes gamestate to menu as button is clicked
    #checks when in gamestate gameover or controls that the menu button is clicked
    elif 870 < x < 930 and 720 < y < 780 and (gamestate == "gameover" or gamestate == "controls") :
        gamestate = "menu" #changes gamestate to menu as button is clicked
    return gamestate #returns gamestate

def drawMenuScreen(menuScreenImage) :
    screen.blit(menuScreenImage, (0, 250))

def menuOptions(position) :
    x = position[0] #gets the x-coordinate from where mouse click was
    y = position[1] #gets the y-coordinate as well
    if 320 < x < 640 : #checks if x-coordinate was where the options are
        if 475 < y < 575 : #checks y-coordinate to see if option 1 is clicked
            return "play" #returns corresponding gamestate for option 1
        elif 575 < y < 675 : #checks y-coordinate to see if option 2 is clicked
            return "controls" #returns corresponding gamestate for option 2
        elif 675 < y < 775 : #checks y-coordinate to see if option 3 is clicked
            return "quit" #returns corresponding gamestate for option 3
    return "menu" #if click is outside all menu options return menu as gamestate should not change

def resetEverything(Pacman, Ghosts, maze, level, dotCount, energizerCount, start) :
    for Ghost in Ghosts : #iterates through the ghost list and gets each ghost
        Ghost.chaseSpeed = 1.5 #changes the Ghost speed to original level 1 speed
        Ghost.chaseScale = 30.5
        Ghost.partial = False #makes sure partial is False
    maze = resetMaze(Pacman, Ghosts) #resetsMaze to have all the dots back and Ghosts and Pacman
    Pacman.score = 0 #score is set back to 0
    Pacman.lives = 3 #lives is set back to 3
    level = 1 #level is 1 again
    dotCount = 0 #reset dot and energizer count
    energizerCount = 0
    start = True #start becomes true as only a new round begins now
    return maze, level, dotCount, energizerCount, start #returns values

def drawControlsScreen(ControlImage) :
    screen.blit(ControlImage, (0, 250)) #screen becomes control screen

def ghostsStartRound(Ghosts, start, PacmanDirection) :
    if start == True and PacmanDirection != [0, 0] : #checks if the round has just started
        for Ghost in Ghosts : #iterates through the ghost list and gets each ghost
            Ghost.mode = "scatter" #changes each ghost's mode to scatter
            #changes the timestamp of startTime to indicate a change in mode,
            #Ghost buffer allows ghost to be in scatter mode at the start of the round for longer,
            #but also lets the scatter modes start and end at different points throughout the round
            Ghost.startTime = pygame.time.get_ticks() + Ghost.buffer
            start = False #changes the start to False as it is no longer the start of a round
    return start #returns value of start for other modules to use

def showHighScore() :
    highScoreFile = open("highScore.txt", "r") #highScore file is opened in read mode
    highScore = highScoreFile.read() #reads the entire file and returns it as a string
    #closes the file to maintain data integrity and avoid issues like data corruption and resource leaks
    highScoreFile.close()
    #Gets the entire text to be outputted on screen together
    scoreText = font.render(f'High Score: {highScore}', True, 'white')
    screen.blit(scoreText, (750, 1000)) #Outputs the highScore onto the screen
    return int(highScore) #returns the highScore for other modules to use

def checkNewHighScore(score, highScore) :
    if score > highScore : #checks if user score is greater than high score
        highScoreFile = open("highScore.txt", "w") #opens file in write mode
        highScoreFile.write(str(score)) #then overwrites current contents of file with the user's score
        highScoreFile.close() #closes the file for same reason as above
        highScore = score #sets highScore as user score
    return highScore #returns the highScore

Pacman1 = Pacman()
redGhost = Ghost(384, 448, [1,0], "red", 10000)
pinkGhost = Ghost(544, 448, [-1,0], "pink", 7000)
orangeGhost = Ghost(384, 512, [1,0], "orange", 5000)
blueGhost = Ghost(544, 512, [-1,0], "blue", 2000)

Ghosts =[]
Ghosts.append(redGhost)
Ghosts.append(pinkGhost)
Ghosts.append(orangeGhost)
Ghosts.append(blueGhost)

run = True
while run:
    timer.tick(fps)
    if tick == 29 :
        tick = 0
    else :
        tick += 1
    screen.fill('black')
    if gamestate == "play" :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RIGHT :
                    Pacman1.newDirection = [1, 0]
                if event.key == pygame.K_LEFT :
                    Pacman1.newDirection = [-1, 0]
                if event.key == pygame.K_UP :
                    Pacman1.newDirection = [0, -1]
                if event.key == pygame.K_DOWN :
                    Pacman1.newDirection = [0, 1]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gamestate = pauseButton(event.pos, gamestate, Pacman1)
        drawMaze(maze, cellSize)
        scoreUpdate(Pacman1.score)
        Pacman1.x, Pacman1.y, Pacman1.direction = moveEntity(Pacman1, cellSize, maze)   
        Pacman1.drawPacman(tick)
        redGhost.drawGhost(redGhostImage, partialImages, tick)
        pinkGhost.drawGhost(pinkGhostImage, partialImages, tick)
        orangeGhost.drawGhost(orangeGhostImage, partialImages, tick)
        blueGhost.drawGhost(blueGhostImage, partialImages, tick)
        start = ghostsStartRound(Ghosts, start, Pacman1.direction)
        redGhost.findMode()
        pinkGhost.findMode()
        blueGhost.findMode()
        orangeGhost.findMode()
        redGhost.moveGhost(Pacman1, Ghosts, maze, cellSize)
        pinkGhost.moveGhost(Pacman1, Ghosts, maze, cellSize)
        orangeGhost.moveGhost(Pacman1, Ghosts, maze, cellSize)
        blueGhost.moveGhost(Pacman1, Ghosts, maze, cellSize)
        Pacman1.score, gamestate = checkGhostCollisions(Pacman1, Ghosts, cellSize, Pacman1.score, gamestate)
        maze, Pacman1.score, dotCount, energizerCount, level, start = scoring(Pacman1, cellSize, maze, Ghosts, dotCount, energizerCount, level, start)
        drawLives(Pacman1.lives, pacmanImage)
        drawPauseButton(pauseButtonImage)
        highScore = showHighScore()
        checkNewHighScore(Pacman1.score, highScore)
    elif gamestate == "gameover" :
        drawGameOver(gameoverImage)
        scoreUpdate(Pacman1.score)
        highScore = showHighScore()
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gamestate = menuButton(event.pos, gamestate)
        if gamestate == "menu" :
            maze, level, dotCount, energizerCount, start = resetEverything(Pacman1, Ghosts, maze, level, dotCount, energizerCount, start)
    elif gamestate == "pause" :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gamestate = pauseButton(event.pos, gamestate, Pacman1)
                    gamestate = menuButton(event.pos, gamestate)
        drawPauseButton(pauseButtonImage)
        drawPauseMenu(pauseMenuImage)
        if gamestate == "menu" :
            maze, level, dotCount, energizerCount, start = resetEverything(Pacman1, Ghosts, maze, level, dotCount, energizerCount, start)
    elif gamestate == "menu" :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gamestate = menuOptions(event.pos)
        drawMenuScreen(menuScreenImage)
    elif gamestate == "quit" :
        run = False
    elif gamestate == "controls" :
        drawControlsScreen(controlsImage)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gamestate = menuButton(event.pos, gamestate)
    pygame.display.flip()
pygame.quit()