import pygame
class Slider():
    def __init__(self, left, top, width, clr, radius = 8):
        self.left = left
        self.top = top
        self.clr = clr
        self.radius = radius
        self.width = width
        self.mx = self.left

    def draw_slider(self,screen, height, circleClr = (255,255,255), thickness = 2):
        pygame.draw.rect(screen,self.clr,(self.left,self.top, self.width, height))
        pygame.draw.circle(screen,circleClr, (self.mx,self.top+height/2), self.radius, thickness)

        self.hitbox = pygame.Rect(self.mx-self.radius, (self.top+height/2) - self.radius, self.radius * 2, self.radius * 2)
    
    def detect_mouse(self,mouseIsDown, mx, my):
        if mouseIsDown and self.hitbox.collidepoint(mx,my):
            self.mx = mx
            if self.mx < self.left:
                self.mx = self.left
            elif self.mx > self.left + self.width:
                self.mx = self.left + self.width
    
    def change_clr(self, size = 255):
        #set proportion between slider width and 255(rgb max value)
        self.proportion = self.width / size
        increase = (self.mx - self.left) / self.proportion
        return increase

    def set_clr(self,RGB_value):
        self.mx = RGB_value * self.proportion + self.left


