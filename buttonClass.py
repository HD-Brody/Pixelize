import pygame
class Button():
    def __init__(self,x,y,w,h,img = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.box = pygame.Rect(x,y,w,h)
        self.clr = (40,40,45)

    def draw_button(self,screen):
        pygame.draw.rect(screen,self.clr,self.box)
        screen.blit(self.img,(self.x,self.y))
    
    def click_button(self,mx,my):
        if self.box.collidepoint(mx,my):
            self.clr = (90,90,95)
            return True
    
    def clear_button(self):
        self.clr = (40,40,45)