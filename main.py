import pygame, random, time

from PIL import Image
from func import *
from math import *
#-----------------------Screen class' functions----------------------
def screen_init(self, name, rows, cols, fps, tetromino_size,  positions):
     pygame.init()
     
     pygame.mixer.init()
     pygame.mixer.music.load("music/Korobeiniki.wav")
     pygame.mixer.music.set_volume(0.7)
     pygame.mixer.music.play()
     
     self.tetromino_scale = 5 #Recommendation: 5; Original: 0
     self.random_tetrominoes = []
     self.tetromino_size = tetromino_size
     self.tetromino_colours = {"I":"#00ffff", "J":"#6666ff", "L":"#ffcc66", "O":"#ffff00", "S":"#66ff66","T":"#ff66ff", "Z":"#ff6666"}
     self.rows, self.cols = rows, cols
     self.w, self.h = self.size = (self.tetromino_size * rows + 1, self.tetromino_size * cols + 1)
     self.fps = fps
     self.extra_width = 500
     self.extra_height = 100
     
     
     self.screen = pygame.display.set_mode((self.w + self.extra_width + self.tetromino_size * self.tetromino_scale, self.h + self.extra_height + self.tetromino_size * self.tetromino_scale))
     pygame.display.set_caption(name)
     self.display = pygame.Surface(self.size)
     self.font = Font("small_font.png", 10)
     self.font.set_fontColor("#e9e9e9")
     block = pygame.Surface((32,32))
     block.fill(random.choice(list(self.tetromino_colours.values())))

     pygame.display.set_icon(block)
     self.clock = pygame.time.Clock()
     
     self.colours = {"black":list(pygame.Color("#" + "0"*6)), "white":list(pygame.Color("#" + "f"*6)), "grey": list(pygame.Color("#" + "56" * 3))}
     self.positions = positions
     self.mx, self.my = coord_into_tuple(list(self.positions.keys())[-1])
     self.stop = 0
     
     self.held_tetromino = None
     self.held_ticks = 0
     
     self.score = 0
     self.t = 3
     self.tick = 0
     
     
def update(self):
     """Create the cells."""
     for c,(i,j) in self.positions.items():
          pygame.draw.line(self.display, self.colours["white"] , (i,0), (i,self.h))
          pygame.draw.line(self.display, self.colours["white"] ,(0,j), (self.w,j))
          #pygame.draw.line(self.screen, (255,0,0) , (i + self.tetromino_size//2,0), (i + self.tetromino_size//2,self.h))
          #pygame.draw.line(self.screen, (255,0,0) ,(0,j + self.tetromino_size//2), (self.w,j + self.tetromino_size//2))
          x,y = coord_into_tuple(c)
          if x in (0, self.mx - 1) or y in (0, self.my - 1):
               s = pygame.Surface([self.tetromino_size]*2)
               s.fill(self.colours["grey"])
               self.display.blit(s, (i,j))
     
def get_active_coords(self, tetrominoes):
     #return [c for c, (i,j) in self.positions.items() if (coord_into_tuple(c)[0] not in (0, self.mx, self.mx - 1) and coord_into_tuple(c)[1] not in (0, self.my, self.my - 1)) and pygame.Color(self.display.get_at((i + self.tetromino_size//2,j + self.tetromino_size//2))) in map(pygame.Color, self.tetromino_colours.values()) ]            
     return [c for tetromino in tetrominoes[:-1] for c in tetromino.pixel_coords]
def hold(self, tetrominoes, events):
     """Function for blitting in the screen the pieces held."""
     name = "HOLD"
     self.font.render_text(name, self.screen, (45,10))
     if isinstance(self.held_tetromino, Tetromino):
          if self.held_ticks == 0:
               self.screen.blit(self.held_tetromino.img, (77,85))
          else:
               img = self.held_tetromino.img.copy()
               img = swap_color(img, "#464646", self.held_tetromino.colour)
               self.screen.blit(img, (77,85))
                    
     for event in events:
          if event.type == pygame.KEYUP:
               if event.key in [pygame.K_c, pygame.K_LSHIFT]:
                    if not isinstance(self.held_tetromino, Tetromino):
                         self.held_tetromino = tetrominoes[-1]
                         tetrominoes.pop(-1)
                         tetrominoes.append(Tetromino(name = random.choice(list(self.tetromino_colours.keys())),pixel_size = self.tetromino_size, positions = self.positions, coord = f"{random.randint(self.mx//2 - 2, self.mx//2 + 2)}:1"))
                         self.held_ticks = 1
                    else:
                         if not self.held_ticks:
                              self.held_ticks = 1
                              held_tetromino = self.held_tetromino
                              self.held_tetromino = tetrominoes[-1]
                              tetrominoes.pop(-1)
                              tetrominoes.append(held_tetromino)
                    self.held_tetromino.coord = self.held_tetromino.initial_coord
