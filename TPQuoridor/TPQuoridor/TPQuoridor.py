
from GameEngine import *

#Generacion de la ventana
window = pyglet.window.Window(width=SIZE,height=SIZE)

Game = Engine(Assets)
WallTracker = False

@window.event
def on_draw():
    window.clear()
    Bruh.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        Game.key_command(1)
    elif symbol == pyglet.window.key.R:
        Game.key_command(2)
    elif symbol == pyglet.window.key.ENTER:
        Game.key_command(3)

@window.event
def on_mouse_motion(x, y, dx, dy):
    #print("X: "+str(x) + ", Y: "+str(y))
    Game.TrackMouse(x,y)

pyglet.app.run()