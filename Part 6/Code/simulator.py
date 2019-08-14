import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import solarsystem

windowWidth = 1024
windowHeight = 768

pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)

pygame.display.set_caption('Solar System Simulator')

previousMousePosition = [0,0]
mousePosition = None
mouseDown = False

background = pygame.image.load("assets/background.jpg")
logo = pygame.image.load("assets/logo.png")

UITab = pygame.image.load("assets/tabs.png")
UICoordinates = [{"name" : "mercury", "coordinates" : (132,687)},
				 {"name" : "venus", "coordinates" : (229,687)},
				 {"name" : "earth", "coordinates" : (326,687)},
				 {"name" : "mars", "coordinates" : (423,687)},
				 {"name" : "jupiter", "coordinates" : (520,687)},
				 {"name" : "saturn", "coordinates" : (617,687)},
				 {"name" : "neptune", "coordinates" : (713,687)},
				 {"name" : "uranus", "coordinates" : (810,687)}]

celestialBodies = []
currentBody = None

drawAttractions = True

gravity = 10.0

# Draws UI elements
def drawUI():
	surface.blit(UITab, (131,687))
	surface.blit(solarsystem.images["mercury"], (158,714))
	surface.blit(solarsystem.images["venus"], (247,706))
	surface.blit(solarsystem.images["earth"], (344,704))
	surface.blit(solarsystem.images["mars"], (451,714))
	surface.blit(solarsystem.images["jupiter"], (524,692))
	surface.blit(solarsystem.images["saturn"], (620,695))
	surface.blit(solarsystem.images["neptune"], (724,697))
	surface.blit(solarsystem.images["uranus"], (822,697))

# Draws planets
def drawPlanets():

	for planet in celestialBodies:
		planet["position"][0] += planet["velocity"][0]
		planet["position"][1] += planet["velocity"][1]
		surface.blit(solarsystem.images[planet["name"]], (planet["position"][0] - planet["radius"], planet["position"][1] - planet["radius"]))

# Draws currentBody that user is dragging onto the surface upon mouse click.
def drawCurrentBody():
	# Places currentBody at the user's x, y mouse coordinates.
	currentBody["position"][0] = mousePosition[0]
	currentBody["position"][1] = mousePosition[1]

	# Draws a soruce onto the surface: blit(source, dest, area=None, special_flags=0) -> Rect
	# Dest can be a pair of coordinates, as it is here:
	surface.blit(solarsystem.images[currentBody["name"]], (currentBody["position"][0] - currentBody["radius"], currentBody["position"][1] - currentBody["radius"]))

def calculateMovement():

	# Iterates through each planet in the celestialBodies list and checks its
	# affect on each other celestialBody in the list.
	for planet in celestialBodies:

		for otherPlanet in celestialBodies:
			# Checks otherPlanet =/= as current planet, i.e. because we do not
			# want to check a planet's affect against itself.
			if otherPlanet is not planet:
				# DIRECTION: The difference in the X, Y coordinates of the objects
				direction = (otherPlanet["position"][0] - planet["position"][0], otherPlanet["position"][1] - planet["position"][1])

				# MAGNITUDE: The distance between the two objects
				magnitude = math.hypot(otherPlanet["position"][0] - planet["position"][0], otherPlanet["position"][1] - planet["position"][1])

				# NORMALISED VECTOR: pointing in the direction of the force.
				nDirection = (direction[0] / magnitude, direction[1] / magnitude)

				## We need to limit the gravity to stop things flying off to infinity... and beyond!
				if magnitude < 5:
					magnitude = 5
				elif magnitude > 30:
					magnitude = 30

				# Dividing by the magnitude accelerates the objects towards
				# each other, i.e. because the magnitude (i.e. distance between
				# the x, y coordinates of each plane) decreases and therefore
				# we are continually dividing a larger number by an increasingly
				# smaller number, which drives up the STRENGTH of the force.
				strength = ((gravity * planet["mass"] * otherPlanet["mass"]) / (magnitude * magnitude)) / otherPlanet["mass"]

				# Calculates adjustment to the x, y coordinates of the
				#notherPlanet by a multiplying each x, y coordinate by strength.
				appliedForce = (nDirection[0] * strength, nDirection[1] * strength)

				# Applies the appliedForce to each x, y coordinate of the
				# otherPlanet.
				otherPlanet["velocity"][0] -= appliedForce[0]
				otherPlanet["velocity"][1] -= appliedForce[1]

				# Darws line between the planet and otherPlanet.
				if drawAttractions is True:
					pygame.draw.line(surface, (255,255,255), (planet["position"][0],planet["position"][1]), (otherPlanet["position"][0],otherPlanet["position"][1]), 1)

