import pyglet
import pyglet.image as pyi
import os

from Pathfinders import *

#Generacion de la ventana

window = pyglet.window.Window(width=SIZE,height=SIZE)

imgBoard = pyi.load('Media/BoardHQ.png')
imgSlot = pyi.load('Media/SlotHQ.png')

Assets=[]
f = open("Media/IndexMedia.txt", "r")
for x in f:
    x=x.strip()
    Assets.append(x)

#Configurar Engine Renderer
Bruh=pyglet.graphics.Batch()
Background = pyglet.graphics.OrderedGroup(0)
BoardObj = pyglet.graphics.OrderedGroup(1)
Foreground = pyglet.graphics.OrderedGroup(2)
Walls = pyglet.graphics.OrderedGroup(4)
Players = pyglet.graphics.OrderedGroup(3)

BkgrScale = SIZE/imgBoard.width
BoardScale=BkgrScale
SlotScale = BkgrScale*(9/BOARDSIZE)
Jump = imgSlot.width*SlotScale

class Engine:
    def __init__(self,Ass_List):
        self.mtxAssets = Ass_List
        self.imgBank = []
        self.SpriteBank = []
        self.SpritePlayer = []
        self.SpriteWalls=[]
        self.ArrPlayer = []
        self.ArrPathing = []
        self.viewed, self.expanded,self.walls = [],[],[]
        self.WallShadow=False

        self.load_env()
        self.generate_players(NUMPLAYERS)
        self.draw_players()
        #self.ShowPath()

    def load_env(self):
        #Esto Carga los Assets desde el txt
        for x in self.mtxAssets:
            self.imgBank.append(pyi.load(x))
        #Esto genera el tablero y los espacios para las piezas
        Board=pyglet.sprite.Sprite(self.imgBank[0],batch=Bruh,group=Background)
        print("Tablero Cargado")
        Board.scale=BkgrScale
        self.SpriteBank.append(Board)
        for x in range(BOARDSIZE):
            for y in range(BOARDSIZE):
                Slot = pyglet.sprite.Sprite(self.imgBank[1],
                                            int(SIZE/15)+Jump*x,
                                            int(SIZE/15)+Jump*y,
                                            batch=Bruh,group=BoardObj
                                            )
                Slot.scale=SlotScale
                self.SpriteBank.append(Slot)
        
                

    def generate_players(self,Nplay):
        #Posiciones iniciales de los 4 Jugadores posibles
        #En orden van 0->Arriba 1->Abajo 2->Izquierda 3->Derecha
        INITIAL_LOCATIONS = [(int(BOARDSIZE/2)  ,  0),
                             (int(BOARDSIZE/2)  ,  BOARDSIZE-1),
                             (0                 ,  int(BOARDSIZE/2)),
                             (BOARDSIZE-1       ,  int(BOARDSIZE/2))]
        for x in range(Nplay):
            self.ArrPlayer.append(Player(INITIAL_LOCATIONS[x],x,self.imgBank[5+x],self.imgBank[7+x]))

    def draw_players(self):
        for x in self.ArrPlayer:
            a=pyglet.sprite.Sprite(self.imgBank[5+x.Order],
                             int(SIZE/15)+Jump*x.X,
                             int(SIZE/15)+Jump*x.Y,
                             batch=Bruh,group=Players)
            a.scale=SlotScale
            self.SpritePlayer.append(a)
    
    def ShowPath(self):
        for x in range(NUMPLAYERS):
            for node in self.ArrPlayer[x].TrazarRuta(self.expanded,self.viewed,self.walls):
                rut = pyglet.sprite.Sprite(self.imgBank[7+x],
                                           int(SIZE/15)+Jump*node.Pos[0],
                                           int(SIZE/15)+Jump*node.Pos[1],
                                           batch=Bruh,group=Foreground
                                           )
                rut.scale=SlotScale
                self.ArrPathing.append(rut)
                self.viewed,self.expanded = [],[]


    def key_command(self,key):
        if key==1:
            self.enable_wall_tracker()
        elif self.WallShadow:
            if key==2:
                self.rotate_wall()
            elif key==3:
                self.PlaceWall()

    def enable_wall_tracker(self):
        self.WallShadow=pyglet.sprite.Sprite(self.imgBank[3],0,0,batch=Bruh,group=Walls)
        self.WallShadow.scale=SlotScale

    def rotate_wall(self):
        if self.WallShadow.rotation==0:
            self.WallShadow.rotation=90
        else: 
            self.WallShadow.rotation=0

    def PlaceWall(self):
        X=self.WallShadow.x
        Y=self.WallShadow.y
        print("X: "+str(X) + ", Y: "+str(Y))
        self.WallShadow.delete()
        self.WallShadow=False

    def TrackMouse(self,Mx,My):
        if self.WallShadow:
            self.WallShadow.x=Mx
            self.WallShadow.y=My

    

class Player:
    def __init__(self,initial_coords,color,AssCol,AssPath):
        self.X=initial_coords[0]
        self.Y=initial_coords[1]
        self.Order=color
        self.Asset_Player=AssCol
        self.Asset_Path=AssPath

    def TrazarRuta(self,expanded,viewed,walls):
        self.Route=Routing((self.X,self.Y),expanded,viewed,walls,(self.MetaX,self.MetaY))
        return self.Route

    def DrawPlayer(self,img):
        pyglet.sprite.Sprite(img,
                             int(SIZE/15)+Jump*self.X,
                             int(SIZE/15)+Jump*self.Y,
                             batch=Bruh,group=Foreground)
        pass

    def ShowPath(self):
        mtx_Path=[]
        for node in self.Route:
            rut = pyglet.sprite.Sprite(self.Asset_Player,
                                       int(SIZE/15)+Jump*node.Pos[0],
                                       int(SIZE/15)+Jump*node.Pos[1],
                                       batch=Bruh,group=Foreground)
            rut.scale=BkgrScale
            mtx_Path.append(rut)
            


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