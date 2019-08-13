import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

windowWidth = 600
windowHeight = 650

pygame.init()
surface = pygame.display.set_mode((windowWidth, windowHeight))

# Initialises variable to store the mousePosition
mousePosition = None

while True:
  # Creates white surface
  surface.fill((255,255,255))
  # Get initial mouse position
  mousePosition = pygame.mouse.get_pos()

  print(mousePosition)
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

  # Updates display
  pygame.display.update()
