from GameSettings import *

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
  def __init__(self, pos, pre, end,dir):
    self.Pos = pos
    self.prev = pre
    if self.prev!=False:
      self.G = self.prev.G+1
    else:
      self.G = 0
    self.F = self.calcf(end,dir)

  def calcf(self, end,dir):
    h = abs(self.Pos[dir]-end)
    return h+self.G

#Checking Functions ##Tenemos que conseguir dimensions de algun lugar, esta en lectura de .txt
def CheckMove(curr,Expa,View,Walls,next):
    pass

def CheckBorder(Pos):
  if (Pos[0]>=0 and Pos[0]<BOARD_SIZE) and (Pos[1]>=0 and Pos[1]<BOARD_SIZE):
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

def CheckWalls(walls,curr,next):
    if next>curr:
        next,curr=curr,next
    if curr in walls:
        if next in walls[curr]:
            return False
    return True

def CheckF(Nod):
  return Nod.F

def Routing(start,expanded,viewed,walls,end,dir):
    Aux=Node(start, False, end,dir)
    viewed.append(Aux)
    return Astar(expanded, viewed, walls, end,dir)

#A* Algorithm
def Astar(expanded, viewed, walls, end,dir):
    curr = viewed[0]
    if curr.Pos[dir]==end:
        expanded.append(curr)
        #print('End encontrado')
        return finish(curr)
    #Cardinal Verification
    Nb = []
    for i in [-1,1]:
        Nb.append((curr.Pos[0],curr.Pos[1]+i))
        Nb.append((curr.Pos[0]+i,curr.Pos[1]))
    for next in Nb:
        if CheckPrev(curr,next) and CheckBorder(next) and CheckArr(expanded,next) and CheckArr(viewed,next) and CheckWalls(walls,curr.Pos,next):
            viewed.append(Node(next,curr, end,dir))
    #Add to expanded and Sort new Viewed List
    expanded.append(curr)
    viewed.pop(0)
    viewed.sort(key=CheckF)
    #Possibility Verification
    if viewed:
        return Astar(expanded, viewed, walls, end,dir)
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