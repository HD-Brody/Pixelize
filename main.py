import sys
import random
import time
import pygame
from PIL import Image
from blockClass import *
from buttonClass import *
from sliderClass import *
from queueClass import *
pygame.init()
from pygame.locals import QUIT
from stackClass import *
import time

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
GRAY = (40,40,45)

clock = pygame.time.Clock()
framerate = 1000

font = pygame.font.SysFont("Arial Black", 30)

###### IMAGES ######
pencilimg = pygame.image.load('images\pencil.png')
pencilimg = pygame.transform.scale(pencilimg,(50,50))
eraserimg = pygame.image.load('images\eraser.png')
eraserimg = pygame.transform.scale(eraserimg,(50,50))
fillimg = pygame.image.load('images\ebucket.png')
fillimg = pygame.transform.scale(fillimg,(50,50))
dropperimg = pygame.image.load('images\eyedropper.png')
dropperimg = pygame.transform.scale(dropperimg,(50,50))

eyeimg = pygame.image.load('images\eye.png')
eyeimg = pygame.transform.scale(eyeimg,(25,25))

saveimg = pygame.image.load('images\save.png')
saveimg = pygame.transform.scale(saveimg,(50,50))

logoimg = pygame.image.load('images\logo.png')
logoimg = pygame.transform.scale(logoimg,(400,400))

brush1img = pygame.image.load('images\size1brush.png')
brush1img = pygame.transform.scale(brush1img,(25,25))
brush2img = pygame.image.load('images\size2brush.png')
brush2img = pygame.transform.scale(brush2img,(25,25))
brush3img = pygame.image.load('images\size3brush.png')
brush3img = pygame.transform.scale(brush3img,(25,25))

######## FUNCTIONS ########
def redraw(screen, width, height, layerList):
    screen.fill((70, 70, 70))
    pygame.draw.rect(screen, WHITE, (layerList[0][0].col * gridsize, layerList[0][0].row * gridsize,canvasw,canvash))
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
    for bsb in brushSizeList:
        bsb.draw_button(screen)
    saveButton.draw_button(screen)

    #draws colour box that displays current colour
    colour_box = pygame.Rect(725,50,50,50)
    pygame.draw.rect(screen,currentClr,colour_box)
    pygame.draw.rect(screen,BLACK,colour_box,2)

    #draws sliders
    red_slider.draw_slider(screen, 5)
    green_slider.draw_slider(screen, 5)
    blue_slider.draw_slider(screen, 5)
    pygame.display.update()

