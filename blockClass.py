import pygame
pygame.init()
class Square():
    def __init__(self,row,col,clr, screen, size):
        self.row = row
        self.col = col
        self.clr = clr
        self.screen = screen
        self.size = size
        self.square = pygame.Rect((self.col * self.size, self.row * self.size), (self.size, self.size))
    
    def draw_block(self):
        if self.clr != (255,255,255):
            pygame.draw.rect(self.screen, self.clr, self.square)