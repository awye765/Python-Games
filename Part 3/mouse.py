import pygame, sys
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

# Pygame Variables
pygame.init()
clock = pygame.time.Clock()

windowWidth = 800
windowHeight = 800

surface = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption('Pygame Mouse!')

# Mouse Variables
mousePosition = None
mousePressed = False

# Square Variables
squareSize = 40
squareColor = (255, 0, 0)
squareX = windowWidth / 2
squareY = windowHeight - squareSize
draggingSquare = False
gravity = 5.0

# Checks if cursor within boundary of the square
def checkBounds():

	global squareColor, squareX, squareY, draggingSquare

	# We only care to check if cursor within Square if the mouse is pressed
	if mousePressed == True:
		# Is our cursor's x co-ordinate (mousePosition[0]) over our square?
		if mousePosition[0] > squareX and mousePosition[0] < squareX + squareSize:
			# Is our cursor's y co-ordinate (mousePosition[1]) over our square?
			if mousePosition[1] > squareY and mousePosition[1] < squareY + squareSize:
				# Then allow square to be dragged by cursor
				draggingSquare = True
				# Makes cursor invisible when cursor pressed + over Square
				pygame.mouse.set_visible(0)

	else :
		# Resets Square color to red (from Green, which is the color if Square dragged)
		squareColor = (255,0,0)
		# Resets cursor visibility, i.e. so it is visible again
		pygame.mouse.set_visible(1)
		# Resets drag variable
		draggingSquare = False

# Checks gravity
def checkGravity():

	global gravity, squareY, squareSize, windowHeight

	# Is our square in the air and have we let go of it?
	if squareY < windowHeight - squareSize and mousePressed == False:
		squareY += gravity
		gravity = gravity * 1.1
	else :
		squareY = windowHeight - squareSize
		gravity = 5.0

# Draws Square
def drawSquare():

	global squareColor, squareX, squareY, draggingSquare

	# Changes Square color to green if Square being dragged
	if draggingSquare == True:

		squareColor = (0, 255, 0)
		squareX = mousePosition[0] - squareSize / 2
		squareY = mousePosition[1] - squareSize / 2

	pygame.draw.rect(surface, squareColor, (squareX, squareY, squareSize, squareSize))

# How to quit our program
def quitGame():
	pygame.quit()
	sys.exit()

while True:
	# Retrieves position of mouse; returns x, y values of the mouse co-ordinates
	mousePosition = pygame.mouse.get_pos()

	surface.fill((0,0,0))

	# Check whether mouse is pressed down; returns tuple with three values,
	# the first = left button, the second = middle button and third = right button.
	# Below line checks if left button of mouse is pressed.
	if pygame.mouse.get_pressed()[0] == True:
		mousePressed = True
	else :
		mousePressed = False

	checkBounds()
	checkGravity()
	drawSquare()

	clock.tick(60)
	pygame.display.update()

	for event in GAME_EVENTS.get():

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quitGame()

		if event.type == GAME_GLOBALS.QUIT:
			quitGame()