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

# Initialise game platform variablesr
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
    # print("Platform Status: OFF")
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
    # print("Platform Status: ON")

    # Kickstarts while loop to check if player ON a platform.  Note that the
    # block and platform are moving at different speeds, hence when they meet
    # they don't touch at the edges, but overlap upon meeting.
    while foundPlatformTop is False:

      # If bottom x, y - yOffset px == BLACK the top of the platform has been
      # found.  The player object is then bumped up by -1 px along the y axis.
      if surface.get_at(( int(player["x"]), ( int(player["y"]) + player["height"]) - yOffset )) == (0,0,0,255):
        player["y"] -= yOffset
        foundPlatformTop = True
        # print("IF: Test")
        # print(("Player Y + Height: {}").format(player["y"] + player["height"]))
        # print(("Player Y + Height - yOffset: {}").format(player["y"] + player["height"] - yOffset))
        # print(("Platform Y: {}").format(gamePlatforms[0]))

      # Unless above satisfied, the below is run.  This updates yOffset by +1,
      # meaning that the next time the above if statement is run, we are checking
      # the next pixel up from the one previous along the y axis of the block.
      # This process repeats until we find a black pixel, at which point
      # foundPlatformTop is TRUE, and the while loop stopped.  Note that the only
      # colors on the surface when this while loop is run are black (background)
      # and white (the platform) as the block is drawn after the player movement
      # is finalised.  See also diagram in "assets" folder to visualise how this
      # while loop works in practice.
      elif (player["y"] + player["height"]) - yOffset > 0:
        yOffset += 1
        # print("ELIF: Test")
        # print(("Player Y + Height: {}").format(player["y"] + player["height"]))
        # print(("Player Y + Height - yOffset: {}").format(player["y"] + player["height"] - yOffset))
        # print(("Platform Y: {}").format(gamePlatforms[0]))

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
# CREATE PLATFORM OBJECT
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

  # Returns elapsed game time at time platform created
  lastPlatform = GAME_TIME.get_ticks()

# Reduces the platformDelay interval by 50ms each time a platform is created
# until the minimum delay is only 800ms, down from a starting delay of 2000ms
  if platformDelay > 800:
    platformDelay -= 50

# ------------------------------------------------------------------------------
# MOVE PLATFORM
# ------------------------------------------------------------------------------

def movePlatforms():
  # print("Platforms")

  for idx, platform in enumerate(gamePlatforms):
    # For each platform update its y co-ord by platformSpeed (i.e. - 3px) to
    # move it up toward the top of the screen by 3px
    platform["pos"][1] -= platformSpeed

    # Checks if each platform is completely above top of the screen and, IF SO
    # removes the platform from the platform list.
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
  # has been since the last platform we subtract lastPlatform (time elapsed at
  # platform's creation) from the game's TOTAL runtime to date (i.e.
  # GAME_TIME.get_ticks()) and IF this is greater than platformDelay,create a
  # new platform
  if GAME_TIME.get_ticks() - lastPlatform > platformDelay:
    createPlatform()

# ------------------------------------------------------------------------------
# SETS GAME FRAME RATE
# ------------------------------------------------------------------------------

  # Runs program at 60 frames per secosnd
  clock.tick(5)

# ------------------------------------------------------------------------------
# UPDATES GAME DISPLAY
# ------------------------------------------------------------------------------

  # Updates game display
  pygame.display.update()
