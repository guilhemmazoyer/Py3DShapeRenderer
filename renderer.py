import sys, math
import pygame
from pygame.locals import KEYDOWN, K_q
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

class Renderer:
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

    GAME_FPS = 120

    ROTATION_ANGLE = 0.01
    ROTATION_MATRICE = [math.cos(ROTATION_ANGLE),-math.sin(ROTATION_ANGLE),math.sin(ROTATION_ANGLE),math.cos(ROTATION_ANGLE)]

# PARAMETERS:
    # High:
    _WIN = None
    running = True

    # Render:
    focal_length = 300
    rotX = rotY = rotZ = False

    # GUI:
    sliderRotX = Slider
    sliderRotY = Slider
    sliderRotZ = Slider
    sliderFill = Slider
    sliderFocalLength = Slider
    

    def __init__(self) -> None:
        pass
    
    @classmethod
    def drawLine(self, line):
        SP1 = self.project3DOn2DScreen(self.VERTEX_TABLE[line[0]])
        SP2 = self.project3DOn2DScreen(self.VERTEX_TABLE[line[1]])
        pygame.draw.line(self._WIN, self.LIT, SP1, SP2, 2)
    
    @classmethod
    def drawPolygon(self, face):
        polygonPoints = self.findPolygonPoint(face)
        pygame.draw.polygon(self._WIN, (220,220,220), polygonPoints, 0)
    
    @classmethod
    def findPolygonPoint(self, face):
        P1 = self.project3DOn2DScreen(self.VERTEX_TABLE[face[0]])
        P2 = self.project3DOn2DScreen(self.VERTEX_TABLE[face[1]])
        P3 = self.project3DOn2DScreen(self.VERTEX_TABLE[face[2]])
        P4 = self.project3DOn2DScreen(self.VERTEX_TABLE[face[3]])
        return [P1,P2,P3,P4]
        
    @classmethod
    def project3DOn2DScreen(self, Point3D):
        PointX = (self.focal_length*Point3D[0])/(self.focal_length+Point3D[2])
        PointY = (self.focal_length*Point3D[1])/(self.focal_length+Point3D[2])
        return [PointX+(self.WIDTH/2),PointY+(self.HEIGHT/2)]
    
    @classmethod
    def rotateOnAxis(self):
        if(self.rotX) :
            for vertex in self.VERTEX_TABLE :
                ROTATION_RESULT = [vertex[1]*self.ROTATION_MATRICE[0]+vertex[2]*self.ROTATION_MATRICE[2],
                                    vertex[1]*self.ROTATION_MATRICE[1]+vertex[2]*self.ROTATION_MATRICE[3]]
                vertex[1] = ROTATION_RESULT[0]
                vertex[2] = ROTATION_RESULT[1]

        if(self.rotY) :
            for vertex in self.VERTEX_TABLE :
                ROTATION_RESULT = [vertex[0]*self.ROTATION_MATRICE[0]+vertex[2]*self.ROTATION_MATRICE[2],
                                    vertex[0]*self.ROTATION_MATRICE[1]+vertex[2]*self.ROTATION_MATRICE[3]]
                vertex[0] = ROTATION_RESULT[0]
                vertex[2] = ROTATION_RESULT[1]

        if(self.rotZ) :
            for vertex in self.VERTEX_TABLE :
                ROTATION_RESULT = [vertex[0]*self.ROTATION_MATRICE[0]+vertex[1]*self.ROTATION_MATRICE[2],
                                    vertex[0]*self.ROTATION_MATRICE[1]+vertex[1]*self.ROTATION_MATRICE[3]]
                vertex[0] = ROTATION_RESULT[0]
                vertex[1] = ROTATION_RESULT[1]

    @staticmethod
    def checkEvents():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == KEYDOWN and event.key == K_q:
                pygame.quit()
                sys.exit()