import pygame, sys
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

# Pygame Variables
pygame.init()
clock = pygame.time.Clock()

windowWidth = 800
windowHeight = 800

surface = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Pygame Keyboard!')

# Square Variables

## Sets h x w dimension of square
playerSize = 20

## Sets x & y coordinates of square
playerX = (windowWidth / 2) - (playerSize / 2)
playerY = windowHeight - playerSize

## Sets velocity of adjustments to x and y variables
playerVX = 1.0
playerVY = 0.0

jumpHeight = 25.0

## Sets speeds for movement
moveSpeed = 1.0
maxSpeed = 10.0

## Sets gravity
gravity = 1.0

# Keyboard Variables
leftDown = False
rightDown = False
haveJumped = False

def move():

	global playerX, playerY, playerVX, playerVY, haveJumped, gravity

	# Move left
	if leftDown:

		#print("MOVED LEFT")

		#If we're already moving to the right, reset the moving speed and invert the direction

		if playerVX > 0.0:
			## Note on game start, playerVX = 1.0, therefore the above if runs the below code
			playerVX = moveSpeed
			playerVX = -playerVX
		# Make sure our square doesn't leave our window to the left
		if playerX > 0:
			playerX += playerVX
			#print("X coordinate is", playerX)
			#print("VX is", playerVX)
			# print("Move Speed is", moveSpeed)
	# Move right
	if rightDown:

		#print("MOVED RIGHT")

		# If we're already moving to the left reset the moving speed again
		if playerVX < 0.0:
			playerVX = moveSpeed
			
		# Make sure our square doesn't leave our window to the right
		if playerX + playerSize < windowWidth:
			playerX += playerVX
			#print("X coordinate is", playerX)
			#print("VX is", playerVX)
	# Is player travelling upwards at a speed > 1.0 pixel per frame?
	if playerVY > 1.0:
		# Reduces upward speed by 10% each frame until upward speed = 0
		playerVY = playerVY * 0.9
	# If not, i.e. when upward speed = 0, reset haveJumped to False
	else :
		playerVY = 0.0
		haveJumped = False

	# Is our square in the air? Better add some gravity to bring it back down!
	if playerY < windowHeight - playerSize:
		# Remember, top left corner of the Window is
		playerY += gravity
		gravity = gravity * 1.1
	else :
		playerY = windowHeight - playerSize
		gravity = 1.0

	playerY -= playerVY

	# Determines how far to move the player left or right
	if playerVX > 0.0 and playerVX < maxSpeed or playerVX < 0.0 and playerVX > -maxSpeed:
		if haveJumped == False:
			# Accelerates the player's speed in either direction whilst left or right held down
			playerVX = playerVX * 1.1

# How to quit our program
def quitGame():
	pygame.quit()
	sys.exit()

while True:

    # Refreshes the game's pixel surface
	surface.fill((0,0,0))

    # Draws the player square
	pygame.draw.rect(surface, (255,0,0), (playerX, playerY, playerSize, playerSize))

	# Get a list of all events that happened since the last redraw
	for event in GAME_EVENTS.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_LEFT:
				leftDown = True
			if event.key == pygame.K_RIGHT:
				rightDown = True
			if event.key == pygame.K_UP:
				if not haveJumped:
					haveJumped = True
					playerVY += jumpHeight
			if event.key == pygame.K_ESCAPE:
				quitGame()

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				leftDown = False
				playerVX = moveSpeed
			if event.key == pygame.K_RIGHT:
				rightDown = False
				playerVX = moveSpeed

		if event.type == GAME_GLOBALS.QUIT:
			quitGame()

	move()

	clock.tick(60)
	pygame.display.update()