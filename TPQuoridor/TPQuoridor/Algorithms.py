# A* Algorithm
def Astar(expanded, viewed, walls, end):
    curr = viewed[0]
    if curr.Pos == end:
        expanded.append(curr)
        print('End encontrado')
        return finish(curr)
    # Cardinal Verification
    Nb = []
    for i in [-1, 1]:
        Nb.append((curr.Pos[0], curr.Pos[1] + i))
        Nb.append((curr.Pos[0] + i, curr.Pos[1]))
    for next in Nb:
        # To do: Añadir implementacion de CheckWalls()
        if CheckPrev(curr, next) and CheckBorder(next) and CheckArr(expanded, next) and CheckArr(viewed,
                                                                                                 next) and CheckWalls(
                walls, curr, next):
            viewed.append(Node(next, curr, end))
    # Add to expanded and Sort new Viewed List
    expanded.append(curr)
    viewed.pop(0)
    viewed.sort(key=CheckF)
    # Possibility Verification
    if viewed:
        return Astar(expanded, viewed, walls, end)
    else:
        return False


# BFS ALGORITHM
def BFS(expanded, viewed, walls, end):
    if viewed[0].Pos == end:
        expanded.append(viewed[0])
        print('End encontrado')
        return finishA(viewed[0])
    # Cardinal Verification
    Nb = []
    for i in [-1, 1]:
        Nb.append((viewed[0].Pos[0], viewed[0].Pos[1] + i))
        Nb.append((viewed[0].Pos[0] + i, viewed[0].Pos[1]))
    for next in Nb:
        # To do: Añadir implementacion de CheckWalls()
        if CheckPrev(viewed[0], next) and CheckBorder(next) and CheckArr(expanded, next) and CheckArr(viewed, next):
            viewed.append(NodeA(next, viewed[0]))

    # Add to expanded and Sort new Viewed List
    expanded.append(viewed[0])
    viewed.pop(0)
    # Possibility Verification
    if viewed:
        return BFS(expanded, viewed, walls, end)
    else:
        return False


# DFS ALGORITHM
def DFS(checked, curr, walls, end):
    # Cardinal Verification
    if curr.Pos == end:
        finishA(curr)
        return True
    checked.append(curr)
    Nb = []
    for i in [-1, 1]:
        Nb.append((curr.Pos[0], curr.Pos[1] + i))
        Nb.append((curr.Pos[0] + i, curr.Pos[1]))
    for next in Nb:
        # To do: Añadir implementacion de CheckWalls()
        if CheckBorder(next) and CheckArr(checked, next):
            if DFS(checked, NodeA(next, curr), walls, end):
                return True
    return False