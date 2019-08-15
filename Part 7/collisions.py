import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME

windowWidth = 1024
windowHeight = 768

pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption('Collisions')

# Variables to store mouse states
previousMousePosition = [0,0]
mousePosition = None
mouseDown = False

# Variables to store objects
collidables = []
currentObject = None

# Variable to store state of new objects, i.e. expanding or not.
expanding = True

drawAttractions = False

gravity = 1.0

# Draws collidables
def drawCollidables():

	for anObject in collidables:
		anObject["position"][0] += anObject["velocity"][0]
		anObject["position"][1] += anObject["velocity"][1]

		pygame.draw.circle(surface, (255,255,255), (int(anObject["position"][0]), int(anObject["position"][1])), int(anObject["radius"]), 0)

# Draws currentObject that user is dragging onto the surface upon mouse click.
def drawCurrentObject():

	global expanding, currentObject

	# Places currentObject at the user's x, y mouse coordinates.
	currentObject["position"][0] = mousePosition[0]
	currentObject["position"][1] = mousePosition[1]

	# expanding is set to TRUE by default.  This means upon holding the mouseDown
	# the object will continue to expand along its radius by 0.2 px each frame until
	# the object's radius exceeds 30 px, at which point it resets and shrinks.
	if expanding is True and currentObject["radius"] < 30:
		currentObject["radius"] += 0.2

		# If object's radius exceeds 30 px, expanding is reset to FALSE, and its
		# radius reset from 30+ px to 9.9 px.
		if currentObject["radius"] >= 30:
			expanding = False
			currentObject["radius"] = 9.9

	# If expanding is set to FALSE and current radius is greater than 1 the
	# object's radius is reduced by 0.2 px each frame.  Once the radius reduces
	# to <= 1 px, expanding is reset to TRUE and the object's radius reset to
	# 1.1 px.  Provided the mouse is still held down, the cycle repeats and the
	# object increases its radius incrementally each frame.
	elif expanding is False and currentObject["radius"] > 1:
		currentObject["radius"] -= 0.2

		if currentObject["radius"] <= 1:
			expanding = True
			currentObject["radius"] = 1.1

	currentObject["mass"] = currentObject["radius"]

	pygame.draw.circle(surface, (255,0,0), (int(currentObject["position"][0]), int(currentObject["position"][1])), int(currentObject["radius"]), 0)

# Calculates effect each object has on each other object.
def calculateMovement():

	# Iterates through each planet in the collidables list and checks its
	# affect on each other  collidable in the list.
	for anObject in collidables:

		for theOtherObject in collidables:
			# Checks otherObject =/= as current collidablet, i.e. because we do not
			# want to check a planet's affect against itself.
			if anObject is not theOtherObject:

				# DIRECTION: The difference in the X, Y coordinates of the objects
				direction = (theOtherObject["position"][0] - anObject["position"][0], theOtherObject["position"][1] - anObject["position"][1])

				# MAGNITUDE: The magnitude of the DISTANCE between the two objects
				magnitude = math.hypot(theOtherObject["position"][0] - anObject["position"][0], theOtherObject["position"][1] - anObject["position"][1])

				# NORMALISED VECTOR: pointing in the direction of the force.
				nDirection = (direction[0] / magnitude, direction[1] / magnitude)

				## We need to limit the gravity to stop things flying off to infinity... and beyond!
				if magnitude < 5:
					magnitude = 5
				elif magnitude > 15:
					magnitude = 15

				# Dividing by the magnitude accelerates the objects towards
				# each other, i.e. because the magnitude (i.e. distance between
				# the x, y coordinates of each plane) decreases and therefore
				# we are continually dividing a larger number by an increasingly
				# smaller number, which drives up the STRENGTH of the force.
				strength = ((gravity * anObject["mass"] * theOtherObject["mass"]) / (magnitude * magnitude)) / theOtherObject["mass"]

				# Calculates adjustment to the x, y coordinates of the
				#notherPlanet by a multiplying each x, y coordinate by strength.
				appliedForce = (nDirection[0] * strength, nDirection[1] * strength)

				# Applies the appliedForce to each x, y coordinate of the
				# otherPlanet.
				theOtherObject["velocity"][0] -= appliedForce[0]
				theOtherObject["velocity"][1] -= appliedForce[1]

				# Draws line between the planet and otherPlanet.
				if drawAttractions is True:
					pygame.draw.line(surface, (255,255,255), (anObject["position"][0],anObject["position"][1]), (theOtherObject["position"][0],theOtherObject["position"][1]), 1)

