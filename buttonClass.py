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

    def draw_button(self,screen, txt = ''):
        font = pygame.font.SysFont("Arial Black", 13)
        pygame.draw.rect(screen,self.clr,self.box)
        # if there is an img, blit img
        if self.img:
            screen.blit(self.img,(self.x,self.y))
        # if there is txt, blit txt
        if txt != '':
            text = font.render(txt, 1, (255,255,255))
            screen.blit(text,(self.x+5,self.y+2))

    
    def click_button(self,mx,my, ownLogic = ''):
        # if click button, button is used and change button colour
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