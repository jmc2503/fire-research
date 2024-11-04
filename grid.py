from tkinter import *
import random

#Constants for establishing grid and environment appearance
GRID_SIZE = 10 #NxN
SPACE_SIZE = 50
GAME_WIDTH = GRID_SIZE * SPACE_SIZE
GAME_HEIGHT = GRID_SIZE * SPACE_SIZE

#COLOR CONSTANTS
PLAYER_COLOR = "#00FF00" #Green
FIRE_COLOR = "#FF0000" #Red
BACKGROUND_COLOR = "#000000" #Black
OUTLINE_COLOR = "#FFFF00"  #Yellow

#ENVIRONMENT CONSTANTS
FIRE_SPREAD_PROB = 0.1
VIEW_DISTANCE = 3

class FireFighter:
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.square = canvas.create_rectangle(self.x, self.y, self.x + SPACE_SIZE, self.y + SPACE_SIZE, fill=PLAYER_COLOR,tag="player")

class Fire:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = False
        self.square =self.DrawFire()

    def DrawFire(self):
        x_pixel = self.x * SPACE_SIZE
        y_pixel = self.y * SPACE_SIZE
        square = canvas.create_rectangle(x_pixel,y_pixel, x_pixel + SPACE_SIZE, y_pixel +SPACE_SIZE, fill=FIRE_COLOR, tag="fire")
        canvas.itemconfigure(square, state="hidden")
        return square

def ReturnBorders(x, y):
    directions = []
    if y > 0:
        directions.append("up")
    if y < GAME_HEIGHT - 1:
        directions.append("down")
    if x > 0:
        directions.append("left")
    if x < GAME_WIDTH - 1:
        directions.append("right")
    
    return directions

def CheckFireCollision(player):
    global firelist
    for fire in firelist:
        if player.x == fire.x * SPACE_SIZE and player.y == fire.y * SPACE_SIZE:
            canvas.delete(fire.square)  
            firelist.remove(fire)
            break

def CheckFireVisibility(player):
    for fire in firelist:
        dist_x = abs(player.x // SPACE_SIZE - fire.x)
        dist_y = abs(player.y // SPACE_SIZE - fire.y)

        if (dist_x == 0 and dist_y <= VIEW_DISTANCE) or (dist_y == 0 and dist_x <= VIEW_DISTANCE):
            canvas.itemconfigure(fire.square, state="normal")
            fire.visible = True
        else:
            # Otherwise, hide the fire
            canvas.itemconfigure(fire.square, state="hidden")
            fire.visible = False

def DrawViewDistanceOutlines(player):
    # Remove previous outlines
    canvas.delete("outline")

    # Player's position in grid coordinates
    player_grid_x = player.x // SPACE_SIZE
    player_grid_y = player.y // SPACE_SIZE

    for i in range(1, VIEW_DISTANCE + 1):
        if player_grid_y - i >= 0: #UP
            x1, y1 = player.x, (player_grid_y - i) * SPACE_SIZE
            canvas.create_rectangle(x1, y1, x1 + SPACE_SIZE, y1 + SPACE_SIZE, outline=OUTLINE_COLOR, tag="outline")
        if player_grid_y + i < GRID_SIZE: #DOWN
            x1, y1 = player.x, (player_grid_y + i) * SPACE_SIZE
            canvas.create_rectangle(x1, y1, x1 + SPACE_SIZE, y1 + SPACE_SIZE, outline=OUTLINE_COLOR, tag="outline")
        if player_grid_x - i >= 0: #LEFT
            x1, y1 = (player_grid_x - i) * SPACE_SIZE, player.y
            canvas.create_rectangle(x1, y1, x1 + SPACE_SIZE, y1 + SPACE_SIZE, outline=OUTLINE_COLOR, tag="outline")
        if player_grid_x + i < GRID_SIZE: #RIGHT
            x1, y1 = (player_grid_x + i) * SPACE_SIZE, player.y
            canvas.create_rectangle(x1, y1, x1 + SPACE_SIZE, y1 + SPACE_SIZE, outline=OUTLINE_COLOR, tag="outline")

def SpreadFire():
    global firelist
    new_fires = []

    for fire in firelist:
        if FIRE_SPREAD_PROB >= random.random(): #spread fire
            x = fire.x
            y = fire.y

            spreadDirections = ReturnBorders(x, y)
            dir = random.choice(spreadDirections)
            
            if dir == "up": #spread up
                y += 1
            elif dir == "down": #spread down
                y -= 1
            elif dir == "right": #spread right
                x += 1
            elif dir == "left": #spread left
                x -= 1
            
            if all(f.x != x or f.y != y for f in firelist):
                new_fire = Fire(x, y)
                new_fires.append(new_fire)

    firelist.extend(new_fires)      

def MoveSquare(direction, player):

    if direction == "up" and player.y > 0:
        player.y -= SPACE_SIZE
    elif direction == "down" and player.y < GAME_HEIGHT - SPACE_SIZE:
        player.y += SPACE_SIZE
    elif direction == "left" and player.x > 0:
        player.x -= SPACE_SIZE
    elif direction == "right" and player.x < GAME_WIDTH - SPACE_SIZE:
        player.x += SPACE_SIZE
    # Update square position on the canvas
    canvas.coords(player.square, player.x, player.y, player.x + SPACE_SIZE, player.y + SPACE_SIZE)
    SpreadFire()
    CheckFireCollision(player)
    CheckFireVisibility(player)
    DrawViewDistanceOutlines(player)


window = Tk()
window.title("Firefighting Demo")
window.resizable(False, False)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=(GRID_SIZE * SPACE_SIZE), width=(GRID_SIZE * SPACE_SIZE))
canvas.pack()
window.update()

#CENTER THE WINDOW
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

player = FireFighter()

fireStartX = random.randint(0, GRID_SIZE-1)
fireStartY = random.randint(0, GRID_SIZE-1)

firelist = [Fire(fireStartX, fireStartY)]

window.bind("<Up>", lambda event: MoveSquare("up",player))
window.bind("<Down>", lambda event: MoveSquare("down",player))
window.bind("<Left>", lambda event: MoveSquare("left",player))
window.bind("<Right>", lambda event: MoveSquare("right",player))

window.mainloop()