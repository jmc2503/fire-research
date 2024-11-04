from tkinter import *
import random

#Constants for establishing grid and environment appearance
GRID_SIZE = 10 #NxN
SPACE_SIZE = 50
GAME_WIDTH = GRID_SIZE * SPACE_SIZE
GAME_HEIGHT = GRID_SIZE * SPACE_SIZE
PLAYER_COLOR = "#00FF00" #Green
FIRE_COLOR = "#FF0000" #Red
BACKGROUND_COLOR = "#000000" #Black

class FireFighter:
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.square = canvas.create_rectangle(self.x, self.y, self.x+SPACE_SIZE, self.y+SPACE_SIZE, fill=PLAYER_COLOR,tag="player")

class Fire:
    def __init__(self):
        pass

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

window.bind("<Up>", lambda event: MoveSquare("up",player))
window.bind("<Down>", lambda event: MoveSquare("down",player))
window.bind("<Left>", lambda event: MoveSquare("left",player))
window.bind("<Right>", lambda event: MoveSquare("right",player))

window.mainloop()