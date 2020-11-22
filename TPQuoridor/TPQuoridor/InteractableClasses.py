from Pathfinders import *

#Configurar Engine Renderer
Bruh=pyglet.graphics.Batch()
Background = pyglet.graphics.OrderedGroup(0)
BoardObj = pyglet.graphics.OrderedGroup(1)
Foreground = pyglet.graphics.OrderedGroup(2)
Walls = pyglet.graphics.OrderedGroup(4)
Players = pyglet.graphics.OrderedGroup(3)

class WallArray:
    def __init__(self,wall_img,shadow_wall_img):
        self.wall_array={}
        self.wall_shadow=False
        self.img_wall=wall_img
        self.img_shadow_wall=shadow_wall_img

    #Agrega una pared de 1x1 al diccionario, retorna falso si la pared ya existe
    def insert_wall(self,node_coord_1,node_coord_2):
        if node_coord_1 in self.wall_array:
            if node_coord_2 in self.wall_array[node_coord_1]:
                return False
            else:
                self.wall_array[node_coord_1].append(node_coord_2)
                return True
        else:
            self.wall_array[node_coord_1]=[node_coord_2]
            return True

    def insert_wall2(self,Px,Py):
        self.wall_shadow.x=BOARD_BORDER+JUMP*Px
        self.wall_shadow.y=BOARD_BORDER+JUMP*Py

    def delete_this(self):
        self.wall_shadow.delete()
        self.wall_shadow=False

    def rotate_wall(self):
        if self.wall_shadow.rotation==0:
            self.wall_shadow.rotation=90
        else: 
            self.wall_shadow.rotation=0

    def check_valid_placement(self,Bx,By):
        self.wall_shadow.x=BOARD_BORDER+JUMP*Bx
        self.wall_shadow.y=BOARD_BORDER+JUMP*By
        print("X: "+str(Bx)+", Y: "+str(By))
        pass

    def wall_axis_adjuster(self,Mx,My,xini,yini,xlim,ylim):
        Bx=min(xlim,max(xini,Mx))
        By=min(ylim,max(yini,My))
        return self.check_valid_placement(Bx,By)

    def evaluate_wall_placement(self,Mx,My):
        if(self.wall_shadow):
            if(Mx>BOARD_BORDER and My>BOARD_BORDER):
                Mx=int((Mx-BOARD_BORDER)//JUMP)
                My=int((My-BOARD_BORDER)//JUMP)
                if(self.wall_shadow):
                    if(self.wall_shadow.rotation==90):
                        x_ini=0
                        y_ini=1
                        x_limit=BOARD_SIZE-2
                        y_limit=BOARD_SIZE-1
                    else:
                        x_ini=1
                        y_ini=0
                        x_limit=BOARD_SIZE-1
                        y_limit=BOARD_SIZE-2
                    return self.wall_axis_adjuster(Mx,My,x_ini,y_ini,x_limit,y_limit) 
            else:
                return False
        else:
            return False
    def show_shadow_wall(self):
        self.wall_shadow=pyglet.sprite.Sprite(self.img_shadow_wall,0,0,batch=Bruh,group=Walls)
        self.wall_shadow.scale=SLOT_SCALE

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
        
            