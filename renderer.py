import sys, math
import pygame
from pygame.locals import KEYDOWN, K_q
from pygame_widgets.slider import Slider

class Renderer:
# CONSTANTS:
    SCREENSIZE = WIDTH, HEIGHT = 500, 500
    LIT = (214, 214, 66)
    BACKGROUND_COLOR = (20, 20, 20)
    BACKGROUND_BORDER_GRADIENT = (50, 50, 50)
    BACKGROUND_CENTER_GRADIENT = (225, 225, 225)

    #[x,y,z]
    CENTER_VERTEX = [0,0]

    #[x,y,z] relative to the center
    VERTEX_TABLE = [[23,63,85],
                    [23,-63,85],
                    [-86,-63,22],
                    [-86,63,22],
                    [86,63,-24],
                    [86,-63,-24],
                    [-23,-63,-87],
                    [-23,63,-87]]

    #[x,y]
    #PROJECTED_VERTEX_TABLE = [[0,0]*len(VERTEX_TABLE)]
    PROJECTED_VERTEX_TABLE = [[0,0],
                            [0,0],
                            [0,0],
                            [0,0],
                            [0,0],
                            [0,0],
                            [0,0],
                            [0,0]]

    #[p1,p2]
    EDGE_TABLE = [[0,1], [1,2], [2,3], [3,0],
                [0,4], [1,5], [2,6], [3,7],
                [4,5], [5,6], [6,7], [7,4]]

    #[p1,p2,p3,p4,color index]
    FACE_TABLE = [[0,1,2,3,0],[1,5,6,2,1],
                [4,5,6,7,2],[4,0,3,7,3],
                [3,2,6,7,4],[0,1,5,4,5]]

    GAME_FPS = 120

    ROTATION_ANGLE = 0.01
    ROTATION_MATRICE = [math.cos(ROTATION_ANGLE),math.sin(ROTATION_ANGLE)]
    MOVE_VALUE = 1

