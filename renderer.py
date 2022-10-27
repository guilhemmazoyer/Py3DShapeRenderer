import sys, math
import pygame
from pygame.locals import KEYDOWN, K_q
from pygame_widgets.slider import Slider

class Renderer:
# CONSTANTS:
    SCREENSIZE = WIDTH, HEIGHT = 500, 500
    LIT = (214, 214, 66)
    BACKGROUND_COLOR = (10, 10, 10)

    #[x,y,z]
    """VERTEX_TABLE = [[23,63,85], # Cube1
                    [23,-63,85],
                    [-86,-63,22],
                    [-86,63,22],
                    [86,63,-24],
                    [86,-63,-24],
                    [-23,-63,-87],
                    [-23,63,-87]]"""
    VERTEX_TABLE = [[50,-50,50], # Cube2
                    [50,-50,-50],
                    [-50,-50,-50],
                    [-50,-50,50],
                    [50,50,50],
                    [50,50,-50],
                    [-50,50,-50],
                    [-50,50,50]]

    #[p1,p2]
    """EDGE_TABLE = [[0,1], [1,2], [2,3], [3,0], # Cube1
                [0,4], [1,5], [2,6], [3,7],
                [4,5], [5,6], [6,7], [7,4]]"""
    EDGE_TABLE = [[0,1], [1,2], [2,3], [3,0], # Cube2
                [0,4], [1,5], [2,6], [3,7],
                [4,5], [5,6], [6,7], [7,4]]

    #[p1,p2,p3,p4,color index]
    """FACE_TABLE = [[0,1,2,3,0],[1,5,6,2,1], # Cube1
                [4,5,6,7,2],[4,0,3,7,3],
                [3,2,6,7,4],[0,1,5,4,5]]"""
    FACE_TABLE = [[0,1,2,3,0],[1,5,6,2,1], # Cube2
                [4,5,6,7,2],[4,0,3,7,3],
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
    fill = False

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
    def drawPolygon(self):
        #facesToDraw = self.findFacesToDrawFromIndexPoint(self.sortPoints(self.VERTEX_TABLE))
        #facesToDraw = self.findFacesToDrawFromLineArray(self.sortLines(self.EDGE_TABLE))
        facesToDraw = self.findFacesToDrawFromFaceArray(self.sortFaces(self.FACE_TABLE))
        for face in facesToDraw :
            polygonPoints = self.findPolygonPoint(face)
            pygame.draw.polygon(self._WIN, self.getColorFromIndex(face[4]), polygonPoints, 0)

    @staticmethod
    def sortPoints(pointsArray):
        # Create a copy of pointArray and iterate on it
        APoint=[]
        AIndex=[0,1,2,3,4,5,6,7]
        for point in pointsArray:
            APoint.append(point)

        for i in range(len(APoint)):
	
            # Find the minimum element in remaining
            # unsorted array
            min_idx = i
            for j in range(i+1, len(APoint)):
                if APoint[min_idx][2] < APoint[j][2]:
                    min_idx = j
                    
            # Swap the found minimum element with
            # the first element	
            APoint[i], APoint[min_idx] = APoint[min_idx], APoint[i]
            AIndex[i], AIndex[min_idx] = AIndex[min_idx], AIndex[i]
        return AIndex
    
    @classmethod
    def sortLines(self, linesArray):
        # Create a copy of linesArray and iterate on it
        ALine=[]
        AIndex=[0,1,2,3,4,5,6,7,8,9,10,11]
        for line in linesArray:
            ALine.append(line)

        for i in range(len(ALine)):
	
            # Find the minimum element in remaining
            # unsorted array
            min_idx = i
            for j in range(i+1, len(ALine)):
                # take the average value of Z for each line
                ea1 = ALine[min_idx][0]
                eb1 = ALine[min_idx][1]
                e1 = (self.VERTEX_TABLE[ea1][2] + self.VERTEX_TABLE[eb1][2])/2

                ea2 = ALine[j][0]
                eb2 = ALine[j][1]
                e2 = (self.VERTEX_TABLE[ea2][2] + self.VERTEX_TABLE[eb2][2])/2

                if e1 > e2:
                    min_idx = j
                    
            # Swap the found minimum element with
            # the first element	
            ALine[i], ALine[min_idx] = ALine[min_idx], ALine[i]
            AIndex[i], AIndex[min_idx] = AIndex[min_idx], AIndex[i]
        return AIndex

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

    @classmethod
    def findFacesToDrawFromIndexPoint(self, pointIndex):
        facesToDraw = []
        for face in self.FACE_TABLE :
            for i in range(len(face)-1):
                if(face[i]==pointIndex):
                    facesToDraw.append(face)
        return facesToDraw
    
    @classmethod
    def findFacesToDrawFromLineArray(self, arrayLineIndex):
        facesToDraw = []
        tempLine = []
        tempFaceStock = []

        for lineIndex in arrayLineIndex:
            tempLine = self.EDGE_TABLE[lineIndex]
            for face in self.FACE_TABLE:
                for i in range(len(face)-1):
                    # Check if a point of the line is ine the face
                    if tempLine[0]==face[i] or tempLine[1]==face[i] :
                        # Check if the second point of the line is an edge of this face
                        # Check if i+1 is out of range (to match the last vertex with the first vertex)
                        if (i+1)>len(face)-1 :
                            if tempLine[0]==face[0] or tempLine[1]==face[0] :
                                tempFaceStock.append(face)
                            else:
                                pass
                        else:
                            if tempLine[0]==face[i+1] or tempLine[1]==face[i+1] :
                                tempFaceStock.append(face)
        
        tempFaceStock.reverse()
        for face in tempFaceStock:
            if face not in facesToDraw:
                facesToDraw.append(face)

        return facesToDraw

    @classmethod
    def findFacesToDrawFromFaceArray(self, arrayFaceIndex):
        facesToDraw = []

        for index in arrayFaceIndex:
            facesToDraw.append(self.FACE_TABLE[index])
        facesToDraw.reverse()
        return facesToDraw

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