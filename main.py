import renderer
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# This is the main game loop, it constantly runs until you press the Q KEY or close the window.
def main(self):
    pygame.init()  # Initial Setup
    self._WIN = pygame.display.set_mode(self.SCREENSIZE)

# GUI:
    outputRot = TextBox(self._WIN, 75, 5, 65, 20, fontSize=20, borderThickness=2)
    outputRot.setText("Rotation")
    outputRot.disable()  # Act as label instead of textbox

    sliderRotX = Slider(self._WIN, 25, 25, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputRotX = TextBox(self._WIN, 30, 35, 20, 20, fontSize=20, borderThickness=2)
    outputRotX.setText("X")
    outputRotX.disable()  # Act as label instead of textbox

    sliderRotY = Slider(self._WIN, 90, 25, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputRotY = TextBox(self._WIN, 95, 35, 20, 20, fontSize=20, borderThickness=2)
    outputRotY.setText("Y")
    outputRotY.disable()  # Act as label instead of textbox

    sliderRotZ = Slider(self._WIN, 155, 25, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputRotZ = TextBox(self._WIN, 160, 35, 20, 20, fontSize=20, borderThickness=2)
    outputRotZ.setText("Z")
    outputRotZ.disable()  # Act as label instead of textbox

    sliderFill = Slider(self._WIN, self.WIDTH-55, 25, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputFill = TextBox(self._WIN, self.WIDTH-60, 40, 40, 20, fontSize=20, borderThickness=2)
    outputFill.setText("FILL")
    outputFill.disable()  # Act as label instead of textbox

    sliderNum = Slider(self._WIN, self.WIDTH-55, 75, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputNum = TextBox(self._WIN, self.WIDTH-60, 90, 40, 20, fontSize=20, borderThickness=2)
    outputNum.setText("NUM")
    outputNum.disable()  # Act as label instead of textbox

    sliderTransX = Slider(self._WIN, self.WIDTH-120, 25, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputTransX = TextBox(self._WIN, self.WIDTH-135, 40, 60, 20, fontSize=20, borderThickness=2)
    outputTransX.setText("Trans X")
    outputTransX.disable()  # Act as label instead of textbox

    sliderTransY = Slider(self._WIN, self.WIDTH-120, 75, 30, 15, min=0, max=1, step=1, handleColour=(180,0,0), initial=0)
    outputTransY = TextBox(self._WIN, self.WIDTH-135, 90, 60, 20, fontSize=20, borderThickness=2)
    outputTransY.setText("Trans Y")
    outputTransY.disable()  # Act as label instead of textbox

    sliderFocalLength = Slider(self._WIN, 25, self.HEIGHT-40, 200, 15, min=50, max=400, step=2, handleColour=(180,0,0), initial=self.focal_length)
    outputFocalLength = TextBox(self._WIN, 88, self.HEIGHT-62, 74, 25, fontSize=20)
    outputFocalLength.disable()  # Act as label instead of textbox

    sliderFPS = Slider(self._WIN, self.WIDTH-225, self.HEIGHT-40, 200, 15, min=1, max=200, step=10,handleColour=(180,0,0), initial=self.GAME_FPS)
    outputFPS = TextBox(self._WIN, self.WIDTH-165, self.HEIGHT-62, 84, 25, fontSize=20)
    outputFPS.disable()  # Act as label instead of textbox

    PO = [0]*8
    for i in range(8):
        PO[i] = TextBox(self._WIN, 0, 0, 0, 0, fontSize=20, borderThickness=2, textColour=(255,255,255))
        PO[i].setText(i)
        PO[i].disable()  # Act as label instead of textbox

    while self.running:
        pygame.time.Clock().tick(self.GAME_FPS)
        self.checkEvents()
        self.focal_length = sliderFocalLength.getValue()
        outputFocalLength.setText("Focal: " + str(sliderFocalLength.getValue()))
        self.GAME_FPS = sliderFPS.getValue()
        outputFPS.setText(str(sliderFPS.getValue()) + " tick/sec")

        # Activate the rotation tag when sliders are turn on
        self.rotX=True if sliderRotX.getValue()==1 else False
        self.rotY=True if sliderRotY.getValue()==1 else False
        self.rotZ=True if sliderRotZ.getValue()==1 else False
        self.fill=True if sliderFill.getValue()==1 else False
        self.transX=True if sliderTransX.getValue()==1 else False
        self.transY=True if sliderTransY.getValue()==1 else False

        # Fill the background
        self._WIN.fill(self.BACKGROUND_COLOR)
        self.gradientRect(self.BACKGROUND_BORDER_GRADIENT, self.BACKGROUND_CENTER_GRADIENT,
                            pygame.Rect(0,0, self.WIDTH,self.HEIGHT) )

        # Apply rotation in the 3D space
        self.rotateOnAxis()
        # Apply move on vertex
        self.moveVertexOnAxis()
        # Generate projected table
        self.projectVertices()
        # Apply move on projected point
        #self.moveOnAxis()

        if sliderNum.getValue() == 1 :
            for i in range(8):
                PO[i].setX(self.PROJECTED_VERTEX_TABLE[i][0]);PO[i].setY(self.PROJECTED_VERTEX_TABLE[i][1])  
        else:
            for i in range(8):
                PO[i].setX(0);PO[i].setY(0)

        # Draw the lines
        self.drawLine()

        if(self.fill):
            # Fill the faces
            self.drawPolygon()

        pygame_widgets.update(pygame.event.get())
        pygame.display.flip()

if __name__ == '__main__':
    object = renderer.Renderer
    main(object)