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

    sliderFocalLength = Slider(self._WIN, 25, self.HEIGHT-40, 200, 15, min=50, max=400, step=2, handleColour=(180,0,0), initial=self.focal_length)
    outputFocalLength = TextBox(self._WIN, 88, self.HEIGHT-62, 74, 25, fontSize=20)
    outputFocalLength.disable()  # Act as label instead of textbox

    sliderFPS = Slider(self._WIN, self.WIDTH-225, self.HEIGHT-40, 200, 15, min=1, max=200, step=10, handleColour=(180,0,0), initial=self.GAME_FPS)
    outputFPS = TextBox(self._WIN, self.WIDTH-165, self.HEIGHT-62, 84, 25, fontSize=20)
    outputFPS.disable()  # Act as label instead of textbox

    Po0 = TextBox(self._WIN, 0, 0, 0, 0, fontSize=20, borderThickness=2, textColour=(255,255,255))
    Po0.setText("0")
    Po0.disable()  # Act as label instead of textbox
    Po1 = TextBox(self._WIN, 0, 0, 0, 0, fontSize=20, borderThickness=2, textColour=(255,255,255))
    Po1.setText("1")
    Po1.disable()  # Act as label instead of textbox
    Po2 = TextBox(self._WIN, 0, 0, 0, 0, fontSize=20, borderThickness=2, textColour=(255,255,255))
    Po2.setText("2")
    Po2.disable()  # Act as label instead of textbox
    Po3 = TextBox(self._WIN, 0, 0, 0, 0, fontSize=20, borderThickness=2, textColour=(255,255,255))
    Po3.setText("3")
    Po3.disable()  # Act as label instead of textbox
    Po4 = TextBox(self._WIN, 0, 0, 0, 0, fontSize=20, borderThickness=2, textColour=(255,255,255))
    Po4.setText("4")
    Po4.disable()  # Act as label instead of textbox
    Po5 = TextBox(self._WIN, 0, 0, 0, 0, fontSize=20, borderThickness=2, textColour=(255,255,255))
    Po5.setText("5")
    Po5.disable()  # Act as label instead of textbox
    Po6 = TextBox(self._WIN, 0, 0, 0, 0, fontSize=20, borderThickness=2, textColour=(255,255,255))
    Po6.setText("6")
    Po6.disable()  # Act as label instead of textbox
    Po7 = TextBox(self._WIN, 0, 0, 0, 0, fontSize=20, borderThickness=2, textColour=(255,255,255))
    Po7.setText("7")
    Po7.disable()  # Act as label instead of textbox


    while self.running:
        pygame.time.Clock().tick(self.GAME_FPS)
        self.checkEvents()
        self.focal_length = sliderFocalLength.getValue()
        outputFocalLength.setText("Focal: " + str(sliderFocalLength.getValue()))
        self.GAME_FPS = sliderFPS.getValue()
        outputFPS.setText(str(sliderFPS.getValue()) + " tick/sec")

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
        if(sliderFill.getValue() == 1) :
            self.fill = True
        else:
            self.fill = False

        # Fill the background
        self._WIN.fill(self.BACKGROUND_COLOR)

        if sliderNum.getValue() == 1 :
            Po0.setX(self.project3DOn2DScreen(self.VERTEX_TABLE[0])[0])
            Po0.setY(self.project3DOn2DScreen(self.VERTEX_TABLE[0])[1])
            Po1.setX(self.project3DOn2DScreen(self.VERTEX_TABLE[1])[0])
            Po1.setY(self.project3DOn2DScreen(self.VERTEX_TABLE[1])[1])
            Po2.setX(self.project3DOn2DScreen(self.VERTEX_TABLE[2])[0])
            Po2.setY(self.project3DOn2DScreen(self.VERTEX_TABLE[2])[1])
            Po3.setX(self.project3DOn2DScreen(self.VERTEX_TABLE[3])[0])
            Po3.setY(self.project3DOn2DScreen(self.VERTEX_TABLE[3])[1])
            Po4.setX(self.project3DOn2DScreen(self.VERTEX_TABLE[4])[0])
            Po4.setY(self.project3DOn2DScreen(self.VERTEX_TABLE[4])[1])
            Po5.setX(self.project3DOn2DScreen(self.VERTEX_TABLE[5])[0])
            Po5.setY(self.project3DOn2DScreen(self.VERTEX_TABLE[5])[1])
            Po6.setX(self.project3DOn2DScreen(self.VERTEX_TABLE[6])[0])
            Po6.setY(self.project3DOn2DScreen(self.VERTEX_TABLE[6])[1])
            Po7.setX(self.project3DOn2DScreen(self.VERTEX_TABLE[7])[0])
            Po7.setY(self.project3DOn2DScreen(self.VERTEX_TABLE[7])[1])
        else:
            Po0.setX(0)
            Po0.setY(0)
            Po1.setX(0)
            Po1.setY(0)
            Po2.setX(0)
            Po2.setY(0)
            Po3.setX(0)
            Po3.setY(0)
            Po4.setX(0)
            Po4.setY(0)
            Po5.setX(0)
            Po5.setY(0)
            Po6.setX(0)
            Po6.setY(0)
            Po7.setX(0)
            Po7.setY(0)

        # Draw the lines
        for line in self.EDGE_TABLE :
            self.drawLine(line)

        if(self.fill):
            # Fill the faces
            for face in self.FACE_TABLE:
                self.drawPolygon()
        
        # Apply rotation
        self.rotateOnAxis()

        pygame_widgets.update(pygame.event.get())
        pygame.display.update()

if __name__ == '__main__':
    object = renderer.Renderer
    main(object)