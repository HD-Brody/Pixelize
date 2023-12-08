import pygame
pygame.init()
class Square():
    def __init__(self,row,col,clr, screen, size):
        self.row = row
        self.col = col
        self.clr = clr
        self.screen = screen
        self.square = pygame.Rect((self.col * size, self.row * size), (size, size))
    
    def draw_block(self):
        pygame.draw.rect(self.screen, self.clr, self.square)