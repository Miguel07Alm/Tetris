import pygame, string
import binary as bin
global colorkey, color,white, black
colorkey = [0] * 3
color = [255] + [0] * 2
white = [255, 43,54]
black = [51, 91, 93]
def swap_color(obj_img,newColor, oldColor):
    obj_img.set_colorkey(pygame.Color(oldColor))
    surf = obj_img.copy()
    surf.fill(pygame.Color(newColor))
    surf.blit(obj_img,(0,0))
    surf.set_colorkey(colorkey)
    return surf

def clip(surf,x,y,width,height):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,width,height)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

def rgb_to_hex(rgb):
    return "#" + "".join(str(bin.dec_to_hex(x)) if len(str(bin.dec_to_hex(x))) == 2 else "0" + str(bin.dec_to_hex(x)) for idx,x in enumerate(rgb) if idx < 3)
def hex_to_rgb(hex):
    hex = hex.lstrip("#")
    hex = "".join(x.rjust(2) if idx % 2 == 0 else x for idx,x in enumerate(hex)).split(" ")[1:]
    return list(bin.hex_to_dec(x) for x in hex)
class Font:
    def __init__(self, fontsheet_name, n_times = 1):
        self.fontsheet = pygame.image.load(fontsheet_name).convert_alpha()
        self.line_height = self.fontsheet.get_height()
        self.n_times = n_times
        
        
        self.sepColor = hex_to_rgb("#7f7f7f")
        self.fontOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';','%', "|"]
        
        self.baseSpacing = 1
        self.lineSpacing = 2
        self.letter_spacing = []
        
        self.letters = self.get_letters(self.fontsheet)
        self.lettersImgs= {self.fontOrder[idx]:self.letters[idx] for idx in range(len(self.fontOrder))}
        self.fontColor = [255,0,0]
        self.targetColor = "#000012"
        
        self.space_width = self.letter_spacing[0]
        for letter in self.fontOrder:
            self.lettersImgs[letter] = swap_color(self.lettersImgs[letter], pygame.Color(self.targetColor), self.fontColor)
        
        self.fontColor = hex_to_rgb(self.targetColor)
    def width(self, text):
        return sum(self.space_width + self.baseSpacing if char == ' ' else self.letter_spacing[self.fontOrder.index(char)] + self.baseSpacing for char in text)
    def text_len(self,text):
        return self.lettersImgs["a"].get_size()[0] * self.n_times * len(text)
    def set_fontColor(self, color):
        if type(self.fontColor) == str:
            self.fontColor = hex_to_rgb(self.fontColor)
        if rgb_to_hex(self.fontColor) != color and self.fontColor != color:
            for char in self.lettersImgs.keys():
                self.lettersImgs[char] = swap_color(self.lettersImgs[char], pygame.Color(color), self.fontColor)
            self.fontColor = color
    def get_letters(self, fontSheet):
        letters = []
        x = 0
        dx = 0
        for x in range(fontSheet.get_width()):
            if fontSheet.get_at((x, 0))[0] == 127:
                letters.append(clip(fontSheet, dx, 0, x - dx, self.line_height))
                self.letter_spacing.append(x - dx)
                dx = x + 1
            x += 1
        return letters
    
    def render_text(self,text, render, loc,line_width=0):
        """ Function which you can render your text without any restriction """
        x_offset = 0
        y_offset = 0
        if line_width != 0:
            spaces = []
            x = 0
            for i, char in enumerate(text):
                if char == ' ':
                    spaces.append((x, i))
                    x += self.space_width + self.baseSpacing
                else:
                    x += self.letter_spacing[self.fontOrder.index(char)] + self.baseSpacing
            line_offset = 0
            for i, space in enumerate(spaces):
                if (space[0] - line_offset) > line_width:
                    line_offset += spaces[i - 1][0] - line_offset
                    if i != 0:
                        text = text[:spaces[i - 1][1]] + '\n' + text[spaces[i - 1][1] + 1:]
        for i,char in enumerate(text):
            if char not in ['\n', ' ']:
                char_img = pygame.transform.scale(self.lettersImgs[char], (self.lettersImgs[char].get_width() * self.n_times,self.lettersImgs[char].get_height() * self.n_times))
                char_img.set_colorkey((0,0,0))
                render.blit(char_img, (loc[0] + x_offset * self.n_times, loc[1] + y_offset * self.n_times))
                x_offset += self.letter_spacing[self.fontOrder.index(char)] + self.baseSpacing
            elif char == ' ':
                x_offset += self.space_width + self.baseSpacing
            else:
                y_offset += self.lineSpacing + self.line_height
                x_offset = 0
