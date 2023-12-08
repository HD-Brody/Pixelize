import random
import pygame
from blockClass import *
from buttonClass import *
from sliderClass import *
pygame.init()
from pygame.locals import QUIT

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
    for tile in layer:
        tile.draw_block()
    for button in buttons:
        button.draw_button(screen)

    colour_box = pygame.Rect(horzMargin+canvasw+horzMargin//4,50,50,50)
    pygame.draw.rect(screen,currentClr,colour_box)
    pygame.draw.rect(screen,BLACK,colour_box,2)

    red_slider.draw_slider(screen, 5)
    green_slider.draw_slider(screen, 5)
    blue_slider.draw_slider(screen, 5)
    pygame.display.update()

def init_canvas():
    for i in range(vertMargin//gridsize, (canvash//gridsize) + vertMargin//gridsize):
        for j in range(horzMargin//gridsize,(canvasw//gridsize) + horzMargin//gridsize):
            block = Square(i,j,WHITE,screen, gridsize)
            layer.append(block)
            coords.append((i,j))


def fill_bucket(r,c,currentclr):
    if (r,c) not in coords or layer[coords.index((r,c))].clr != currentclr:
        return
    
    else: 
        layer[coords.index((r,c))].clr = currentClr
        fill_bucket(r-1,c,currentclr)
        fill_bucket(r,c+1,currentclr)
        fill_bucket(r+1,c,currentclr)
        fill_bucket(r,c-1,currentclr)

def reset_all_buttons(buttonlist, currentbutton):
    for button in buttonlist:
        if button != currentbutton:
            button.clear_button()
    

######## GLOBAL GAME VARIABLES ########## 
layer = []
coords = []

#values
gridsize = 20
width = 800
height = 500
canvasw = 600
canvash = 400
horzMargin = (width-canvasw)//2
vertMargin = (height-canvash)//2
print(horzMargin)
print(vertMargin)

screen = pygame.display.set_mode((width, height))
inGame = True

drawing = False
usingEraser = False
usingDropper = False
clicking = False
currentClr = BLACK
fill = False

ctrl = False

init_canvas()

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

print(horzMargin//gridsize)
print((canvasw//gridsize) + horzMargin//gridsize)
print(vertMargin//gridsize)
print((canvash//gridsize) + vertMargin//gridsize)

###### MAIN LOOP #######
while inGame:
    mousex,mousey = pygame.mouse.get_pos()
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()

        if event.type == QUIT:
            pygame.quit()

        #fill bucket usage
        if event.type == pygame.MOUSEBUTTONDOWN and fill:
            if (mousey//gridsize,mousex//gridsize) in coords:
                print('FILL IT')
                colour_now = layer[coords.index((mousey//gridsize,mousex//gridsize))].clr
                print(colour_now)
                fill_bucket(mousey//gridsize,mousex//gridsize, colour_now)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if usingDropper:
                # print('dropped')
                # currentClr = layer[coords.index((mousey//gridsize,mousex//gridsize))].clr
                usingDropper = False
            drawing = True
            if mousex > horzMargin + canvasw:
                clicking = True
            if bucket.click_button(mousex,mousey):
                fill = True
                usingEraser = False
                print('fill bucket')
                reset_all_buttons(buttons,bucket)
            if pencil.click_button(mousex,mousey):
                print('pencil')
                currentClr = BLACK
                usingEraser = False
                fill = False
                reset_all_buttons(buttons,pencil)
            if eraser.click_button(mousex,mousey):
                print('eraser')
                # currentClr = WHITE
                drawing = False
                usingEraser = True
                fill = False
                reset_all_buttons(buttons,eraser)
            if eyedropper.click_button(mousex,mousey):
                usingDropper = True
                print('eyedropper')
                reset_all_buttons(buttons,eyedropper)
            
        if pressed[pygame.K_LCTRL]:
            ctrl = True
        
        if ctrl and pressed[pygame.K_s]:
            print('save')
            ctrl = False
            pygame.image.save(screen,'newimage.png')
            

        # if release mouse button
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            clicking = False
            # print('not drawing')

    #NEEDS FIXING ################

    if drawing:
        if (mousey//gridsize,mousex//gridsize) in coords:
            layer[coords.index((mousey//gridsize,mousex//gridsize))].clr = currentClr
            # print(mousey//gridsize,mousex//gridsize)
            # print('drawing rn')
    
    if usingEraser and drawing:
        if (mousey//gridsize,mousex//gridsize) in coords:
            layer[coords.index((mousey//gridsize,mousex//gridsize))].clr = WHITE


    red_slider.detect_mouse(clicking, mousex, mousey)
    green_slider.detect_mouse(clicking, mousex, mousey)
    blue_slider.detect_mouse(clicking, mousex, mousey)
    clrlist = list(currentClr)
    clrlist[0] = red_slider.change_clr()
    clrlist[1] = green_slider.change_clr()
    clrlist[2] = blue_slider.change_clr()
    currentClr = tuple(clrlist)
        
    redraw(screen,width,height,layer)
    clock.tick(framerate)