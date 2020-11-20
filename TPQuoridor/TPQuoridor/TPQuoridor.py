import pyglet
import pyglet.image as pyi
import os

#Generacion de la ventana
Size = 1000
BoardSize=100
window = pyglet.window.Window(width=Size,height=Size)

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
Players = pyglet.graphics.OrderedGroup(3)

BkgrScale = Size/imgBoard.width
BoardScale=BkgrScale
SlotScale = BkgrScale*(9/BoardSize)
Jump = imgSlot.width*SlotScale

class Engine:
    def __init__(self,Ass_List):
        self.mtxAssets = Ass_List
        self.imgBank = []
        self.SpriteBank = []
        self.SpritePlayer = []
        self.ArrPlayer = []
        self.ArrPathing = []
        self.LoadAssets()
        self.viewed, self.expanded,self.walls = [],[],[]
        self.LoadEnv()
        self.GeneratePlayers(4)
        self.DrawPlayers()
        self.ShowPath()

    def LoadAssets(self):
        for x in self.mtxAssets:
            self.imgBank.append(pyi.load(x))
        pass

    def LoadEnv(self):
        Board=pyglet.sprite.Sprite(self.imgBank[0],batch=Bruh,group=Background)
        print("Tablero Cargado")
        Board.scale=BkgrScale
        self.SpriteBank.append(Board)

        for x in range(BoardSize):
            for y in range(BoardSize):
                Slot = pyglet.sprite.Sprite(self.imgBank[1],
                                            int(Size/15)+Jump*x,
                                            int(Size/15)+Jump*y,
                                            batch=Bruh,group=BoardObj
                                            )
                Slot.scale=SlotScale
                self.SpriteBank.append(Slot)
        pass

    def GeneratePlayers(self,Nplay):
        self.ArrPlayer.append(Player(int(BoardSize/2)-3,0,
                                     int(BoardSize/2),BoardSize-1,
                                     0,self.imgBank[3],self.imgBank[7]))

        self.ArrPlayer.append(Player(int(BoardSize/2)+3,BoardSize-1,
                                     int(BoardSize/2),0,
                                     1,self.imgBank[4],self.imgBank[8]))

        self.ArrPlayer.append(Player(0,int(BoardSize/2)-5,
                                     BoardSize-1,int(BoardSize/2),
                                     2,self.imgBank[5],self.imgBank[9]))

        self.ArrPlayer.append(Player(BoardSize-1,int(BoardSize/2)+7,
                                     0,int(BoardSize/2),
                                     3,self.imgBank[6],self.imgBank[10]))
        pass

    def DrawPlayers(self):
        for x in self.ArrPlayer:
            a=pyglet.sprite.Sprite(self.imgBank[3+x.Order],
                             int(Size/15)+Jump*x.X,
                             int(Size/15)+Jump*x.Y,
                             batch=Bruh,group=Players)
            a.scale=SlotScale
            self.SpritePlayer.append(a)
    
    def ShowPath(self):
        for x in range(4):
            for node in self.ArrPlayer[x].TrazarRuta(self.expanded,self.viewed,self.walls):
                rut = pyglet.sprite.Sprite(self.imgBank[7+x],
                                           int(Size/15)+Jump*node.Pos[0],
                                           int(Size/15)+Jump*node.Pos[1],
                                           batch=Bruh,group=Foreground
                                           )
                rut.scale=SlotScale
                self.ArrPathing.append(rut)
                self.viewed,self.expanded = [],[]

def finish(Node):
  Recorrido = []
  #recorre expanded desde el nodo end hasta que el nodo que estemos tenga como prev "start"
  while Node.prev != False:
    Recorrido.append(Node)
    Node = Node.prev
  Recorrido.append(Node)
  Recorrido.reverse()
  return Recorrido

def finishA(Node):
  #recorre expanded desde el nodo end hasta que el nodo que estemos tenga como prev "start"
  while Node.prev != False:
    Recorrido.append(Node)
    Node = Node.prev
  Recorrido.append(Node)
  return Recorrido

#Node para DFS/BFS
class NodeA:
  def __init__(self, pos, pre):
    self.Pos = pos
    self.prev = pre

#Node para A*
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
def CheckMove(curr,Expa,View,Walls,next):
    pass

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

def CheckWalls(arr,curr,next):
    for i in  arr:
        if i==[curr.Pos,next] or i==[next,curr.Pos]:
            return False
    return True

def CheckF(Nod):
  return Nod.F

def Routing(start,expanded,viewed,walls,end):
    Aux=Node(start, False, end)
    viewed.append(Aux)
    return Astar(expanded, viewed, walls, end)

#A* Algorithm
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
    if CheckPrev(curr,next) and CheckBorder(next) and CheckArr(expanded,next) and CheckArr(viewed,next) and CheckWalls(walls,curr,next):
      viewed.append(Node(next,curr, end))
  #Add to expanded and Sort new Viewed List
  expanded.append(curr)
  viewed.pop(0)
  viewed.sort(key=CheckF)
  #Possibility Verification
  if viewed:
    return Astar(expanded, viewed, walls, end)
  else:
    return False
 
#BFS ALGORITHM
def BFS (expanded, viewed, walls, end):
  if viewed[0].Pos == end:
    expanded.append(viewed[0])
    print('End encontrado')
    return finishA(viewed[0])
  #Cardinal Verification
  Nb = []
  for i in [-1,1]:
    Nb.append((viewed[0].Pos[0],viewed[0].Pos[1]+i))
    Nb.append((viewed[0].Pos[0]+i,viewed[0].Pos[1]))
  for next in Nb:
    #To do: Añadir implementacion de CheckWalls()
    if CheckPrev(viewed[0],next) and CheckBorder(next) and CheckArr(expanded,next) and CheckArr(viewed,next):
      viewed.append(NodeA(next,viewed[0]))

  #Add to expanded and Sort new Viewed List
  expanded.append(viewed[0])
  viewed.pop(0)
  #Possibility Verification
  if viewed:
    return BFS(expanded, viewed, walls, end)
  else:
    return False

#DFS ALGORITHM
def DFS (checked, curr, walls, end):
  #Cardinal Verification
  if curr.Pos == end:
    finishA(curr)
    return True
  checked.append(curr)
  Nb = []
  for i in [-1,1]:
    Nb.append((curr.Pos[0],curr.Pos[1]+i))
    Nb.append((curr.Pos[0]+i,curr.Pos[1]))
  for next in Nb:
    #To do: Añadir implementacion de CheckWalls()
    if CheckBorder(next) and CheckArr(checked,next):
      if DFS(checked, NodeA(next, curr), walls, end):
        return True
  return False

class Player:
    def __init__(self,x,y,Ex,Ey,color,AssCol,AssPath):
        self.X=x
        self.Y=y
        self.MetaX=Ex
        self.MetaY=Ey
        self.Order=color
        self.Asset_Player=AssCol
        self.Asset_Path=AssPath

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
            
#test
dimensions = [7,7]
start = [4,6]
end = (2,0)

#Main
viewed, expanded, walls, Recorrido = [],[],[], []
viewed.append(NodeA((start[0],start[1]), False))
BFS(expanded, viewed, walls, end)
print("BFS: ")
for x in Recorrido:
  print(x.Pos,end='')
print()

viewed, walls, Recorrido = [],[],[]
print("DFS: ")
DFS(viewed, NodeA((start[0],start[1]), False), walls, end)
for x in Recorrido:
  print(x.Pos,end='')
print()

Game = Engine(Assets)

@window.event
def on_draw():
    Bruh.draw()
    print("Dibujando")

pyglet.app.run()