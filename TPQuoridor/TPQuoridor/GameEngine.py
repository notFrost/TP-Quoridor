
from InteractableClasses import *

Assets=[]
f = open("Media/IndexMedia.txt", "r")
for x in f:
    x=x.strip()
    Assets.append(x)


class Engine:
    def __init__(self,Ass_List):
        self.mtxAssets = Ass_List
        self.imgBank = []
        self.SpriteBank = []
        self.SpritePlayer = []
        self.ArrPlayer = []
        self.ArrPathing = []
        self.viewed, self.expanded= [],[]
        self.walls=False
        self.mode=0

        self.load_env()
        self.generate_players(NUMPLAYERS)
        self.ShowPath()

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
        self.walls=WallArray(self.imgBank[2],self.imgBank[3])
        
    def generate_players(self,Nplay):
        """
       Posiciones iniciales de los 4 Jugadores posibles:
       0->Arriba
       1->Arriba,Abajo 
       2->Arriba,Abajo,Izquierda 
       3->Arriba,Abajo,Izquierda,Derecha
        """
        INITIAL_LOCATIONS = [(int(BOARD_SIZE/2) +1 ,  0),
                             (int(BOARD_SIZE/2) -1   ,  BOARD_SIZE-1),
                             (0                 ,  int(BOARD_SIZE/2)    +1) ,
                             (BOARD_SIZE-1       ,  int(BOARD_SIZE/2)   -1)]

        GOAL_LOCATIONS = [( int(BOARD_SIZE/2),BOARD_SIZE-1),
                             (int(BOARD_SIZE/2),0),
                             (BOARD_SIZE-1,int(BOARD_SIZE/2)),
                             (0,int(BOARD_SIZE/2))]
        for x in range(Nplay):
            self.ArrPlayer.append(Player(INITIAL_LOCATIONS[x],GOAL_LOCATIONS[x],x,self.imgBank[5+x],self.imgBank[9+x]))

    def ShowPath(self):
        for x in self.ArrPlayer:
            x.generate_route(self.expanded,self.viewed,self.walls.wall_array)
            x.show_route()
            self.viewed, self.expanded = [],[]
        pass

    def set_mode(self,key):
        """
        DESIGNACION DE LOS MODOS DEL JUEGO
        0  -> Idle, los jugadores pueden clickear el entorno
        1  -> Wall_Placement, un jugador va a colocar una pared
        2  -> Player Move, un jugador va a mover su ficha
        """
        self.mode=key

    def key_command(self,key):
        if self.mode==0:
            if key==1:
                self.set_mode(1)
                self.walls.command_manager(key)
        elif self.mode==1:
            if key==3 or key==2:
                self.walls.command_manager(key)
                if key==3:
                    self.set_mode(0)
                    self.ShowPath()
                
    
    def PlaceWall(self):
        print("se coloco xd")

    def TrackMouse(self,Mx,My):
        if self.mode==1:
            if self.walls.refresh_shadow_pos(Mx,My):
               self.ShowPath()
        pass
 