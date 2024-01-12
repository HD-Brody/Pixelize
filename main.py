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
from stackClass import *
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
pencilimg = pygame.image.load('.\pencil.png')
pencilimg = pygame.transform.scale(pencilimg,(50,50))
eraserimg = pygame.image.load('.\eraser.png')
eraserimg = pygame.transform.scale(eraserimg,(50,50))
fillimg = pygame.image.load('.\ebucket.png')
fillimg = pygame.transform.scale(fillimg,(50,50))
dropperimg = pygame.image.load('.\eyedropper.png')
dropperimg = pygame.transform.scale(dropperimg,(50,50))
eyeimg = pygame.image.load('.\eye.png')
eyeimg = pygame.transform.scale(eyeimg,(25,25))


######## FUNCTIONS ########
def redraw(screen, width, height, layerList):
    screen.fill((70, 70, 70))
    pygame.draw.rect(screen, WHITE, (horzMargin,vertMargin,canvasw,canvash))
    #draws all pixels in canvas
    for i in range(len(layerList)):
        if layerVisibleButtons[i].isUsed:
            for block in layerList[i]:
                block.draw_block()

    #draws all buttons in ui
    for button in buttons:
        button.draw_button(screen)
    for lay in layerButtons:
        lay.draw_button(screen)
    for vis in layerVisibleButtons:
        vis.draw_button(screen)

    #draws colour box that displays current colour
    colour_box = pygame.Rect(horzMargin+canvasw+horzMargin//4,50,50,50)
    pygame.draw.rect(screen,currentClr,colour_box)
    pygame.draw.rect(screen,BLACK,colour_box,2)

    #draws sliders
    red_slider.draw_slider(screen, 5)
    green_slider.draw_slider(screen, 5)
    blue_slider.draw_slider(screen, 5)
    pygame.display.update()


def create_new_layer():
    layer = []
    coord = []
    for i in range(vertMargin//gridsize, (canvash//gridsize) + vertMargin//gridsize):
        for j in range(horzMargin//gridsize,(canvasw//gridsize) + horzMargin//gridsize):
            block = Square(i,j,WHITE,screen, gridsize)
            layer.append(block)
            coord.append((i,j))
    
    return (layer,coord)

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
        if (r,c) in coords[currentLayer] and layerList[currentLayer][coords[currentLayer].index((r,c))].clr == currentcolour:
            #change colour
            layerList[currentLayer][coords[currentLayer].index((r,c))].clr = currentClr
            directions = ((r-1,c),(r,c+1),(r+1,c),(r,c-1))
            #enqueue all directions to queue
            for newr,newc in directions:
                q.enqueue((newr,newc))


######## GLOBAL GAME VARIABLES ########## 
layerList = []
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
currentLayer = 0
inGame = True
clicking = False
ctrl = False
action = []
moves = Stack()
#sliders
red_slider = Slider(horzMargin+canvasw+horzMargin//6, 120, horzMargin-horzMargin//3, RED)
green_slider = Slider(horzMargin+canvasw+horzMargin//6, 150, horzMargin-horzMargin//3, GREEN)
blue_slider = Slider(horzMargin+canvasw+horzMargin//6, 180, horzMargin-horzMargin//3, BLUE)

#buttons
pencil = Button(25,50,50,50, pencilimg)
eraser = Button(25,125,50,50, eraserimg)
bucket = Button(25,200,50,50, fillimg)
eyedropper = Button(25,275,50,50, dropperimg)
clear = Button(25, 350, 50, 50,None)
undo = Button(25, 425, 50, 50, None)
buttons = [pencil,eraser,bucket,eyedropper, clear, undo]

#layer buttons
layer1button = Button(horzMargin+canvasw+horzMargin//6 + 20, 210, horzMargin-horzMargin//3, 25)
layer2button = Button(horzMargin+canvasw+horzMargin//6 + 20, 250, horzMargin-horzMargin//3, 25)
layerButtons = [layer1button, layer2button]

# layer visibility buttons
layer1visible = Button(horzMargin+canvasw+horzMargin//12, 210, 25, 25, eyeimg)
layer2visible = Button(horzMargin+canvasw+horzMargin//12, 250, 25, 25,eyeimg)
layerVisibleButtons = [layer1visible, layer2visible]

#starts off with pencil and layer 1
pencil.click_button(25,50)
layer1button.click_button(horzMargin+canvasw+horzMargin//6+20, 210)

for l in layerButtons:
    layerandcoords = create_new_layer()
    layerList.append(layerandcoords[0])
    coords.append(layerandcoords[1])
for l in layerVisibleButtons:
    l.click_button(l.x,l.y)
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
            
            if clear.click_button(mousex,mousey,'clear'):
                print('screen clear')
                for i in layerList[currentLayer]:
                    i.clr = WHITE
            if undo.click_button(mousex, mousey):
                print('undo')
                if moves.size() > 0:
                    undoneaction = moves.pop()
                    for i in undoneaction:
                        print(i)
                        layerList[currentLayer][coords[currentLayer].index(i[0])].clr = i[1]

            if eyedropper.click_button(mousex,mousey):
                print('eyedropper')
                eyedropper.deactivate_others(buttons)
            
            #layer button presses
            if layer1button.click_button(mousex,mousey):
                currentLayer = 0
                layer1button.deactivate_others(layerButtons)
                print(currentLayer)
            
            if layer2button.click_button(mousex,mousey):
                currentLayer = 1
                layer2button.deactivate_others(layerButtons)
                print(currentLayer)

            #layer visibility buttons
            if layer1visible.click_button(mousex,mousey, 'layer'):
                layer1visible.isUsed = not layer1visible.isUsed

                if layer1visible.clr == (40,40,45):
                    layer1visible.clr = (90,90,95)
                else:
                    layer1visible.clr = (40,40,45)

            if layer2visible.click_button(mousex,mousey, 'layer'):
                layer2visible.isUsed = not layer2visible.isUsed

                if layer2visible.clr == (40,40,45):
                    layer2visible.clr = (90,90,95)
                else:
                    layer2visible.clr = (40,40,45)
        
        # ctrl-s to save
        if pressed[pygame.K_LCTRL]:
            ctrl = True
        
        if ctrl and pressed[pygame.K_s]:
            print('save')
            ctrl = False
            pygame.image.save(screen,'newimage.png')
            
        # if release mouse button
        if event.type == pygame.MOUSEBUTTONUP:
            if len(action)>0:
                moves.push(action)
            clicking = False
            action = []


    #is mouse is clicked and position in canvas bounds
    if clicking and (mousey//gridsize,mousex//gridsize) in coords[0]:

        if pencil.isUsed:
            #draw using current colour
            oldClr = layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr
            pixelchange = ((mousey//gridsize,mousex//gridsize), oldClr, currentClr)
            action.append(pixelchange)
            layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr = currentClr

        
        if eraser.isUsed:
            #draw using white
            layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr = WHITE

        if bucket.isUsed:
            #screenshot colour before fill and pass it into function
            colour_now = layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr
            fill_bucket(mousey//gridsize,mousex//gridsize, colour_now)

        if eyedropper.isUsed:
            #set new positions of all sliders based on RBG
            red_slider.set_clr((layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr)[0])
            green_slider.set_clr((layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr)[1])
            blue_slider.set_clr((layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr)[2])
        
            




    #mouse detection for colour sliders
    red_slider.detect_mouse(clicking, mousex, mousey)
    green_slider.detect_mouse(clicking, mousex, mousey)
    blue_slider.detect_mouse(clicking, mousex, mousey)

    #changes current colour based on values from sliders
    currentClr = (red_slider.change_clr(), green_slider.change_clr(), blue_slider.change_clr())
        
    redraw(screen,width,height,layerList)
    clock.tick(framerate)

