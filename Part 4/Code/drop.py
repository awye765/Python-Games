import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME


# ------------------------------------------------------------------------------
# INITIALISE GAME
# ------------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------
# DRAW PLAYER
# ------------------------------------------------------------------------------

def drawPlayer():
  # Draws player Square in color red (255, 0, 0) at x, y co-ords with width 10
  # and height 25.
  pygame.draw.rect(surface, (255,0,0), (player["x"], player["y"], player["width"], player["height"]))

# ------------------------------------------------------------------------------
# MOVE PLAYER
# ------------------------------------------------------------------------------

def movePlayer():

  global platformsDroppedThrough, dropping

  # ----------------------------------------------------------------------------
  # CODE TO CHECK IF PLAYER ON PLATFORM
  # ----------------------------------------------------------------------------
  # Variables store state regarding whether bottom corners of Square are on or
  # off of a platform
  leftOfPlayerOnPlatform = True
  rightOfPlayerOnPlatform = True

  # Checks if surface beneath Square's bottom LEFT is BLACK (0,0,0,255) and
  # IF SO, updates leftOfPlayerOnPlatform variable to False.
  if surface.get_at(( int(player["x"]), int(player["y"]) + player["height"])) == (0,0,0,255):
    leftOfPlayerOnPlatform = False

  # Checks if surface beneath Square's bottom RIGHT is BLACK (0,0,0,255) and
  # IF SO, updates rightOfPlayerOnPlatform variable to False.
  if surface.get_at(( int(player["x"]) + player["width"], int(player["y"]) + player["height"])) == (0,0,0,255):
    rightOfPlayerOnPlatform = False

  # ----------------------------------------------------------------------------
  # CODE IF PLAYER NOT ON A PLATFORM
  # ----------------------------------------------------------------------------

  # Checks if BOTH bottom LEFT and RIGHT of Square are on a BLACK surface AND
  # that player is not at bottom of screen, move player down by vy, i.e. 5 px.
  if leftOfPlayerOnPlatform is False and rightOfPlayerOnPlatform is False and (player["y"] + player["height"]) + player["vy"] < windowHeight:

    # Update player's y co-ord by adding vy velocity, i.e. pulling player
    # down toward bottom of screen
    player["y"] += player["vy"]

    # Update dropping variable to indicate player IS dropping and update the
    # number of platformsDroppedThrough by +1
    if dropping is False:
      dropping = True
      platformsDroppedThrough += 1

  # ----------------------------------------------------------------------------
  # CODE IF PLAYER IS ON A PLATFORM
  # ----------------------------------------------------------------------------

  else :
    # Initialises variables necessary to determine interaction of player on a
    # platform
    foundPlatformTop = False
    yOffset = 0
    dropping = False

    # Kickstarts while loop to check if player ON a platform
    while foundPlatformTop is False:

      if surface.get_at(( int(player["x"]), ( int(player["y"]) + player["height"]) - yOffset )) == (0,0,0,255):
        player["y"] -= yOffset
        foundPlatformTop = True
      elif (player["y"] + player["height"]) - yOffset > 0:
        yOffset += 1
      else :
        # If we don't find a BLACK px before we reach the top of the surface
        # then it's GAME OVER.
        gameOver()
        break

  # ----------------------------------------------------------------------------
  # CODE TO MOVE PLAYER
  # ----------------------------------------------------------------------------

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

# ------------------------------------------------------------------------------
# CREATE PLATFORM
# ------------------------------------------------------------------------------

# Creates platform object
def createPlatform():

  global lastPlatform, platformDelay

  # Sets platform y co-ord to window height, i.e. bottom of screen (600 px)
  platformY = windowHeight
  # Sets gapPosition to a random integer b/t 0 and windowWidth - 40 (360).  This
  # is used to identify the x co-ord of the gap
  gapPosition = random.randint(0, windowWidth - 40)

  # Create variable gamePlatforms and append co-ords for platform + gap
  gamePlatforms.append({"pos" : [0, platformY], "gap" : gapPosition})

  #
  lastPlatform = GAME_TIME.get_ticks()

  if platformDelay > 800:
    platformDelay -= 50

# ------------------------------------------------------------------------------
# MOVE PLATFORM
# ------------------------------------------------------------------------------

def movePlatforms():
  # print("Platforms")

  for idx, platform in enumerate(gamePlatforms):

    platform["pos"][1] -= platformSpeed

    if platform["pos"][1] < -10:
      gamePlatforms.pop(idx)

# ------------------------------------------------------------------------------
# DRAW PLATFORMS
# ------------------------------------------------------------------------------

def drawPlatforms():

  for platform in gamePlatforms:
    # Draws a white rectangle (255, 255, 255) at x, y co-ords with windowWidth
    # and height 10 px.
    pygame.draw.rect(surface, (255,255,255), (platform["pos"][0], platform["pos"][1], windowWidth, 10))
    # Draws a black rectangle (0, 0, 0) at x, y co-ords with width 40 px and
    # height 10 px.  I.e. is overlapped on top of the white rectangle.
    pygame.draw.rect(surface, (0,0,0), (platform["gap"], platform["pos"][1], 40, 10) )

# ------------------------------------------------------------------------------
# GAME RESET ROUTINES
# ------------------------------------------------------------------------------

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

  # Color the surface black
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

# ------------------------------------------------------------------------------
# PLATFORM CREATION INTERVAL CONTROLLER
# ------------------------------------------------------------------------------
  # Creates a platform around every 2 seconds.  The get_ticks function returns
  # the legnth of time for which the game has been running.  To see how long it
  # has been since the last platform we subjtract lastPlatform from the runtime
  # (i.e. GAME_TIME.get_ticks()) and IF this is greater than platformDelay,
  # create a new platform
  if GAME_TIME.get_ticks() - lastPlatform > platformDelay:
    createPlatform()

# ------------------------------------------------------------------------------
# SETS GAME FRAME RATE
# ------------------------------------------------------------------------------

  # Runs program at 60 frames per second
  clock.tick(60)

# ------------------------------------------------------------------------------
# UPDATES GAME DISPLAY
# ------------------------------------------------------------------------------

  # Updates game display
  pygame.display.update()
