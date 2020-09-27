import pyglet
import pyglet.image as pyi
import os

#Generacion de la ventana
Size = 600
window = pyglet.window.Window(width=Size,height=Size)

imgBoard = pyi.load('Media/BoardHQ.png')
imgSlot = pyi.load('Media/SlotHQ.png')
imgWall = pyi.load('Media/WallHQ.png')
imgP1 = pyi.load('Media/Player1.png')
imgP2 = pyi.load('Media/Player2.png')
imgP3 = pyi.load('Media/Player3.png')
imgP4 = pyi.load('Media/Player4.png')

mtx_Ass = [imgBoard,imgSlot,imgWall,imgP1,imgP2,imgP3,imgP4]

#Configurar Engine Renderer
Bruh=pyglet.graphics.Batch()
Background = pyglet.graphics.OrderedGroup(0)
BoardObj = pyglet.graphics.OrderedGroup(1)
Foreground = pyglet.graphics.OrderedGroup(2)

BkgrScale = Size/imgBoard.width
Board=pyglet.sprite.Sprite(imgBoard,batch=Bruh,group=Background)
Board.scale=BkgrScale

mtx_Board = []
Jump = imgSlot.width*BkgrScale
BoardSize=9
for x in range(BoardSize):
    for y in range(BoardSize):
        Slot = pyglet.sprite.Sprite(imgSlot,
                                    int(Size/15)+Jump*x,
                                    int(Size/15)+Jump*y,
                                    batch=Bruh,group=BoardObj)
        Slot.scale=BkgrScale
        mtx_Board.append(Slot)

class Engine:

    def __init__(self,mtx_Ass):
        self.mAss = mtx_Ass
        self.LoadEnv()

    def LoadEnv(self):
        Board=pyglet.sprite.Sprite(self.mAss[0],group=Background)
        print("Tablero Cargado")



#Game = Engine(mtx_Ass)

@window.event
def on_draw():
    Bruh.draw()
    print("Dibujando")

pyglet.app.run()