# PARAMETERS:
    # High:
    _WIN = None
    running = True

    # Render:
    focal_length = 300
    rotX = rotY = rotZ = False
    transX = transY = transXinv = transYinv = False
    fill = False

    # GUI:
    sliderRotX = sliderRotY = sliderRotZ = Slider
    sliderFill = sliderFocalLength = Slider
    

    def __init__(self) -> None:
        pass


    """Draw lines"""
    @classmethod
    def drawLine(self):
        for line in self.EDGE_TABLE:
            SP1 = self.PROJECTED_VERTEX_TABLE[line[0]]
            SP2 = self.PROJECTED_VERTEX_TABLE[line[1]]
            pygame.draw.line(self._WIN, self.LIT, SP1, SP2, 2)
    

    """Draw polygons"""
    @classmethod
    def drawPolygon(self):
        facesToDraw = self.findFacesToDrawFromFaceArray(self.sortFaces(self.FACE_TABLE))
        for i in range(2,len(facesToDraw)) :
            polygonPoints = self.findPolygonPoint(facesToDraw[i])
            pygame.draw.polygon(self._WIN, self.getColorFromIndex(facesToDraw[i][4]), polygonPoints, 0)


    """Sorting tools, croissant storage"""
    @classmethod
    def sortFaces(self, facesArray):
        # Create a copy of linesArray and iterate on it
        AFace=[]
        AIndex=[0,1,2,3,4,5]
        for face in facesArray:
            AFace.append(face)

        for i in range(len(AFace)):
	
            # Find the minimum element in remaining
            # unsorted array
            min_idx = i
            for j in range(i+1, len(AFace)):
                # take the average value of Z for each face
                ea1 = AFace[min_idx][0]
                eb1 = AFace[min_idx][1]
                ec1 = AFace[min_idx][2]
                ed1 = AFace[min_idx][3]
                e1 = (self.VERTEX_TABLE[ea1][2] + self.VERTEX_TABLE[eb1][2] + self.VERTEX_TABLE[ec1][2] + self.VERTEX_TABLE[ed1][2])/4

                ea2 = AFace[j][0]
                eb2 = AFace[j][1]
                ec2 = AFace[j][2]
                ed2 = AFace[j][3]
                e2 = (self.VERTEX_TABLE[ea2][2] + self.VERTEX_TABLE[eb2][2] + self.VERTEX_TABLE[ec2][2] + self.VERTEX_TABLE[ed2][2])/4

                if e1 > e2:
                    min_idx = j
                    
            # Swap the found minimum element with
            # the first element	
            AFace[i], AFace[min_idx] = AFace[min_idx], AFace[i]
            AIndex[i], AIndex[min_idx] = AIndex[min_idx], AIndex[i]
        return AIndex


    """Return faces to draw based on an index array"""
    @classmethod
    def findFacesToDrawFromFaceArray(self, arrayFaceIndex):
        facesToDraw = []
        for index in arrayFaceIndex:
            facesToDraw.append(self.FACE_TABLE[index])
        facesToDraw.reverse()
        return facesToDraw


    """Return the points that constitute a given face"""
    @classmethod
    def findPolygonPoint(self, face):
        P1 = self.PROJECTED_VERTEX_TABLE[face[0]]
        P2 = self.PROJECTED_VERTEX_TABLE[face[1]]
        P3 = self.PROJECTED_VERTEX_TABLE[face[2]]
        P4 = self.PROJECTED_VERTEX_TABLE[face[3]]
        return [P1,P2,P3,P4]


    """Project a vertex and return its value in the 2D space"""
    @classmethod
    def project3DOn2DScreen(self, vertex):
        PointX = (self.focal_length*vertex[0])/(self.focal_length+vertex[2])
        PointY = (self.focal_length*vertex[1])/(self.focal_length+vertex[2])
        return [PointX+(self.WIDTH/2),PointY+(self.HEIGHT/2)]


    """Rotate the points in the 3D space"""
    @classmethod
    def rotateOnAxis(self):
        # Rotation de tous les points du cube par rapport à l'axe X
        if(self.rotX) :
            for vertex in self.VERTEX_TABLE :
                ROTATION_X_RESULT = [vertex[1]*self.ROTATION_MATRICE[0]+vertex[2]*-self.ROTATION_MATRICE[1],
                                    vertex[1]*self.ROTATION_MATRICE[1]+vertex[2]*self.ROTATION_MATRICE[0]]
                vertex[1] = ROTATION_X_RESULT[0]
                vertex[2] = ROTATION_X_RESULT[1]

        # Rotation de tous les points du cube par rapport à l'axe Y
        if(self.rotY) :
            for vertex in self.VERTEX_TABLE :
                ROTATION_Y_RESULT = [vertex[0]*self.ROTATION_MATRICE[0]+vertex[2]*-self.ROTATION_MATRICE[1],
                                    vertex[0]*self.ROTATION_MATRICE[1]+vertex[2]*self.ROTATION_MATRICE[0]]
                vertex[0] = ROTATION_Y_RESULT[0]
                vertex[2] = ROTATION_Y_RESULT[1]
        
        # Rotation de tous les points du cube par rapport à l'axe Z
        if(self.rotZ) :
            for vertex in self.VERTEX_TABLE :
                ROTATION_Z_RESULT = [vertex[0]*self.ROTATION_MATRICE[0]+vertex[1]*-self.ROTATION_MATRICE[1],
                                    vertex[0]*self.ROTATION_MATRICE[1]+vertex[1]*self.ROTATION_MATRICE[0]]
                vertex[0] = ROTATION_Z_RESULT[0]
                vertex[1] = ROTATION_Z_RESULT[1]


    """Move the vertices in the 3D space"""
    @classmethod
    def moveProjectVerticesOnAxis(self):
        # Déplacement de tous les points du cube sur l'axe X
        if self.transX:
            if self.transXinv :
                if (self.CENTER_VERTEX+self.MOVE_VALUE)<250 :
                    self.CENTER_VERTEX+=self.MOVE_VALUE
                else:
                    self.transXinv = False
            else :
                if (self.CENTER_VERTEX-self.MOVE_VALUE)>-250 :
                    self.CENTER_VERTEX-=self.MOVE_VALUE
                else:
                    self.transXinv = True

        # Déplacement de tous les points du cube sur l'axe Y
        if self.transY :
            if self.transYinv :
                if (self.CENTER_VERTEX+self.MOVE_VALUE)<250 :
                    self.CENTER_VERTEX+=self.MOVE_VALUE
                else:
                    self.transYinv = False
            else :
                if (self.CENTER_VERTEX-self.MOVE_VALUE)>-250 :
                    self.CENTER_VERTEX-=self.MOVE_VALUE
                else:
                    self.transYinv = True


    """Project points from 3D space to 2D space"""
    @classmethod
    def projectVertices(self):
        for i in range(len(self.VERTEX_TABLE)):
            self.PROJECTED_VERTEX_TABLE[i] = self.project3DOn2DScreen(self.VERTEX_TABLE[i])


    @classmethod
    def gradientRect(self, border_colour, middle_colour, target_rect ):
        """ Draw a gradient filled rectangle covering <target_rect> """
        colour_rect = pygame.Surface( ( 3, 3 ) )                                   # tiny! 3x3 bitmap
        pygame.draw.line( colour_rect, border_colour,  ( 0,0 ), ( 0,2 ) )            # up colour line
        pygame.draw.line( colour_rect, border_colour, ( 1,0 ), ( 1,2 ) )            # middle colour line
        pygame.draw.line( colour_rect, border_colour, ( 2,0 ), ( 2,2 ) )            # down colour line
        pygame.draw.line( colour_rect, middle_colour, ( 1,1 ), ( 1,1 ) )            # center colour point

        colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
        self._WIN.blit( colour_rect, target_rect )


    @staticmethod
    def getColorFromIndex(index):
        if index==0:
            return (250,0,0)
        elif index==1:
            return (125,125,0)
        elif index==2:
            return (0,250,0)
        elif index==3:
            return (0,125,125)
        elif index==4:
            return (0,0,250)
        elif index==5:
            return (125,125,125)
        else:
            return (0,0,0)


    @staticmethod
    def checkEvents():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == KEYDOWN and event.key == K_q:
                pygame.quit()
                sys.exit()