import sys
import random
import time
import pygame
from blockClass import *
from buttonClass import *
from sliderClass import *
from queueClass import *
pygame.init()
from pygame.locals import QUIT

print(sys.getrecursionlimit())
sys.setrecursionlimit(1500)

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GRAY = (40,40,45)

clock = pygame.time.Clock()
framerate = 1000

###### IMAGES ######
pencilimg = pygame.image.load('Photoshop\pencil.png')
pencilimg = pygame.transform.scale(pencilimg,(50,50))
eraserimg = pygame.image.load('Photoshop\eraser.png')
eraserimg = pygame.transform.scale(eraserimg,(50,50))
fillimg = pygame.image.load('Photoshop\ebucket.png')
fillimg = pygame.transform.scale(fillimg,(50,50))
dropperimg = pygame.image.load('Photoshop\eyedropper.png')
dropperimg = pygame.transform.scale(dropperimg,(50,50))

######## FUNCTIONS ########
def redraw(screen, width, height, layer):
    screen.fill((70, 70, 70))
    #draws all pixels in canvas
    for tile in layer:
        tile.draw_block()
    #draws all buttons in ui
    for button in buttons:
        button.draw_button(screen)

    #draws colour box that displays current colour
    colour_box = pygame.Rect(horzMargin+canvasw+horzMargin//4,50,50,50)
    pygame.draw.rect(screen,currentClr,colour_box)
    pygame.draw.rect(screen,BLACK,colour_box,2)

    #draws sliders
    red_slider.draw_slider(screen, 5)
    green_slider.draw_slider(screen, 5)
    blue_slider.draw_slider(screen, 5)
    pygame.display.update()

def init_canvas():
    #creates a white canvas of block objects
    for i in range(vertMargin//gridsize, (canvash//gridsize) + vertMargin//gridsize):
        for j in range(horzMargin//gridsize,(canvasw//gridsize) + horzMargin//gridsize):
            block = Square(i,j,WHITE,screen, gridsize)
            layer.append(block)
            coords.append((i,j))


# def fill_bucket(r,c,currentcolour):
#     #WITH DFS
#     if (r,c) not in coords:
#         print('out of bounds')
#         return
#     elif layer[coords.index((r,c))].clr != currentcolour:
#         print('different colour')
#         return
#     else: 
#         layer[coords.index((r,c))].clr = currentClr
#         directions = ((r-1,c),(r,c+1),(r+1,c),(r,c-1))
#         for newr,newc in directions:
#             if (newr,newc) in coords and layer[coords.index((newr,newc))].clr == currentcolour:
#                 fill_bucket(newr,newc,currentcolour)

def fill_bucket(r,c,currentcolour):
    #WITH BFS
    #if clicked on same colour as current, return
    if currentcolour == currentClr:
        return
    q = Queue()
    q.enqueue((r,c))
    while not q.isEmpty():
        #remove head node of queue
        r,c = q.dequeue()
        # if coord is in bounds and colour is unfilled
        if (r,c) in coords and layer[coords.index((r,c))].clr == currentcolour:
            #change colour
            layer[coords.index((r,c))].clr = currentClr
            directions = ((r-1,c),(r,c+1),(r+1,c),(r,c-1))
            #enqueue all directions to queue
            for newr,newc in directions:
                q.enqueue((newr,newc))


init_canvas()

######## GLOBAL GAME VARIABLES ########## 
layer = []
coords = []

#int values
gridsize = 10
width = 800
height = 500
canvasw = 600
canvash = 400
horzMargin = (width-canvasw)//2
vertMargin = (height-canvash)//2
print('number of pixels:', (canvash//gridsize) * (canvasw//gridsize))

screen = pygame.display.set_mode((width, height))

#bools and misc
currentClr = BLACK
inGame = True
clicking = False
ctrl = False

#sliders
red_slider = Slider(horzMargin+canvasw+horzMargin//6, 120, horzMargin-horzMargin//3, RED)
green_slider = Slider(horzMargin+canvasw+horzMargin//6, 150, horzMargin-horzMargin//3, GREEN)
blue_slider = Slider(horzMargin+canvasw+horzMargin//6, 180, horzMargin-horzMargin//3, BLUE)

#buttons
pencil = Button(25,50,50,50, pencilimg)
eraser = Button(25,125,50,50, eraserimg)
bucket = Button(25,200,50,50, fillimg)
eyedropper = Button(25,275,50,50, dropperimg)
buttons = [pencil,eraser,bucket,eyedropper]
pencil.click_button(25,50)


###### MAIN LOOP #######
while inGame:
    mousex,mousey = pygame.mouse.get_pos()
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()

        if event.type == QUIT:
            pygame.quit()

        # used to check if buttons are pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True

            if bucket.click_button(mousex,mousey):
                print('fill bucket')
                bucket.deactivate_others(buttons)

            if pencil.click_button(mousex,mousey):
                print('pencil')
                pencil.deactivate_others(buttons)

            if eraser.click_button(mousex,mousey):
                print('eraser')
                eraser.deactivate_others(buttons)

            if eyedropper.click_button(mousex,mousey):
                print('eyedropper')
                eyedropper.deactivate_others(buttons)

        
        # ctrl-s to save
        if pressed[pygame.K_LCTRL]:
            ctrl = True
        
        if ctrl and pressed[pygame.K_s]:
            print('save')
            ctrl = False
            pygame.image.save(screen,'newimage.png')
            

        # if release mouse button
        if event.type == pygame.MOUSEBUTTONUP:
            clicking = False

    #is mouse is clicked and position in canvas bounds
    if clicking and (mousey//gridsize,mousex//gridsize) in coords:

        if pencil.isUsed:
            #draw using current colour
            layer[coords.index((mousey//gridsize,mousex//gridsize))].clr = currentClr
        
        if eraser.isUsed:
            #draw using white
            layer[coords.index((mousey//gridsize,mousex//gridsize))].clr = WHITE

        if bucket.isUsed:
            #screenshot colour before fill and pass it into function
            colour_now = layer[coords.index((mousey//gridsize,mousex//gridsize))].clr
            fill_bucket(mousey//gridsize,mousex//gridsize, colour_now)

        if eyedropper.isUsed:
            #set new positions of all sliders based on RBG
            red_slider.set_clr((layer[coords.index((mousey//gridsize,mousex//gridsize))].clr)[0])
            green_slider.set_clr((layer[coords.index((mousey//gridsize,mousex//gridsize))].clr)[1])
            blue_slider.set_clr((layer[coords.index((mousey//gridsize,mousex//gridsize))].clr)[2])


    #mouse detection for colour sliders
    red_slider.detect_mouse(clicking, mousex, mousey)
    green_slider.detect_mouse(clicking, mousex, mousey)
    blue_slider.detect_mouse(clicking, mousex, mousey)

    #changes current colour based on values from sliders
    currentClr = (red_slider.change_clr(), green_slider.change_clr(), blue_slider.change_clr())
        
    redraw(screen,width,height,layer)
    clock.tick(framerate)