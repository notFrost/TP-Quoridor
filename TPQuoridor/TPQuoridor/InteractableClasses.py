from Pathfinders import *

class Wall:
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def evaluate_wall_placement():

        pass


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
                             BOARD_BORDER+JUMP*self.X,
                             BOARD_BORDER+JUMP*self.Y,
                             batch=Bruh,group=Foreground)
        pass

    def ShowPath(self):
        mtx_Path=[]
        for node in self.Route:
            rut = pyglet.sprite.Sprite(self.Asset_Player,
                                       BOARD_BORDER+JUMP*node.Pos[0],
                                       BOARD_BORDER+JUMP*node.Pos[1],
                                       batch=Bruh,group=Foreground)
            rut.scale=BACKGROUND_SCALE
            mtx_Path.append(rut)
            