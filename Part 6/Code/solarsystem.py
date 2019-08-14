import pygame, copy

# Dictionary store of planet images assigned to their name labels
images = {
	"mercury" : pygame.image.load("assets/mercury.png"),
	"venus" : pygame.image.load("assets/venus.png"),
	"earth" : pygame.image.load("assets/earth.png"),
	"mars" : pygame.image.load("assets/mars.png"),
	"jupiter" : pygame.image.load("assets/jupiter.png"),
	"saturn" : pygame.image.load("assets/saturn.png"),
	"neptune" : pygame.image.load("assets/neptune.png"),
	"uranus" : pygame.image.load("assets/uranus.png"),
}

# List storing dictionary of planet variables
planets = [{
	"name" : "mercury",
	"radius" : 15.0,
	"mass" : 0.6,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "venus",
	"radius" : 23.0,
	"mass" : 0.95,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "earth",
	"radius" : 24.0,
	"mass" : 1.0,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "mars",
	"radius" : 15.0,
	"mass" : 0.4,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "jupiter",
	"radius" : 37.0,
	"mass" : 15.0,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "saturn",
	"radius" : 30.0,
	"mass" : 4,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "neptune",
	"radius" : 30.0,
	"mass" : 4.2,
	"velocity" : [0,0],
	"position" : [0,0]
},
{
	"name" : "uranus",
	"radius" : 30.0,
	"mass" : 3.8,
	"velocity" : [0,0],
	"position" : [0,0]
}]

# Creates each newPlanet
def makeNewPlanet(which):
	# Iterates through each pieceOfRock currently stored in planets
	for pieceOfRock in planets:
		# Checks which planet in planets has identical name to the user clicked
		# planet name and once it finds a match, creates a deepcopy of a planet
		# object with the corresponding variables.  See below re deepcopy.
		if pieceOfRock["name"] == which:
			return copy.deepcopy(pieceOfRock)

	return False

# DEEPCOPY
#
# When you create a variable you make a pointer to an object.  Sometimes you
# want to create a copy of the underlying object that you can modify WITHOUT
# automatically modifying the original object at the same time.  To do so you
# can use the deepcopy method.
#
# A deep copy makes the copying process recursive. It means first constructing a
# NEW collection object and then recursively populating it with COPIES of the
# child objects found in the original rather than REFERENCES. Copying an object
# this way walks the whole object tree to create a fully independent clone of
# the original object and all of its children.
#
# By contrast, a shallow copy means constructing a new collection object and
# then populating it with REFERENCES to the child objects found in the original.
# In essence, a shallow copy is only one level deep. The copying process does
# not recurse and therefore won’t create copies of the child objects themselves.
#
# - https://realpython.com/python-variables/#variable-assignment
# - https://docs.python.org/2/library/copy.html
# - https://realpython.com/copying-python-objects/