def draw(mx, my, colour, bsize, oldClr):
    layerList[currentLayer][coords[currentLayer].index((my//gridsize,mx//gridsize))].clr = colour

    pixelchange = ((my//gridsize,mx//gridsize), oldClr, colour)

    if pixelchange[1] != colour:
        action.append(pixelchange)

    if bsize == 2:
        crds = [
            (my//gridsize + 1,mx//gridsize),
            (my//gridsize + 1,mx//gridsize + 1),
            (my//gridsize,mx//gridsize + 1)
        ]
        for i in crds:
            if i in coords[currentLayer]:
                if layerList[currentLayer][coords[currentLayer].index(i)].clr != colour:
                    action.append((i, layerList[currentLayer][coords[currentLayer].index(i)].clr, colour))
                    layerList[currentLayer][coords[currentLayer].index(i)].clr = colour
            
    if bsize == 3:
        crds = [
            (my//gridsize+1,mx//gridsize-1),
            (my//gridsize+1,mx//gridsize),
            (my//gridsize+1,mx//gridsize+1),
            (my//gridsize,mx//gridsize-1),
            (my//gridsize,mx//gridsize+1),
            (my//gridsize-1,mx//gridsize-1),
            (my//gridsize-1,mx//gridsize),
            (my//gridsize-1,mx//gridsize+1),
        ]
        for i in crds:
            if i in coords[currentLayer]:
                if layerList[currentLayer][coords[currentLayer].index(i)].clr != colour:
                    action.append((i, layerList[currentLayer][coords[currentLayer].index(i)].clr, colour))
                    layerList[currentLayer][coords[currentLayer].index(i)].clr = colour

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
            if layerList[currentLayer][coords[currentLayer].index((r,c))].clr != currentClr:
                    action.append(((r,c), layerList[currentLayer][coords[currentLayer].index((r,c))].clr, currentClr))
            layerList[currentLayer][coords[currentLayer].index((r,c))].clr = currentClr
            directions = ((r-1,c),(r,c+1),(r+1,c),(r,c-1))
            #enqueue all directions to queue
            for i in directions:
                q.enqueue(i)
                
def makeTransparent(imageName):
    img = Image.open(imageName)
    img = img.convert("RGBA")
 
    datas = img.getdata()
 
    newData = []
 
    for item in datas:
        if item[0] in range(230,256) and item[1] in range(230,256) and item[2] in range(230,256):
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
 
    img.putdata(newData)
    img.save("./transparentImg.png", "PNG")
    print("Successful")

######## GLOBAL GAME VARIABLES ########## 
layerList = []
coords = []

#int values
width = 800
height = 500
screen = pygame.display.set_mode((width, height))

#bools and misc
brushSize = 1
currentClr = BLACK
currentLayer = 0
startScreen = True
inGame = False
clicking = False
ctrl = False
action = []
moves = Stack()
#sliders
red_slider = Slider(716, 120, 70, RED)
green_slider = Slider(716, 150, 70, GREEN)
blue_slider = Slider(716, 180, 70, BLUE)

#buttons
pencil = Button(25,50,50,50, pencilimg)
eraser = Button(25,125,50,50, eraserimg)
bucket = Button(25,200,50,50, fillimg)
eyedropper = Button(25,275,50,50, dropperimg)
clear = Button(25, 350, 50, 50,None)
undo = Button(25, 425, 50, 50, None)
buttons = [pencil,eraser,bucket,eyedropper, clear, undo]

brush1button = Button(25,height-40,25,25,brush1img)
brush2button = Button(55,height-40,25,25,brush2img)
brush3button = Button(85,height-40,25,25,brush3img)
brushSizeList = [brush1button,brush2button,brush3button]

saveButton = Button(725,425,50,50, saveimg)

#layer buttons
layer1button = Button(737, 210, 60, 25)
layer2button = Button(737, 250, 60, 25)
layerButtons = [layer1button, layer2button]

# layer visibility buttons
layer1visible = Button(708, 210, 25, 25, eyeimg,True)
layer2visible = Button(708, 250, 25, 25,eyeimg,True)
layerVisibleButtons = [layer1visible, layer2visible]

#starts off with pencil and layer 1
pencil.click_button(pencil.x,pencil.y)
brush1button.click_button(brush1button.x,brush1button.y)
layer1button.click_button(layer1button.x, layer1button.y)

#START SCREEN VARIABLES
butWidth = 150
createFileBut = Button(width//2 - butWidth//2, 400,butWidth,50)

slidWidth = 250
widthSlider = Slider(width//2 - slidWidth//2, 250, slidWidth, WHITE, 15)
heightSlider = Slider(width//2 - slidWidth//2, 300, slidWidth, WHITE,15)
pixelSlider = Slider(width//2 - slidWidth//2, 350, slidWidth, WHITE,15)

widthSlider.mx += widthSlider.width
heightSlider.mx += heightSlider.width

###### MAIN LOOP #######
while startScreen:
    screen.fill((70, 70, 70))
    screen.blit(logoimg,((width//2 - logoimg.get_width()//2), -50))
    createFileBut.draw_button(screen)

    canvasw = int(round(100 + widthSlider.change_clr(500),-1))
    canvash = int(round(100 + heightSlider.change_clr(300),-1))
    gridsize = int(round((5 + pixelSlider.change_clr(15))/5)*5)

    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        mousex,mousey = pygame.mouse.get_pos()

        if event.type == QUIT:
            pygame.quit()

        # used to check if buttons are pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicking = True
            
            if createFileBut.click_button(mousex,mousey):
                canvash = round(canvash/gridsize)*gridsize
                canvasw = round(canvasw/gridsize)*gridsize
                horzMargin = (width-canvasw)//2
                vertMargin = (height-canvash)//2

                for l in layerButtons:
                    layerandcoords = create_new_layer()
                    layerList.append(layerandcoords[0])
                    coords.append(layerandcoords[1])
                for l in layerVisibleButtons:
                    l.click_button(l.x,l.y)
                startScreen = False
                inGame = True

        if event.type == pygame.MOUSEBUTTONUP:
            clicking = False

    for s in [widthSlider,heightSlider,pixelSlider]:
        s.draw_slider(screen,30, BLACK, 5)
        s.detect_mouse(clicking,mousex,mousey)

    widthText = font.render(str("Canvas width: "), 1, WHITE)
    heightText = font.render(str("Canvas height: "), 1, WHITE)
    gridText = font.render(str("Grid size: "), 1, WHITE)
    screen.blit(widthText,(25,240))
    screen.blit(heightText,(15,290))
    screen.blit(gridText,(100,340))

    widthNum = font.render(str(canvasw), 1, WHITE)
    heightNum = font.render(str(canvash), 1, WHITE)
    gridNum = font.render(str(gridsize), 1, WHITE)
    screen.blit(widthNum,(550,240))
    screen.blit(heightNum,(550,290))
    screen.blit(gridNum,(550,340))

    pygame.display.update()
    clock.tick(framerate)

time.sleep(0.1)

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

            #brush size buttons
            if brush1button.click_button(mousex,mousey):
                brushSize = 1
                brush1button.deactivate_others(brushSizeList)
            if brush2button.click_button(mousex,mousey):
                brushSize = 2
                brush2button.deactivate_others(brushSizeList)
            if brush3button.click_button(mousex,mousey):
                brushSize = 3
                brush3button.deactivate_others(brushSizeList)

            #misc buttons
            if saveButton.click_button(mousex,mousey):
                rect = pygame.Rect(layerList[0][0].col * gridsize, layerList[0][0].row * gridsize,canvasw,canvash) 
                sub = screen.subsurface(rect)
                screenshot = pygame.Surface((canvasw, canvash))
                screenshot.blit(sub, (0,0))
                pygame.image.save(screenshot, "newImg.jpg")
                makeTransparent("newImg.jpg")
            
        # ctrl-s to save
        if pressed[pygame.K_LCTRL]:
            ctrl = True
        
        if ctrl:
            if pressed[pygame.K_s]:
                ctrl = False
                rect = pygame.Rect(layerList[0][0].col * gridsize, layerList[0][0].row * gridsize,canvasw,canvash) 
                sub = screen.subsurface(rect)
                screenshot = pygame.Surface((canvasw, canvash))
                screenshot.blit(sub, (0,0))
                pygame.image.save(screenshot, "newImg.jpg")
                makeTransparent("newImg.jpg")
            if pressed[pygame.K_z]:
                if moves.size() > 0:
                    undoneaction = moves.pop()
                    for i in undoneaction:
                        layerList[currentLayer][coords[currentLayer].index(i[0])].clr = i[1]
                
        
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
            draw(mousex,mousey,currentClr,brushSize, oldClr)

        if eraser.isUsed:
            #draw using white
            oldClr = layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr
            draw(mousex,mousey,WHITE,brushSize, oldClr)

        if bucket.isUsed:
            #screenshot colour before fill and pass it into function
            colour_now = layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr
            fill_bucket(mousey//gridsize,mousex//gridsize, colour_now)

        if eyedropper.isUsed:
            #set new positions of all sliders based on RBG
            red_slider.set_clr((layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr)[0])
            green_slider.set_clr((layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr)[1])
            blue_slider.set_clr((layerList[currentLayer][coords[currentLayer].index((mousey//gridsize,mousex//gridsize))].clr)[2])

    redraw(screen,width,height,layerList)

    #mouse detection for colour sliders
    red_slider.detect_mouse(clicking, mousex, mousey)
    green_slider.detect_mouse(clicking, mousex, mousey)
    blue_slider.detect_mouse(clicking, mousex, mousey)

    #changes current colour based on values from sliders
    currentClr = (red_slider.change_clr(), green_slider.change_clr(), blue_slider.change_clr())
        
    clock.tick(framerate)

