import pygame
class Button():
    def __init__(self,x,y,w,h,img = None, isUsed=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = img
        self.box = pygame.Rect(x,y,w,h)
        self.clr = (40,40,45)
        self.isUsed = isUsed

    def draw_button(self,screen):
        pygame.draw.rect(screen,self.clr,self.box)
        if self.img:
            screen.blit(self.img,(self.x,self.y))
    
    def click_button(self,mx,my, ownLogic = ''):
        if self.box.collidepoint(mx,my):
            if ownLogic == '':
                self.clr = (90,90,95)
                self.isUsed = True
            return True

    def deactivate_others(self, listOfButtons):
        #make booleans of other buttons false and reset colour
        for button in listOfButtons:
            if button != self and button.isUsed:
                button.clr = (40,40,45)
                button.isUsed = False