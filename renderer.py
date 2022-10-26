import sys, math
import pygame
from pygame.locals import KEYDOWN, K_q
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# CONSTANTS:
SCREENSIZE = WIDTH, HEIGHT = 500, 500
LIT = (214, 214, 66)
BACKGROUND_COLOR = (10, 10, 10)

#[x,y,z]
VERTEX_TABLE = [[23,63,85],
                [23,-63,85],
                [-86,-63,22],
                [-86,63,22],
                [86,63,-24],
                [86,-63,-24],
                [-23,-63,-87],
                [-23,63,-87]]
#[p1,p2]
EDGE_TABLE = [[0,1], [1,2], [2,3], [3,0],
            [4,5], [5,6], [6,7], [7,4],
            [0,4], [1,5], [2,6], [3,7]]

#[p1,p2,p3,p4,color index]
FACE_TABLE = [[0,1,2,3,0],[1,5,6,2,1],
            [3,4,7,6,2],[4,0,3,7,3],
            [3,2,6,7,4],[0,1,5,4,5]]

FOCAL_LENGHT = 300
GAME_FPS = 120

ROTATION_ANGLE = 0.01
ROTATION_MATRICE = [math.cos(ROTATION_ANGLE),-math.sin(ROTATION_ANGLE),math.sin(ROTATION_ANGLE),math.cos(ROTATION_ANGLE)]

ROTATE_X = False
ROTATE_Y = False
ROTATE_Z = False

# This is the main game loop, it constantly runs until you press the Q KEY
# or close the window.
# CAUTION: This will run as fast as you computer allows,
# if you need to set a specific FPS look at tick methods.

def main():
    pygame.init()  # Initial Setup
    _WIN = pygame.display.set_mode(SCREENSIZE)
    rotX = rotY = rotZ = False
    focal_lenght = FOCAL_LENGHT

    sliderRotX = Slider(_WIN, 25, 25, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputRotX = TextBox(_WIN, 30, 35, 20, 20, fontSize=20, borderThickness=2)
    outputRotX.setText("X")
    outputRotX.disable()  # Act as label instead of textbox

    sliderRotY = Slider(_WIN, 90, 25, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputRotY = TextBox(_WIN, 95, 35, 20, 20, fontSize=20, borderThickness=2)
    outputRotY.setText("Y")
    outputRotY.disable()  # Act as label instead of textbox

    sliderRotZ = Slider(_WIN, 155, 25, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputRotZ = TextBox(_WIN, 160, 35, 20, 20, fontSize=20, borderThickness=2)
    outputRotZ.setText("Z")
    outputRotZ.disable()  # Act as label instead of textbox

    sliderFill = Slider(_WIN, WIDTH-55, 25, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputFill = TextBox(_WIN, WIDTH-60, 40, 40, 20, fontSize=20, borderThickness=2)
    outputFill.setText("FILL")
    outputFill.disable()  # Act as label instead of textbox

    sliderFocalLenght = Slider(_WIN, 25, HEIGHT-40, 200, 15, min=50, max=400, step=2, handleColour=(180,0,0), initial=focal_lenght)
    outputFocalLenght = TextBox(_WIN, 105, HEIGHT-62, 40, 25, fontSize=20)
    outputFocalLenght.disable()  # Act as label instead of textbox

    # The loop proper, things inside this loop will
    # be called over and over until you exit the window
    running = True
    while running:
        checkEvents()
        focal_lenght = sliderFocalLenght.getValue()

        if(sliderRotX.getValue() == 1) :
            rotX = True
        else:
            rotX = False
        if(sliderRotY.getValue() == 1) :
            rotY = True
        else:
            rotY = False

        if(sliderRotZ.getValue() == 1) :
            rotZ = True
        else:
            rotZ = False

        _WIN.fill(BACKGROUND_COLOR)
        for line in EDGE_TABLE :
            drawLine(line, focal_lenght, _WIN)
        for face in FACE_TABLE:
            customColor = (42*face[4],42*face[4],42*face[4])
            drawPolygon(face, customColor, focal_lenght, _WIN)
        outputFocalLenght.setText(sliderFocalLenght.getValue())
        rotateOnAxis(rotX, rotY, rotZ)

        pygame_widgets.update(pygame.event.get())
        pygame.display.update()
        pygame.time.Clock().tick(GAME_FPS)

def drawLine(line, focal_lenght, _WIN):
    SP1 = project3DOn2DScreen(focal_lenght, VERTEX_TABLE[line[0]])
    SP2 = project3DOn2DScreen(focal_lenght, VERTEX_TABLE[line[1]])
    pygame.draw.line(_WIN, LIT, SP1, SP2, 2)

def drawPolygon(face, customColor, focal_lenght, _WIN):
    polygonPoints = findPolygonPoint(face, focal_lenght)
    pygame.draw.polygon(_WIN, customColor, polygonPoints, 0)

def findPolygonPoint(face, focal_lenght):
    P1 = project3DOn2DScreen(focal_lenght,VERTEX_TABLE[face[0]])
    P2 = project3DOn2DScreen(focal_lenght,VERTEX_TABLE[face[1]])
    P3 = project3DOn2DScreen(focal_lenght,VERTEX_TABLE[face[2]])
    P4 = project3DOn2DScreen(focal_lenght,VERTEX_TABLE[face[3]])
    return [P1,P2,P3,P4]

def project3DOn2DScreen(focal_lenght, Point3D):
    PointX = (focal_lenght*Point3D[0])/(focal_lenght+Point3D[2])
    PointY = (focal_lenght*Point3D[1])/(focal_lenght+Point3D[2])
    return [PointX+(WIDTH/2),PointY+(HEIGHT/2)]

def rotateOnAxis(rotX, rotY, rotZ):
    if(rotX) :
        for vertex in VERTEX_TABLE :
            ROTATION_RESULT = [vertex[1]*ROTATION_MATRICE[0]+vertex[2]*ROTATION_MATRICE[2],vertex[1]*ROTATION_MATRICE[1]+vertex[2]*ROTATION_MATRICE[3]]
            vertex[1] = ROTATION_RESULT[0]
            vertex[2] = ROTATION_RESULT[1]

    if(rotY) :
        for vertex in VERTEX_TABLE :
            ROTATION_RESULT = [vertex[0]*ROTATION_MATRICE[0]+vertex[2]*ROTATION_MATRICE[2],vertex[0]*ROTATION_MATRICE[1]+vertex[2]*ROTATION_MATRICE[3]]
            vertex[0] = ROTATION_RESULT[0]
            vertex[2] = ROTATION_RESULT[1]

    if(rotZ) :
        for vertex in VERTEX_TABLE :
            ROTATION_RESULT = [vertex[0]*ROTATION_MATRICE[0]+vertex[1]*ROTATION_MATRICE[2],vertex[0]*ROTATION_MATRICE[1]+vertex[1]*ROTATION_MATRICE[3]]
            vertex[0] = ROTATION_RESULT[0]
            vertex[1] = ROTATION_RESULT[1]

def checkEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()