def next_tetrominoes(self):
     """Function for blitting the next tetrominoes in screen."""
     name = "NEXT"
     screen_width = self.screen.get_width()
     
     self.font.render_text(name, self.screen, (screen_width - 45*4 - 15, 10))     
     y = 0
     for tetromino in self.random_tetrominoes:
          self.screen.blit(tetromino.img, (screen_width - 45*4, 75*2 + y))
          y += 225
def start(self):
     dt = self.t - (time.time() - self.t0)
     if dt > 1:
          self.font.render_text(str(round(dt)),self.display, (self.display.get_width()//2 - 15, self.display.get_height()//2 - 15))
     elif dt > 0:
          self.font.render_text("GO!",self.display, (self.display.get_width()//2 - 45, self.display.get_height()//2 - 15))
     return True if dt <= 0 else False
def lose(self, active_coords):
     return True if sum(map(lambda c: coord_into_tuple(c)[1] <= 1, active_coords)) > 0 else False
def scoring(self, active_coords, tetrominoes):
     """Function for the scoring algorithm based in the classic games."""
     self.font.n_times -= 3
     self.font.render_text(f"SCORE: {self.score}", self.screen, (self.screen.get_width()//2 - 100, 2))
     self.font.n_times += 3
     target = self.rows - 2 # nº free horizontal cells
     score = {"1": 40, "2": 100, "3": 300, "4":1200}
     lines = 0
     try: 
          min_row = min(map(lambda c: coord_into_tuple(c)[1], active_coords)) 
     except: min_row = self.my - 1
     for row in list(range(min_row,self.my))[::-1]:
          n = 0
          for c in active_coords:
               cx,cy = coord_into_tuple(c)
               if cy == row: n += 1
          if n == target: 
               for t in tetrominoes[:-1]:
                    indexes = []
                    for c in t.pixel_coords:
                         cx,cy = coord_into_tuple(c)
                         if cy < row:
                              t.pixel_coords[t.pixel_coords.index(c)] = sum_coord(c, "0:1")
                         elif cy == row:
                              indexes.append(c)
                    for c in indexes:
                         t.pixel_coords.pop(t.pixel_coords.index(c))
               lines += 1    
     if lines > 0: 
          self.score += score[str(lines)]
def try_again(self, keys):
     self.font.n_times -= 5
     self.font.render_text("New Game: 'J'", self.display, (self.display.get_width()//2 - 125, self.display.get_height()//2 - 15))
     self.font.n_times += 5
     if keys[pygame.K_j]:
          main()
     
def mainloop(self,tetrominoes):
     self.t0 = time.time()
     while True:
          self.tick += 1
          self.screen.fill("#121212")
          active_coords = self.get_active_coords(tetrominoes)
          pygame.key.set_repeat(70)
          events = pygame.event.get()
          
          keys = pygame.key.get_pressed()
          
          for event in events:
               if event.type == pygame.QUIT:
                    raise SystemExit
               if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_ESCAPE, pygame.K_F1]: 
                         self.stop += 1
                         self.stop %= 2
               
          self.hold(tetrominoes, events)           
          self.next_tetrominoes()
          self.scoring(active_coords, tetrominoes)
          if not self.stop:
               self.display.fill(self.colours["black"])
               if self.lose(active_coords): self.try_again(keys)
               
               elif self.start():
                    for tetronimo in tetrominoes:
                         if tetronimo in self.random_tetrominoes: self.random_tetrominoes.pop(self.random_tetrominoes.index(tetronimo))
                         if tetronimo.alert == 1: 
                              tetrominoes.append(self.random_tetrominoes[0])
                              self.random_tetrominoes.pop(0)
                              self.random_tetrominoes.append(Tetromino(random.choice(list(self.tetromino_colours.keys())), self.tetromino_size, self.positions,f"{random.randint(self.mx//2 - 2, self.mx//2 + 2)}:1" ))
                              self.held_ticks = 0
                         tetronimo.update(events, keys, active_coords)
                         tetronimo.draw(self.display)
                    
               self.update()
               display = pygame.transform.scale(self.display, (self.w + self.tetromino_size * self.tetromino_scale, self.h + self.tetromino_size * self.tetromino_scale))
               self.screen.blit(display, (self.extra_width //2 ,self.extra_height //2))
               '''arr = pygame.surfarray.pixels3d(self.screen.copy()).transpose((1,0,2))
               img = Image.fromarray(arr)
               img.save(f"images/game{self.tick}.png")'''
               self.clock.tick(self.fps)
               pygame.display.flip()
          
Screen_class = type("Screen", (), {"__init__":screen_init, "mainloop":mainloop, "update":update, "get_active_coords": get_active_coords, "hold":hold, "next_tetrominoes": next_tetrominoes, "scoring": scoring, "lose": lose, "start": start, "try_again":try_again, })

#-----------------------Tetromino class' functions----------------------
def tetromino_init(self, name, pixel_size, positions, coord):
     self.name = name
     self.pixel_size = pixel_size
     self.part_size = [self.pixel_size] * 2
     self.parts = [pygame.Surface(self.part_size).convert_alpha()] * 4
     self.colours = {"I":"#00ffff", "J":"#6666ff", "L":"#ffcc66", "O":"#ffff00", "S":"#66ff66","T":"#ff66ff", "Z":"#ff6666"}
     self.colour = pygame.Color(self.colours[name])
     for part in self.parts:
          part.fill(self.colour)
     self.positions = positions
     self.limitX, self.limitY = map(int, list(self.positions.keys())[-1].split(":"))
     self.initial_coord = coord
     self.coord = coord
     self.pos = self.positions[coord]
     #-----The shapes of the tetrominoes
     self.shapes = {
          "I": [(i ,0) for i in range(4)],
          "J": [(i, 0) for i in range(3)] + [(0 , 1)],
          "L": [(i, 0) for i in range(3)] + [(2 , 1)],
          "O": [(i, j) for i in (0,1) for j in (0,1)],
          "S": [(i, j) for i,j in [(0,0), (1,0), (1,1), (2,1)]],
          "T": [(i, 0) for i in range(3)] + [(1 , 1)],
          "Z": [(i, j) for i,j in [(0,0), (1,0), (1,1), (2,1)]],
     }
     self.shape = self.shapes[name]
     self.width, self.height = self.size = max(map(lambda pos: pos[0] * self.pixel_size + self.pixel_size, self.shape)),max(map(lambda pos: pos[1] * self.pixel_size + self.pixel_size, self.shape)) 
     self.img = pygame.Surface(self.size)
     self.img.set_colorkey([0] * 3)
     #--Creation of the Tetromino Shape
     for idx, part in enumerate(self.parts):
          w, h = self.shape[idx]
          self.img.blit(part, (w * self.pixel_size,h * self.pixel_size))

     if self.name in "TSJL": self.img = pygame.transform.flip(self.img, False, True)
     self.speed = 1 # 1 -> 100%
     self.tick = 0
     self.movility = {
          pygame.K_LEFT: lambda c: sum_coord(c, "-1:0"),
          pygame.K_RIGHT: lambda c: sum_coord(c, "1:0"),
          pygame.K_DOWN: lambda c: sum_coord(c, "0:1"),       
     }
     self.rotate = {
          pygame.K_z: lambda img: pygame.transform.rotate(img, 90),
          pygame.K_LCTRL: lambda img: pygame.transform.rotate(img, 90),
          pygame.K_x: lambda img: pygame.transform.rotate(img, -90),
          pygame.K_UP: lambda img: pygame.transform.rotate(img, -90),
     }
     self.predicted_shadow_coords = []
     self.pixel_coords = self.get_coords(self.img)
     
     self.alert = 0
     self.play = 1
def sum_coord(c1, c2):
     return ":".join(map(str, [coord_into_tuple(c1)[i] + coord_into_tuple(c2)[i] for i in range(2)]))
def sub_coord(c1, c2):
     return ":".join(map(str, [coord_into_tuple(c1)[i] - coord_into_tuple(c2)[i] for i in range(2)]))
def coord_into_tuple(c):
     return tuple(map(int, c.split(":")))
def pos_into_coord(tup):
     return ":".join(map(str, tup))
def change_coord(c, index, num):
     return pos_into_coord([num if i == index else n for i,n in enumerate(coord_into_tuple(c))])
     
def get_part_coords(self, img):
     return {f"{x}:{y}":img.get_at((i,j)) for x,i in enumerate(range(0, img.get_width(), self.pixel_size)) for y,j in enumerate(range(0, img.get_height(), self.pixel_size)) if list(img.get_at((i,j))) == list(self.colour)}

def get_borders_coords(self):
     part_coords = self.get_part_coords(self.img)
     #self.coord is equal to the part_coord: '0:0'
     borders_coords = {}
     max_x, max_y = max(map(lambda c: coord_into_tuple(c)[0], part_coords.keys())), max(map(lambda c: coord_into_tuple(c)[1], part_coords.keys()))
     min_x, min_y = min(map(lambda c: coord_into_tuple(c)[0], part_coords.keys())), min(map(lambda c: coord_into_tuple(c)[1], part_coords.keys()))
     borders_coords["LEFT"] = [c for c in list(map(lambda c: c if coord_into_tuple(c)[0] == min_x else 0, part_coords.keys())) if type(c) == str][0]
     borders_coords["DOWN"] = [c for c in list(map(lambda c: c if coord_into_tuple(c)[1] == max_y else 0, part_coords.keys())) if type(c) == str][0]
     borders_coords["RIGHT"] = [c for c in list(map(lambda c: c if coord_into_tuple(c)[0] == max_x  else 0, part_coords.keys())) if type(c) == str][0]
     return borders_coords
def tetromino_coords(self, img):
     return [sum_coord(self.coord, c) for c in self.get_part_coords(img).keys()]

def shadow(self, screen):
     part = self.parts[0].copy()
     part.set_alpha(125)
     try: 
          for c in self.predicted_shadow_coords:
               screen.blit(part, self.positions[c])
     except: pass
     
def movement(self, events, active_coords):
     cond = 0
     for event in events:
          if event.type == pygame.KEYDOWN:
               if event.key in self.movility.keys(): 
                    coord = self.movility[event.key](self.coord)
                    for c in self.get_borders_coords().values():                         
                         x,y = coord_into_tuple(sum_coord(coord, c))
                         if sum_coord(coord, c) in active_coords or x in (0, self.limitX, self.limitX - 1) or y in (self.limitY, self.limitY - 1): cond += 1
                    if not cond: 
                         self.coord = coord
                         return True
          if event.type == pygame.KEYUP:
               if event.key == pygame.K_SPACE: 
                    if len(self.predicted_shadow_coords) > 0:
                         order = [sub_coord(self.predicted_shadow_coords[i], list(self.get_part_coords(self.img).keys())[i]) for i in range(4)]
                         min_orderX, min_orderY = min(x for x,y in map(coord_into_tuple, order)), min(y for x,y in map(coord_into_tuple, order))
                         self.coord = [pos_into_coord((x,y)) for x,y in map(coord_into_tuple,order) if x == min_orderX and y == min_orderY][0]
                         cond += 1
     if cond: return True
     
     return False
def rotation(self, events, active_coords):
     for event in events:
          if event.type == pygame.KEYUP:
               if event.key in self.rotate.keys():
                    img = self.rotate[event.key](self.img)
                    cond = 0
                    for c in self.get_part_coords(img):
                         sum_c = sum_coord(self.coord, c)
                         if sum_c in active_coords: cond += 1
                    if not cond: 
                         self.img = img
                         self.width, self.height = self.img.get_size()
                         return True
     return False
def moving_down(self, active_coords, rotate):
     coords = self.get_coords(self.img)
     cond = 0
     for c in coords:
          sum_c = self.movility[pygame.K_DOWN](c)
          cy = coord_into_tuple(sum_c)[1]
          if sum_c in active_coords or cy in (self.limitY, self.limitY - 1): cond += 1
     if not cond: 
          if self.tick % (21 - self.speed) == 0 and not rotate: self.coord = sum_coord(self.coord, "0:1")
          return True
     return False
     
def tetromino_update(self, events, keys,active_coords):
     self.tick += self.speed
     move = False
     rotate = False
     moving_down = True
     if self.play:
          #For the tetromino's movement left-right-down 
          move = self.movement(events, active_coords)
          #For the tetromino's rotation
          rotate = self.rotation(events, active_coords)
          #For moving down
          moving_down = self.moving_down(active_coords, rotate) 
               
          borders_coords = list(self.get_borders_coords().values())
          left_coord, bottom_coord, right_coord = borders_coords
          
          lx, ly = coord_into_tuple(sum_coord(left_coord, self.coord)); rx, ry = coord_into_tuple(sum_coord(right_coord, self.coord)); bx, by = coord_into_tuple(sum_coord(bottom_coord, self.coord))
          #---The limitations of the movement---
          #print((lx,ly), (rx,ry), (bx,by), self.coord)
          if lx < 1: 
               n = abs(lx-1)
               self.coord = sum_coord(self.coord, f"{n}:0")
          if rx > self.limitX - 2: 
               n = -abs(rx-(self.limitX - 2))
               self.coord = sum_coord(self.coord, f"{n}:0")
          if by > self.limitY - 2: 
               n = -abs(by-(self.limitY - 2))
               self.coord = sum_coord(self.coord, f"0:{n}")
     #--------------------------------------     
     self.pos = self.positions[self.coord]
     
     if self.play:
          
          current_coords = self.get_coords(self.img)
          self.pixel_coords = current_coords
          predicted_coords = [[sum_coord(c, f"0:{i}") if sum_coord(c, f"0:{i}") not in active_coords and not coord_into_tuple(sum_coord(c, f"0:{i}"))[1] in (self.limitY - 1, self.limitY) else None for c in current_coords] for i,n in enumerate(range(by, self.limitY + 1))]
          filter_coords = []
          for coords in predicted_coords:
               if not all(map(lambda c: c != None, coords)):
                    break
               filter_coords.append(coords)
          if len(filter_coords) > 0: self.predicted_shadow_coords = filter_coords[-1] 
          for name in self.movility.keys():
               if keys[name] and name != pygame.K_DOWN:
                    if lx != 1 and rx != self.limitX - 2: move = True
          
          if not moving_down and not move: 
               self.alert += 1
               self.play = 0
     else: self.alert += 1
          
def draw(self, screen):
     if self.play: self.shadow(screen)
     for pixel_coord in self.pixel_coords:
          screen.blit(self.parts[0], self.positions[pixel_coord])
     
Tetromino = type("Tetromino", (), {"__init__":tetromino_init, "draw": draw, "update": tetromino_update, "get_borders_coords": get_borders_coords, "movement": movement, "get_part_coords": get_part_coords,"rotation": rotation, "get_coords": tetromino_coords, "moving_down":moving_down, "shadow": shadow})


#-----------------------Main Function----------------------
def main():
     tetromino_size = 32
     rows, cols = 12, 22
     screen_size = (tetromino_size*rows + 1,tetromino_size*cols + 1)
     positions = {f"{x}:{y}":(i,j) for x,i in enumerate(range(0, screen_size[0], tetromino_size)) for y,j in enumerate(range(0,screen_size[1], tetromino_size))}
     
     screen = Screen_class(name = "Tetris", rows = rows, cols = cols, fps = 30, tetromino_size =  tetromino_size, positions = positions)
     names = "IJLOSTZ"
     tetrominoes = [Tetromino(name = random.choice(names),pixel_size = tetromino_size, positions = positions, coord = f"{random.randint(screen.mx//2 - 2, screen.mx//2 + 2)}:1")]
     screen.random_tetrominoes += tetrominoes
     screen.random_tetrominoes += [Tetromino(name = random.choice(names),pixel_size = tetromino_size, positions = positions, coord = f"{random.randint(screen.mx//2 - 2, screen.mx//2 + 2)}:1") for i in range(4)]
     #random.choice(names)
     screen.mainloop(tetrominoes)
     
if __name__ == "__main__":
     main()