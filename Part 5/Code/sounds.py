import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

windowWidth = 600
windowHeight = 650

pygame.init()
surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Soundboard')

# Creates buttons variable as empty list
buttons = []

# Creates stop button variable to store loaded stop image for use as button
stopButton = { "image" : pygame.image.load("assets/images/stop.png"), "position" : (275, 585)}

# Initialises variable to store the mousePosition
mousePosition = None

# Initialises variable to store the volume, setting it to 1.0 initially, i.e.
# full volume.
volume = 1.0

# Initiates pygame.mixer
pygame.mixer.init()
# Loads mixer with the background farm.OGG music from OGG directory
pygame.mixer.music.load('assets/sounds/OGG/farm.ogg')
# Plays the background music on loop forever (denoted by the (-1)).  The number
# value can be used to set how many times the music is looped, e.g. 1, 2, 3 times
# and so on.
pygame.mixer.music.play(-1)

# Draws buttons
def drawButtons():
  # Loops through each button in the buttons list and "blits" them onto the
  # surface.  "Blitting" is essentially pygame's equivalent of a paste function.
  for button in buttons:
    surface.blit(button["image"], button["position"])

  surface.blit(stopButton["image"], stopButton['position'])

# Draws volume slider button
def drawVolume():
  # Draws VERTICAL element of the slider.  The x, y co-ordinates (drawn from
  # top left of the surface) are 450, 610.  The width and height of the rectangle
  # are 100, 5 respectively.
  pygame.draw.rect(surface, (229, 229, 229), (450, 610, 100, 5))

  volumePosition = (100 / 100) * (volume * 100)
  # Draws HORIZONTAL element of the slider. he x, y co-ordinates (drawn from
  # top left of the surface) are 450 + volumePosition, 610.  The width and height
  # of the rectangle are 10, 2g5 respectively.
  pygame.draw.rect(surface, (204, 204, 204), (450 + volumePosition, 600, 10, 25))

# Determines what happens immediately following a mouse click.
def handleClick():

  global mousePosition, volume

  for button in buttons:
    # Returns the size and position of each button in buttons
    buttonSize = button['image'].get_rect().size
    buttonPosition = button['position']
    # Checks if mousePosition x co-ordinate at click is inside or outside of
    # each button.
    if mousePosition[0] > buttonPosition[0] and mousePosition[0] < buttonPosition[0] + buttonSize[0]:
      # Checks is mousePosition y co-ordinate at click is inside or outside of
      # each button.
      if mousePosition[1] > buttonPosition[1] and mousePosition[1] < buttonPosition[1] + buttonSize[1]:
        # If both conditions above are TRUE, i.e. mouse click was INSIDE a buttons
        # then pygame plays the sound of the corresponding button to the level of
        # volume set at that time.
        button['sound'].set_volume(volume)
        button['sound'].play()
    # Checks if mouse position at click is inside or outside of the stopButton.
    # Same logic as above, albeit for the stopButton.
    if mousePosition[0] > stopButton['position'][0] and mousePosition[0] < stopButton['position'][0] + stopButton['image'].get_rect().size[0]:
      if mousePosition[1] > stopButton['position'][1] and mousePosition[1] < stopButton['position'][1] + stopButton['image'].get_rect().size[1]:
        # Stops the pygame.mixer
        pygame.mixer.stop()

def checkVolume():

  global mousePosition, volume

  if pygame.mouse.get_pressed()[0] == True:
    # If left mouse button HELD DOWN within volumen slider position run loop.
    if mousePosition[1] > 600 and mousePosition[1] < 625:
      if mousePosition[0] > 450 and mousePosition[0] < 550:
        # Volume function takes a value between 0.0 (mute) and 1.0 (full volume).
        # If you pass volume() a value > 1.0 it becomes 1.0.  If you pass it a
        # value of < 0.0 it becomes 0.0.
        #
        # If left button IS held down, user trying to drag volume slider to the
        # position they desire.  SO we work out where the mouse is between 0.0
        # and 1.0 and set the volume to the new level.
        #
        # Because drawVolume is run immediately after this function, the adjusted
        # positio of the slider is re-drawn after the user adjusts the slider.
        volume = float((mousePosition[0] - 450)) / 100

def quitGame():
  pygame.quit()
  sys.exit()

# Create Buttons
## Appends each button as a dictionary item to the buttons list.  Each buttons
## dictionary item has three keys: (1) image, (2) position and (3) sound.  The
## last item in the dictionary ensures each sound is loaded as a pygame sound
## object.  This allows us to control the quality of the sound, e.g. volume etc.
buttons.append({ "image" : pygame.image.load("assets/images/sheep.png"), "position" : (25, 25), "sound" : pygame.mixer.Sound('assets/sounds/OGG/sheep.ogg')})
buttons.append({ "image" : pygame.image.load("assets/images/rooster.png"), "position" : (225, 25), "sound" : pygame.mixer.Sound('assets/sounds/OGG/rooster.ogg')})
buttons.append({ "image" : pygame.image.load("assets/images/pig.png"), "position" : (425, 25), "sound" : pygame.mixer.Sound('assets/sounds/OGG/pig.ogg')})
buttons.append({ "image" : pygame.image.load("assets/images/mouse.png"), "position" : (25, 225), "sound" : pygame.mixer.Sound('assets/sounds/OGG/mouse.ogg')})
buttons.append({ "image" : pygame.image.load("assets/images/horse.png"), "position" : (225, 225), "sound" : pygame.mixer.Sound('assets/sounds/OGG/horse.ogg')})
buttons.append({ "image" : pygame.image.load("assets/images/dog.png"), "position" : (425, 225), "sound" : pygame.mixer.Sound('assets/sounds/OGG/dog.ogg')})
buttons.append({ "image" : pygame.image.load("assets/images/cow.png"), "position" : (25, 425), "sound" : pygame.mixer.Sound('assets/sounds/OGG/cow.ogg')})
buttons.append({ "image" : pygame.image.load("assets/images/chicken.png"), "position" : (225, 425), "sound" : pygame.mixer.Sound('assets/sounds/OGG/chicken.ogg')})
buttons.append({ "image" : pygame.image.load("assets/images/cat.png"), "position" : (425, 425), "sound" : pygame.mixer.Sound('assets/sounds/OGG/cat.ogg')})

# 'main' loop
while True:
  # Creates white surface
  surface.fill((255,255,255))
  # Get initial mouse position
  mousePosition = pygame.mouse.get_pos()
  # Listen for mouse events
  for event in GAME_EVENTS.get():
    # Listens for ESC key being pressed and, if so, quits game
    if event.type == pygame.KEYDOWN:

      if event.key == pygame.K_ESCAPE:
        quitGame()

    if event.type == GAME_GLOBALS.QUIT:
      quitGame()
    # Listens for mouse click having been released, i.e. because mouse button
    # has to pop up after it's been clicked unless the button is being held
    # down.
    if event.type == pygame.MOUSEBUTTONUP:
      # Calls the handleClick function if button has been clicked and released.
      handleClick()
  # Draws buttons, checks volume and draws volume
  drawButtons()
  checkVolume()
  drawVolume()
  # Updates display
  pygame.display.update()
