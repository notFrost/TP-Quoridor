from Pathfinders import *

#Configurar Engine Renderer
Bruh=pyglet.graphics.Batch()
OutOfBounds=pyglet.graphics.OrderedGroup(0)
Background = pyglet.graphics.OrderedGroup(1)
BoardObj = pyglet.graphics.OrderedGroup(2)
Foreground = pyglet.graphics.OrderedGroup(3)
Players = pyglet.graphics.OrderedGroup(4)
Walls = pyglet.graphics.OrderedGroup(5)
Cursorobj = pyglet.graphics.OrderedGroup(6)

class WallArray:
    def __init__(self,wall_img,shadow_wall_img):
        self.wall_sprite_array=[]
        self.wall_array={}
        self.wall_shadow=False
        self.shadow_pos=(0,0)
        self.img_wall=wall_img
        self.img_shadow_wall=shadow_wall_img
    
    def command_manager(self,key):
        """
        DESIGNACION DE LOS COMANDOS PARA PAREDES
        1   -> Enable_Shadow, Habilita el overlay para colocar una pared
        2   -> Rotate_Wall, Rota la pared y actualiza su posicion
        3   -> Place_Wall, Agrega la pared al arreglo existente y la dibuja
        """
        if key==1:
            if self.enable_shadow():
                print("Se habilito la sombra")
        elif key==2:
            if self.rotate_wall():
                print("Se roto la sombra")
        elif key==3:
            if self.place_wall():
                print(self.wall_array)
                print("Se guardo pared")
            else:
                print("Guardado incorrecto")

    def enable_shadow(self):
        self.wall_shadow=pyglet.sprite.Sprite(self.img_shadow_wall,0,0,batch=Bruh,group=OutOfBounds)
        self.wall_shadow.scale=SLOT_SCALE

    def rotate_wall(self):
        if self.wall_shadow.rotation==0:
            self.wall_shadow.rotation=90
            if not self.refresh_shadow_pos():
                self.wall_shadow.rotation=0
                return False    
        else:
            self.wall_shadow.rotation=0
            if not self.refresh_shadow_pos():
                self.wall_shadow.rotation=90
                return False    
        return True

    def place_wall(self):
        if self.shadow_pos == (0,0):
            return False
        c1,c1_end,c2,c2_end=self.__create_coords(self.shadow_pos[0],self.shadow_pos[1])
        self.save_wall(c1,c1_end)
        self.save_wall(c2,c2_end)
        for c in [c1,c2]:
            wall=pyglet.sprite.Sprite(  self.img_wall,
                                        BOARD_BORDER+JUMP*c[0],
                                        BOARD_BORDER+JUMP*c[1],
                                        batch=Bruh,group=Walls)
            wall.scale=SLOT_SCALE
            wall.rotation=self.wall_shadow.rotation
            self.wall_sprite_array.append(wall)
        self.wall_shadow.delete()
        self.wall_shadow=False
        self.shadow_pos=(0,0)
        return True


    def save_wall(self,coord,coord_end):
        if coord not in self.wall_array:
            self.wall_array[coord]=[]
        self.wall_array[coord].append(coord_end)
        return True

    def refresh_shadow_pos(self,*args):
        """
        Puede ser usada:
        -Agregando la posicion X e Y del raton a los argumentos
        -Sin argumentos (usara los de la ultima llamada con argumentos o (0,0)
        """
        if args:
            self.last_mouse=args
            Mx=int((args[0]-BOARD_BORDER)//JUMP)
            My=int((args[1]-BOARD_BORDER)//JUMP)
            if (Mx,My)==self.shadow_pos:
                print("No hay cambio")
                return False
        else:
            Mx=int((self.last_mouse[0]-BOARD_BORDER)//JUMP)
            My=int((self.last_mouse[1]-BOARD_BORDER)//JUMP)

        
        pos=self.__fix_shadow_position(Mx,My)
        if type(pos)!=bool:
            if self.wall_shadow.group==OutOfBounds:
                self.wall_shadow.group=Cursorobj
            self.wall_shadow.x=BOARD_BORDER+JUMP*pos[0]
            self.wall_shadow.y=BOARD_BORDER+JUMP*pos[1]
            self.shadow_pos=(pos[0],pos[1])
            print("SI HAY CAMBIO")
            return True
        return False

    def __fix_shadow_position(self,Mx,My):
        """
        AJUSTA A LA SOMBRA DENTRO DE LOS LIMITES PERMITIDOS Y EVITA COLOCAR SOBRE PAREDES
        """
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
        if self.__check_valid_placement(Bx,By):
            return Bx,By
        else:
            return False      

    def __check_valid_placement(self,Bx,By):
        c1,c1_end,c2,c2_end=self.__create_coords(Bx,By)
        #print([c1,c1_end,c2,c2_end])
        #print(self.wall_array)
        if self.__check_array(c1,c1_end) and self.__check_array(c2,c2_end):
            return True
        else:
            return False

    def __check_array(self,coord,coord_end):
        if coord in self.wall_array:
            if coord_end in self.wall_array[coord]:
                print("CONFLICTO")
                return False
        return True

    def __create_coords(self,Bx,By):
        """
        GENERA LAS COORDENADAS DE AMBOS CUADROS PARA LA PARED
        Coloca la menor coordenada a la derecha de cada tupla
        Output: (coord1),(coord1_end),(coord2),(coord2_end)
        """
        if (self.wall_shadow.rotation==90):
            return (Bx,By),(Bx,By-1),(Bx+1,By),(Bx+1,By-1)
        else:
            return (Bx,By),(Bx-1,By),(Bx,By+1),(Bx-1,By+1)

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
            for e in self.mtx_Path:
                e.delete()
            for node in self.Route:
                rut = pyglet.sprite.Sprite(self.Asset_Path,
                                            BOARD_BORDER+JUMP*node.Pos[0],
                                            BOARD_BORDER+JUMP*node.Pos[1],
                                            batch=Bruh,group=Foreground)
                rut.scale=SLOT_SCALE
                self.mtx_Path.append(rut)
            self.Change=False