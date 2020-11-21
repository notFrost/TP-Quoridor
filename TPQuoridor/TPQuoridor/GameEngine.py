
from InteractableClasses import *


imgBoard = pyi.load('Media/BoardHQ.png')
imgSlot = pyi.load('Media/SlotHQ.png')

BOARD_BORDER = int(SIZE/15)

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

BACKGROUND_SCALE = SIZE/imgBoard.width
#BoardScale=BACKGROUND_SCALE
SLOT_SCALE = BACKGROUND_SCALE*(9/BOARD_SIZE)
JUMP = imgSlot.width*SLOT_SCALE

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
        Board.scale=BACKGROUND_SCALE
        self.SpriteBank.append(Board)
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                Slot = pyglet.sprite.Sprite(self.imgBank[1],
                                            BOARD_BORDER+JUMP*x,
                                            BOARD_BORDER+JUMP*y,
                                            batch=Bruh,group=BoardObj
                                            )
                Slot.scale=SLOT_SCALE
                self.SpriteBank.append(Slot)
        
    def generate_players(self,Nplay):
        #Posiciones iniciales de los 4 Jugadores posibles
        #En orden van 0->Arriba 1->Abajo 2->Izquierda 3->Derecha
        INITIAL_LOCATIONS = [(int(BOARD_SIZE/2)  ,  0),
                             (int(BOARD_SIZE/2)  ,  BOARD_SIZE-1),
                             (0                 ,  int(BOARD_SIZE/2)),
                             (BOARD_SIZE-1       ,  int(BOARD_SIZE/2))]
        for x in range(Nplay):
            self.ArrPlayer.append(Player(INITIAL_LOCATIONS[x],x,self.imgBank[5+x],self.imgBank[7+x]))

    def draw_players(self):
        for x in self.ArrPlayer:
            a=pyglet.sprite.Sprite(self.imgBank[5+x.Order],
                             BOARD_BORDER+JUMP*x.X,
                             BOARD_BORDER+JUMP*x.Y,
                             batch=Bruh,group=Players)
            a.scale=SLOT_SCALE
            self.SpritePlayer.append(a)
    
    def ShowPath(self):
        for x in range(NUMPLAYERS):
            for node in self.ArrPlayer[x].TrazarRuta(self.expanded,self.viewed,self.walls):
                rut = pyglet.sprite.Sprite(self.imgBank[7+x],
                                           BOARD_BORDER+JUMP*node.Pos[0],
                                           BOARD_BORDER+JUMP*node.Pos[1],
                                           batch=Bruh,group=Foreground
                                           )
                rut.scale=SLOT_SCALE
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
        self.WallShadow.scale=SLOT_SCALE

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

    def wall_axis_adjuster(self,Mx,My,xini,yini,xlim,ylim):
        if(Mx>xlim):
            Bx=xlim
        elif (Mx>xini+JUMP*0.5):
            Bx=BOARD_BORDER+JUMP*(int(Mx//JUMP)-1)
        else:
            Bx=xini
        if(My>ylim):
            By=ylim
        elif (My>yini+JUMP*0.5):
            By=BOARD_BORDER+JUMP*(int(My//JUMP))
        else:
            By=yini
        self.WallShadow.x=Bx
        self.WallShadow.y=By

    def TrackMouse(self,Mx,My):
        if(self.WallShadow):
            if(self.WallShadow.rotation==90):
                x_ini=BOARD_BORDER
                y_ini=BOARD_BORDER+JUMP
                x_limit=BOARD_BORDER+JUMP*(BOARD_SIZE-2)
                y_limit=BOARD_BORDER+JUMP*(BOARD_SIZE-1)
            else:
                x_ini=BOARD_BORDER+JUMP
                y_ini=BOARD_BORDER
                x_limit=BOARD_BORDER+JUMP*(BOARD_SIZE-1)
                y_limit=BOARD_BORDER+JUMP*(BOARD_SIZE-2)
            self.wall_axis_adjuster(Mx,My,x_ini,y_ini,x_limit,y_limit) 
 