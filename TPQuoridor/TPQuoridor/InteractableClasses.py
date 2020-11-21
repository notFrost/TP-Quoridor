from Pathfinders import *

#Configurar Engine Renderer
Bruh=pyglet.graphics.Batch()
Background = pyglet.graphics.OrderedGroup(0)
BoardObj = pyglet.graphics.OrderedGroup(1)
Foreground = pyglet.graphics.OrderedGroup(2)
Walls = pyglet.graphics.OrderedGroup(4)
Players = pyglet.graphics.OrderedGroup(3)

class Wall:
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def evaluate_wall_placement():

        pass


class Player:
    def __init__(self,initial_coords,goal_coords,color,AssCol,AssPath):
        self.X=initial_coords[0]
        self.Y=initial_coords[1]
        self.MetaX=goal_coords[0]
        self.MetaY=goal_coords[1]
        self.Order=color
        self.Asset_Player=AssCol
        self.Asset_Path=AssPath
        self.Sprite=False
        self.mtx_Path=False
        self.Change=True
        self.generate_sprite()
        
    def generate_sprite(self):
        self.Sprite=pyglet.sprite.Sprite(self.Asset_Player,
                             BOARD_BORDER+JUMP*self.X,
                             BOARD_BORDER+JUMP*self.Y,
                             batch=Bruh,group=Players)
        self.Sprite.scale=SLOT_SCALE

    def generate_route(self,expanded,viewed,walls):
        self.Route=Routing((self.X,self.Y),expanded,viewed,walls,(self.MetaX,self.MetaY))
        self.Change=True
        return self.Route

    def show_route(self):
        if(self.Change):
            self.mtx_Path=[]
            for node in self.Route:
                rut = pyglet.sprite.Sprite(self.Asset_Path,
                                            BOARD_BORDER+JUMP*node.Pos[0],
                                            BOARD_BORDER+JUMP*node.Pos[1],
                                            batch=Bruh,group=Foreground)
                rut.scale=SLOT_SCALE
                self.mtx_Path.append(rut)
            self.Change=False
        
            