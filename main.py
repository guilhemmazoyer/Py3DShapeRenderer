import renderer
import sys, math
import pygame
from pygame.locals import KEYDOWN, K_q
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# This is the main game loop, it constantly runs until you press the Q KEY or close the window.
def main(self):
    pygame.init()  # Initial Setup
    self._WIN = pygame.display.set_mode(self.SCREENSIZE)

# GUI:
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

    sliderFocalLength = Slider(self._WIN, 25, self.HEIGHT-40, 200, 15, min=50, max=400, step=2, handleColour=(180,0,0), initial=self.focal_length)
    outputFocalLength = TextBox(self._WIN, 105, self.HEIGHT-62, 40, 25, fontSize=20)
    outputFocalLength.disable()  # Act as label instead of textbox

    while self.running:
        self.checkEvents()
        self.focal_length = sliderFocalLength.getValue()

        if(sliderRotX.getValue() == 1) :
            self.rotX = True
        else:
            self.rotX = False
        if(sliderRotY.getValue() == 1) :
            self.rotY = True
        else:
            self.rotY = False

        if(sliderRotZ.getValue() == 1) :
            self.rotZ = True
        else:
            self.rotZ = False

        # Fill the background
        self._WIN.fill(self.BACKGROUND_COLOR)

        # Draw the lines
        for line in self.EDGE_TABLE :
            self.drawLine(line)

        # Fill the faces
        for face in self.FACE_TABLE:
            self.drawPolygon(face)
        
        # Apply rotation and focal length
        outputFocalLength.setText(sliderFocalLength.getValue())
        self.rotateOnAxis()

        pygame_widgets.update(pygame.event.get())
        pygame.display.update()
        pygame.time.Clock().tick(self.GAME_FPS)

if __name__ == '__main__':
    object = renderer.Renderer
    main(object)