# Checks if UI clicked.
def checkUIForClick(coordinates):
	# Loops through each tab in UICoordinates
	for tab in UICoordinates:
		# Temporarily stores the x coordinate of each tab in UICoordinates for
		# purpose of confirming if mouse x coordinate inside UI element.
		tabX = tab["coordinates"][0]
		# If mouse x coordinate is inside x bounds of a UI element, then
		# return the corresponding "name" of that tab from UICoordinates.
		if coordinates[0] > tabX and coordinates[0] < tabX + 82:
			return tab["name"]

	return False

# Upon user click somewhere within the window, program checks if current
# position is inside a UI element and, IF SO, returns the name of the
# corresponding planet. That name is then used to create a planet corresponding
# to that named planet.
def handleMouseDown():
	global mousePosition, currentBody
	# Checks if mousePosition is at / below 687 px, i.e. where the UI elements
	# begin.
	if(mousePosition[1] >= 687):
		# Runs checkUIForClick and does so passing in the current mousePosition
		# coordinates.  If checkUIForClick identifies a planet, it will return
		# the new plane'ts name and store it in newPlanet variable.
		newPlanet = checkUIForClick(mousePosition)

		# If newPlanet found, i.e. user clicked on a UI element, then use the
		# makeNewPlanet function from solarsystem.py to create a planet that
		# corresponds to the variables for the named planet.
		if newPlanet is not False:
			currentBody = solarsystem.makeNewPlanet(newPlanet)


def quitGame():
	pygame.quit()
	sys.exit()

# 'main' loop
while True:

	mousePosition = pygame.mouse.get_pos()
	surface.blit(background, (0,0))

	# Handle user and system events
	for event in GAME_EVENTS.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_ESCAPE:
				quitGame()

		if event.type == pygame.KEYUP:

			if event.key == pygame.K_r:
				celestialBodies = []
			if event.key == pygame.K_a:
				if drawAttractions is True:
					drawAttractions = False
				elif drawAttractions is False:
					drawAttractions = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown = True
			handleMouseDown()

		if event.type == pygame.MOUSEBUTTONUP:
			mouseDown = False

		if event.type == GAME_GLOBALS.QUIT:
			quitGame()

	# Draw the UI; Update the movement of the planets; Draw the planets in their new positions.
	drawUI()
	calculateMovement()
	drawPlanets()

	# If our user has created a new planet, draw it where the mouse is
	if currentBody is not None:
		drawCurrentBody()

		# If our user has released the mouse, add the new planet to the
		# celestialBodies list and let gravity do its thing.  This is what sets
		# each planet moving off on initiation.  Test with a single planet in
		# play to see what is meant by this comment.  See also line 212 below!
		if mouseDown is False:
			currentBody["velocity"][0] = (mousePosition[0] - previousMousePosition[0]) / 4
			currentBody["velocity"][1] = (mousePosition[1] - previousMousePosition[1]) / 4
			celestialBodies.append(currentBody)
			currentBody = None

	# Draw the logo for the first four seconds of the program
	if GAME_TIME.get_ticks() < 4000:
		surface.blit(logo, (108,77))

	# Store the previous mouse coordinates to create a vector when we release a new planet
	previousMousePosition = mousePosition

	clock.tick(60)
	pygame.display.update()

# Vectors
#
# http://www.rasmus.is/uk/t/F/Su58k03.htm
#
# https://www.mathsisfun.com/algebra/vectors.html