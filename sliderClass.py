import pygame
class Slider():
    def __init__(self, left, top, width, clr):
        self.left = left
        self.top = top
        self.clr = clr
        self.radius = 8
        self.width = width
        self.mx = self.left

    def draw_slider(self,screen, height):
        pygame.draw.rect(screen,self.clr,(self.left,self.top, self.width, height))
        pygame.draw.circle(screen,(255,255,255), (self.mx,self.top+height/2), self.radius, 2)

        self.hitbox = pygame.Rect(self.mx-self.radius, (self.top+height/2) - self.radius, self.radius * 2, self.radius * 2)
    
    def detect_mouse(self,mouseIsDown, mx, my):
        if mouseIsDown and self.hitbox.collidepoint(mx,my):
            self.mx = mx
            if self.mx < self.left:
                self.mx = self.left
            elif self.mx > self.left + self.width:
                self.mx = self.left + self.width
    
    def change_clr(self):
        self.proportion = self.width / 255
        increase = (self.mx - self.left) / self.proportion
        return increase

        
    def set_clr(self,RGB_value):
        self.mx = RGB_value * self.proportion + self.left


