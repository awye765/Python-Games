import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

# Initialise pygame environment
pygame.init()
clock = pygame.time.Clock()

# Load image assets for title and game over screens
title_image = pygame.image.load("assets/title.jpg")
game_over_image = pygame.image.load("assets/game_over.jpg")

# Set game window
windowWidth = 400
windowHeight = 600

surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Drop!')

# Initialise variables for keyboard commands
leftDown = False
rightDown = False

# Initialise game start / end variables
gameStarted = False
gameEnded = False

# Initialise game platforms
gamePlatforms = []
platformSpeed = 3
platformDelay = 2000
lastPlatform = 0
platformsDroppedThrough = -1
dropping = False

# Initialise game timers
gameBeganAt = 0
timer = 0

# Initialise player
player = {
  "x" : windowWidth / 2,
  "y" : 0,
  "height" : 25,
  "width" : 10,
  "vy" : 5
}

# Draws player
def drawPlayer():

  pygame.draw.rect(surface, (255,0,0), (player["x"], player["y"], player["width"], player["height"]))


# Moves player
def movePlayer():

  global platformsDroppedThrough, dropping

  leftOfPlayerOnPlatform = True
  rightOfPlayerOnPlatform = True

  if surface.get_at(( int(player["x"]), int(player["y"]) + player["height"])) == (0,0,0,255):
    leftOfPlayerOnPlatform = False

  if surface.get_at(( int(player["x"]) + player["width"], int(player["y"]) + player["height"])) == (0,0,0,255):
    rightOfPlayerOnPlatform = False

  if leftOfPlayerOnPlatform is False and rightOfPlayerOnPlatform is False and (player["y"] + player["height"]) + player["vy"] < windowHeight:
    player["y"] += player["vy"]

    if dropping is False:
      dropping = True
      platformsDroppedThrough += 1

  else :

    foundPlatformTop = False
    yOffset = 0
    dropping = False

    while foundPlatformTop is False:

      if surface.get_at(( int(player["x"]), ( int(player["y"]) + player["height"]) - yOffset )) == (0,0,0,255):
        player["y"] -= yOffset
        foundPlatformTop = True
      elif (player["y"] + player["height"]) - yOffset > 0:
        yOffset += 1
      else :

        gameOver()
        break

  if leftDown is True:
    if player["x"] > 0 and player["x"] - 5 > 0:
      player["x"] -= 5
    elif player["x"] > 0 and player["x"] - 5 < 0:
      player["x"] = 0

  if rightDown is True:
    if player["x"] + player["width"] < windowWidth and (player["x"] + player["width"]) + 5 < windowWidth:
      player["x"] += 5
    elif player["x"] + player["width"] < windowWidth and (player["x"] + player["width"]) + 5 > windowWidth:
      player["x"] = windowWidth - player["width"]

# Draws platforms
def createPlatform():ß

  global lastPlatform, platformDelay

  platformY = windowHeight
  gapPosition = random.randint(0, windowWidth - 40)

  gamePlatforms.append({"pos" : [0, platformY], "gap" : gapPosition})
  lastPlatform = GAME_TIME.get_ticks()

  if platformDelay > 800:
    platformDelay -= 50

# Moves platforms
def movePlatforms():
  # print("Platforms")

  for idx, platform in enumerate(gamePlatforms):

    platform["pos"][1] -= platformSpeed

    if platform["pos"][1] < -10:
      gamePlatforms.pop(idx)

# Draws platforms
def drawPlatforms():

  for platform in gamePlatforms:

    pygame.draw.rect(surface, (255,255,255), (platform["pos"][0], platform["pos"][1], windowWidth, 10))
    pygame.draw.rect(surface, (0,0,0), (platform["gap"], platform["pos"][1], 40, 10) )

# Runs game over reset routine
def gameOver():

  global gameStarted, gameEnded

  platformSpeed = 0
  gameStarted = False
  gameEnded = True

# Restarts game
def restartGame():

  global gamePlatforms, player, gameBeganAt, platformsDroppedThrough, platformDelay

  gamePlatforms = []
  player["x"] = windowWidth / 2
  player["y"] = 0
  gameBeganAt = GAME_TIME.get_ticks()
  platformsDroppedThrough = -1
  platformDelay = 2000

# Quits game
def quitGame():

  pygame.quit()
  sys.exit()

# The 'main' loop
while True:

  surface.fill((0,0,0))

  for event in GAME_EVENTS.get():

    if event.type == pygame.KEYDOWN:

      if event.key == pygame.K_LEFT:
        leftDown = True
      if event.key == pygame.K_RIGHT:
        rightDown = True
      if event.key == pygame.K_ESCAPE:
        quitGame()

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT:
        leftDown = False
      if event.key == pygame.K_RIGHT:
        rightDown = False

      if event.key == pygame.K_SPACE:
        if gameStarted == False:
          restartGame()
          gameStarted = True

    if event.type == GAME_GLOBALS.QUIT:
      quitGame()

# If game has started, run below code
  if gameStarted is True:
    # Play game
    timer = GAME_TIME.get_ticks() - gameBeganAt

    # Works through every platform in the game and moves it up at the speed
    # set with the variable platformSpeed.  Also checks if a platform has
    # reached the top of the window.  If it has, it will remove that platform
    # from the gamePlatforms list.
    movePlatforms()
    drawPlatforms()
    movePlayer()
    drawPlayer()

# If game has ended, run below code
  elif gameEnded is True:
    # Draw game over screen
    surface.blit(game_over_image, (0, 150))

# In all other scenarios, i.e. game not yet started, nor ended, run below code
  else :
    # Draw Welcome Screen
    surface.blit(title_image, (0, 150))

  if GAME_TIME.get_ticks() - lastPlatform > platformDelay:
    createPlatform()

  clock.tick(60)
  pygame.display.update()
