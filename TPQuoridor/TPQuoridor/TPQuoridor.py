
from GameEngine import *

#Generacion de la ventana
window = pyglet.window.Window(width=SIZE,height=SIZE)
fps_display = pyglet.window.FPSDisplay(window=window)

Game = Engine(Assets)
WallTracker = False

def update(dt): 
        pass

pyglet.clock.schedule_interval(update, 1/60)

@window.event
def on_draw():
#    pyglet.clock.tick()
    window.clear()
    Bruh.draw()
    fps_display.draw()


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