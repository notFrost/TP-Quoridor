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
        self.wall_sprite_array=[]
        self.wall_array={}
        self.wall_shadow=False
        self.shadow_pos=(0,0)
        self.img_wall=wall_img
        self.img_shadow_wall=shadow_wall_img
    

    def place_wall(self,Px,Py):
        wall=pyglet.sprite.Sprite(  BOARD_BORDER+JUMP*Px,
                                    BOARD_BORDER+JUMP*Py,
                                    self.img_wall,
                                    batch=Bruh,group=Walls)
        wall.rotation=self.wall_shadow.rotation
        self.wall_sprite_array.append(wall)

    def delete_this(self):
        self.wall_shadow.delete()
        self.wall_shadow=False

    def rotate_wall(self):
        if self.wall_shadow.rotation==0:
            self.wall_shadow.rotation=90
        else: 
            self.wall_shadow.rotation=0
        self.refresh_shadow_pos()

    def check_valid_placement(self,Bx,By):
        if (self.wall_shadow.rotation==90):
            node_coord_1=(Bx,By)
            node_coord_1_end=(Bx,By+1)
            node_coord_2=(Bx+1,By)
            node_coord_2_end=(Bx+1,By+1)
        else:
            node_coord_1=(Bx,By)
            node_coord_1_end=(Bx+1,By)
            node_coord_2=(Bx,By+1)
            node_coord_2_end=(Bx+1,By+1)

        if node_coord_1 not in self.wall_array:
            return True
        else:
            if node_coord_2 not in self.wall_array[node_coord_1]:
                return True
            else:
                return False

    def fix_shadow_position(self,Mx,My):
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
        Bx=min(x_limit,max(x_ini,Mx))
        By=min(y_limit,max(y_ini,My))
        if self.check_valid_placement(Bx,By):
            print("X: "+str(Bx)+", Y: "+str(By))
            return True,Bx,By
        else:
            return False

    def refresh_shadow_pos(self,*args):
        if args:
            self.last_mouse=args
            Mx=int((args[0]-BOARD_BORDER)//JUMP)
            My=int((args[1]-BOARD_BORDER)//JUMP)
        else:
            Mx=int((self.last_mouse[0]-BOARD_BORDER)//JUMP)
            My=int((self.last_mouse[1]-BOARD_BORDER)//JUMP)

        if(self.wall_shadow):
            #print("X: "+str(Mx)+", Y: "+str(My))
            log=self.fix_shadow_position(Mx,My)
            if log[0]:
                self.wall_shadow.x=BOARD_BORDER+JUMP*log[1]
                self.wall_shadow.y=BOARD_BORDER+JUMP*log[2]
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
        
            