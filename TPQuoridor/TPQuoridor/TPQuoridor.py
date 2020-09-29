import pyglet
import pyglet.image as pyi
import os

#Generacion de la ventana
Size = 800
BoardSize=20
window = pyglet.window.Window(width=Size,height=Size)

imgBoard = pyi.load('Media/BoardHQ.png')
imgSlot = pyi.load('Media/SlotHQ.png')
imgWall = pyi.load('Media/WallHQ.png')
imgP1 = pyi.load('Media/Player1.png')
imgP2 = pyi.load('Media/Player2.png')
imgP3 = pyi.load('Media/Player3.png')
imgP4 = pyi.load('Media/Player4.png')
slotP1 = pyi.load('Media/SLOTP1.png')
slotP2 = pyi.load('Media/SLOTP2.png')
slotP3 = pyi.load('Media/SLOTP3.png')
slotP4 = pyi.load('Media/SLOTP4.png')
mtx_Ass = [imgBoard,imgSlot,imgWall,imgP1,imgP2,imgP3,imgP4]
mtx_Alg_Ass = [slotP1,slotP2,slotP3,slotP4]
#Configurar Engine Renderer
Bruh=pyglet.graphics.Batch()
Background = pyglet.graphics.OrderedGroup(0)
BoardObj = pyglet.graphics.OrderedGroup(1)
Foreground = pyglet.graphics.OrderedGroup(2)

BkgrScale = Size/imgBoard.width
Board=pyglet.sprite.Sprite(imgBoard,batch=Bruh,group=Background)
Board.scale=BkgrScale

mtx_Board = []
SlotScale = BkgrScale*(9/BoardSize)
Jump = imgSlot.width*SlotScale

for x in range(BoardSize):
    for y in range(BoardSize):
        Slot = pyglet.sprite.Sprite(imgSlot,
                                    int(Size/15)+Jump*x,
                                    int(Size/15)+Jump*y,
                                    batch=Bruh,group=BoardObj)
        Slot.scale=SlotScale
        mtx_Board.append(Slot)
        pass
class Engine:

    def __init__(self,mtx_Ass):
        self.mAss = mtx_Ass
        self.LoadEnv()

    def LoadEnv(self):
        Board=pyglet.sprite.Sprite(self.mAss[0],group=Background)
        print("Tablero Cargado")


def finish(Node):
  Recorrido = []
  #recorre expanded desde el nodo end hasta que el nodo que estemos tenga como prev "start"
  while Node.prev != False:
    Recorrido.append(Node)
    Node = Node.prev
  Recorrido.append(Node)
  Recorrido.reverse()
  return Recorrido

#Node
class Node:
  def __init__(self, pos, pre, end):
    self.Pos = pos
    self.prev = pre
    if self.prev!=False:
      self.G = self.prev.G+1
    else:
      self.G = 0
    self.F = self.calcf(end)

  def calcf(self, end):
    h = abs(self.Pos[0]-end[0])+abs(self.Pos[1]-end[1])
    return h+self.G

#Checking Functions ##Tenemos que conseguir dimensions de algun lugar, esta en lectura de .txt
def CheckBorder(Pos):
  if (Pos[0]>=0 and Pos[0]<BoardSize) and (Pos[1]>=0 and Pos[1]<BoardSize):
    return True
  return False

def CheckPrev(curr,Pos):
  if not curr.prev:
    return True
  elif curr.prev.Pos == Pos:
    return False
  return True
  
def CheckArr(arr,Pos):
  for i in arr:
    if i.Pos == Pos:
      return False
  return True

def CheckF(Nod):
  return Nod.F

def Routing(start,expanded,viewed,walls,end):
    Aux=Node(start, False, end)
    viewed.append(Aux)
    return Astar(expanded, viewed, walls, end)

#Main Aglorithm
def Astar(expanded, viewed, walls, end):
  curr = viewed[0]
  if curr.Pos == end:
    expanded.append(curr)
    print('End encontrado')
    return finish(curr)
  #Cardinal Verification
  Nb = []
  for i in [-1,1]:
    Nb.append((curr.Pos[0],curr.Pos[1]+i))
    Nb.append((curr.Pos[0]+i,curr.Pos[1]))
  for next in Nb:
    #To do: Añadir implementacion de CheckWalls()
    if CheckPrev(curr,next) and CheckBorder(next) and CheckArr(expanded,next) and CheckArr(viewed,next):
      viewed.append(Node(next,curr, end))
  #Add to expanded and Sort new Viewed List
  expanded.append(curr)
  viewed.pop(0)
  viewed.sort(key=CheckF)
  #Possibility Verification
  if viewed:
    return Astar(expanded, viewed, walls, end)
  else:
    return false
 

class Player:
    def __init__(self,x,y,color,AssCol,AssPath):
        self.X=x
        self.Y=y
        self.MetaX=BoardSize-1
        self.MetaY=BoardSize-1
        self.Order=color
        self.Asset_Player=AssCol
        self.Asset_Path=AssPath
        self.DefinirDireccion()

    def DefinirDireccion(self):
        if self.X==0:
            self.MetaX=BoardSize-1
            self.MetaY=int(BoardSize/2)
        elif self.Y==0:
            self.MetaX=int(BoardSize/2)
            self.MetaY=BoardSize-1
        pass

    def TrazarRuta(self,expanded,viewed,walls):
        self.Route=Routing((self.X,self.Y),expanded,viewed,walls,(self.MetaX,self.MetaY))
        return self.Route

    def DrawPlayer(self,img):
        pyglet.sprite.Sprite(img,
                             int(Size/15)+Jump*self.X,
                             int(Size/15)+Jump*self.Y,
                             batch=Bruh,group=Foreground)
        pass

    def ShowPath(self):
        mtx_Path=[]
        for node in self.Route:
            rut = pyglet.sprite.Sprite(self.Asset_Player,
                                       int(Size/15)+Jump*node.Pos[0],
                                       int(Size/15)+Jump*node.Pos[1],
                                       batch=Bruh,group=Foreground)
            rut.scale=BkgrScale
            mtx_Path.append(rut)
            

#Main
#test

viewed, expanded,walls = [],[],[]
dimensions = [7,7]

mtxPlayer=[]
mtxPlayer.append(Player(int(BoardSize/2),0,1,imgP1,imgSlot))
mtxPlayer.append(Player(int(BoardSize/2),BoardSize-1,1,imgP2,imgSlot))
mtxPlayer.append(Player(0,int(BoardSize/2),1,imgP3,imgSlot))
mtxPlayer.append(Player(BoardSize-1,int(BoardSize/2),1,imgP4,imgSlot))

for x in mtxPlayer:
    x.DrawPlayer(imgP1)

#mtx_Path=[]
#for node in objPlayer1.TrazarRuta(expanded,viewed,walls):
##    rut = pyglet.sprite.Sprite(slotP1,
#                                           int(Size/15)+Jump*node.Pos[0],
#                                           int(Size/15)+Jump*node.Pos[1],
##                                           batch=Bruh,group=Foreground)
#    rut.scale=BkgrScale
#    mtx_Path.append(rut)
#
#for node in objPlayer2.TrazarRuta(expanded,viewed,walls):
#    rut = pyglet.sprite.Sprite(slotP2,
#                                           int(Size/15)+Jump*node.Pos[0],
 #                                          int(Size/15)+Jump*node.Pos[1],
  #                                         batch=Bruh,group=Foreground)
   # rut.scale=BkgrScale
   # mtx_Path.append(rut)

#Game = Engine(mtx_Ass)

@window.event
def on_draw():
    Bruh.draw()
    print("Dibujando")

pyglet.app.run()