# Handles collisions
def handleCollisions():

	h = 0

	while h < len(collidables):

		i = 0

		anObject = collidables[h]

		while i < len(collidables):

			otherObject = collidables[i]

			# Only run the below if anObject is NOT the same referenced object
			# as otherObject.
			if anObject != otherObject:

				# Calculate DISTANCE between anObject and otherObject.
				distance = math.hypot(otherObject["position"][0] - anObject["position"][0], otherObject["position"][1] - anObject["position"][1])

				# If distance between centrepoints of each circular object is
				# LESS than their combined radiuses then we know for certain the
				# two objects have collided.  If so, we run the subsequent code.
				if distance < otherObject["radius"] + anObject["radius"]:

					# First we get the angle of the collision between the two
					# objects by essentially drawing an imaginary triangle
					# between the two objects and calculating the hypotenuse.
					collisionAngle = math.atan2(anObject["position"][1] - otherObject["position"][1], anObject["position"][0] - otherObject["position"][0])

					# hen we need to calculate the speed of each object.  This is
					# simply the hypotenuse of the triangle we might draw based
					# on the velocity of each object, i.e. the movements in the
					# x and y directions.  In other words this is the MAGNITUDE
					# of the x and y velocity of each object, which we calculate
					# using pythagorous theorem.
					anObjectSpeed = math.sqrt(anObject["velocity"][0] * anObject["velocity"][0] + anObject["velocity"][1] * anObject["velocity"][1])
					theOtherObjectSpeed = math.sqrt(otherObject["velocity"][0] * otherObject["velocity"][0] + otherObject["velocity"][1] * otherObject["velocity"][1])

					# Now, we work out the direction of the objects in radians
					anObjectDirection = math.atan2(anObject["velocity"][1], anObject["velocity"][0])
					theOtherObjectDirection = math.atan2(otherObject["velocity"][1], otherObject["velocity"][0])

					# Now we calculate the new X/Y values of each object for the collision
					anObjectsNewVelocityX = anObjectSpeed * math.cos(anObjectDirection - collisionAngle)
					anObjectsNewVelocityY = anObjectSpeed * math.sin(anObjectDirection - collisionAngle)

					otherObjectsNewVelocityX = theOtherObjectSpeed * math.cos(theOtherObjectDirection - collisionAngle)
					otherObjectsNewVelocityY = theOtherObjectSpeed * math.sin(theOtherObjectDirection - collisionAngle)

					# We adjust the velocity based on the mass of the objects
					anObjectsFinalVelocityX = ((anObject["mass"] - otherObject["mass"]) * anObjectsNewVelocityX + (otherObject["mass"] + otherObject["mass"]) * otherObjectsNewVelocityX)/(anObject["mass"] + otherObject["mass"])
					otherObjectsFinalVelocityX = ((anObject["mass"] + anObject["mass"]) * anObjectsNewVelocityX + (otherObject["mass"] - anObject["mass"]) * otherObjectsNewVelocityX)/(anObject["mass"] + otherObject["mass"])

					# Now we set those values
					anObject["velocity"][0] = anObjectsFinalVelocityX
					otherObject["velocity"][0] = otherObjectsFinalVelocityX


			i += 1

		h += 1

def handleMouseDown():
	global currentObject

	currentObject = {
		"radius" : 3,
		"mass" : 3,
		"velocity" : [0,0],
		"position" : [0,0]
	}

def quitGame():
	pygame.quit()
	sys.exit()

# 'main' loop
while True:

	surface.fill((0,0,0))
	mousePosition = pygame.mouse.get_pos()

	# Handle user and system events
	for event in GAME_EVENTS.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_ESCAPE:
				quitGame()

		if event.type == pygame.KEYUP:

			if event.key == pygame.K_r:
				collidables = []
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

	# Calculate the movements, handle the collisions, draw everything updated
	calculateMovement()
	handleCollisions()
	drawCollidables()

	if currentObject is not None:
		drawCurrentObject()

		# If our user has released the mouse, add the new Object to the collidables list and let gravity do its thing
		if mouseDown is False:
			currentObject["velocity"][0] = (mousePosition[0] - previousMousePosition[0]) / 4
			currentObject["velocity"][1] = (mousePosition[1] - previousMousePosition[1]) / 4
			collidables.append(currentObject)
			currentObject = None

	# Store the previous mouse coordinates to create a vector when we release a new anObject
	previousMousePosition = mousePosition

	clock.tick(60)
	pygame.display.update()

	# Calculating speed from velocity
	#
	# - https://www.youtube.com/watch?v=IK3I_lOWLuU