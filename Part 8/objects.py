# ------------------------------------------------------------------------------
# FRED
# ------------------------------------------------------------------------------

class Fred():

  # Class variables
  x = 0
  y = 625

  isHit = False
  timeHit = 0
  health = 100

  leftImage = None
  rightImage = None
  leftImageHit = None
  rightImageHit = None

  direction = 1
  speed = 8
  pygame = None

  # Resets Fred's attributes
  def reset(self, x):
    self.x = x
    self.y = 625

    self.isHit = False
    self.timeHit = 0
    self.health = 100

    self.direction = 1
    self.speed = 8
    self.pygame = None

  # Moves Fred LEFT
  def moveLeft(self, leftBound):

    if self.direction is not 0:
      self.direction = 0

    if((self.x - self.speed) > leftBound):
      self.x -= self.speed

  # Moves Fred RIGHT
  def moveRight(self, rightBound):

    if self.direction is not 1:
      self.direction = 1

    if((self.x + self.speed) + 58 < rightBound):
      self.x += self.speed

  # Loads Images
  def loadImages(self, pygame):
    self.leftImage = pygame.image.load("assets/Fred-Left.png")
    self.rightImage = pygame.image.load("assets/Fred-Right.png")
    self.leftImageHit = pygame.image.load("assets/Fred-Left-Hit.png")
    self.rightImageHit = pygame.image.load("assets/Fred-Right-Hit.png")

  # Draws Fred onto surface
  def draw(self, surface, time):

    if time - self.timeHit > 800:
      self.timeHit = 0
      self.isHit = False

    # Draws right side image
    if self.direction is 1:
      # Checks if Fred hit and, IF SO, draws the hit version of right side Fred
      if self.isHit is False:
        surface.blit(self.rightImage, (self.x, self.y))
      else :
        surface.blit(self.rightImageHit, (self.x, self.y))
    # Draws left side image
    else :
      # Checks if Fred hit and, IF SO, draws the hit version of left side Fred
      if self.isHit is False:
        surface.blit(self.leftImage, (self.x, self.y))
      else :
        surface.blit(self.leftImageHit, (self.x, self.y))

  # Initialises Fred
  def __init__(self, x):
    self.x = x

# ------------------------------------------------------------------------------
# BARREL
# ------------------------------------------------------------------------------

class Barrel():

  # Class variables
  slots = [(4, 103), (82, 27), (157, 104), (234, 27), (310, 104), (388, 27), (463, 104), (539, 27), (615, 104), (691, 27), (768, 104), (845, 27), (920, 104)]
  slot = 0
  x = 0
  y = 0

  image = None
  brokenImage = None

  isBroken = False
  timeBroken = 0
  needsRemoving = False

  size = [33,22]
  ratio = 0.66

  vy = 1.5
  gravity = 1.05
  maxY = 20

  # Splits a barrel upon hitting Fred
  def split(self, time):
    self.isBroken = True
    self.timeBroken = time
    self.vy = 5
    self.x -= 10

  # Checks for collision between barrel and Fred
  def checkForCollision(self, fred):

    hitX = False
    hitY = False

    # Checks if x coordinate of Fred's leftomost top corner is within x
    # coordinates of barrel's top.
    if fred.x > self.x and fred.x < self.x + 75:
      hitX = True

    # Checks if x coordinate of Fred's rightmost top corner is within x
    # coordinates of barrel's top.
    elif fred.x + 57 > self.x and fred.x + 57 < self.x + 75:
      hitX = True

    # Checks if y coordinate of Fred's leftmost bottom corner AND Fred's
    # leftmost top corner are within y coordinates of barrel's bottom.
    if fred.y + 120 > self.y and fred.y < self.y:
      hitY = True
    # Checks if y coordinate of Fred's leftmost top corner are within y
    # coordinates of barrel's leftmost top corner.
    elif fred.y < self.y + 48:
      hitY = True
    # If Fred and barrel overlap at any x or y coordinate then there is a hit.
    if hitX is True and hitY is True:
      return True

  # Loads Images
  def loadImages(self, pygame):
    self.image = pygame.image.load("assets/Barrel.png")
    self.brokenImage = pygame.image.load("assets/Barrel_break.png")

  # Moves barrel
  def move(self, windowHeight):

    if self.vy < self.maxY:
      self.vy = self.vy * self.gravity
    self.y += self.vy

    if self.y > windowHeight:
      self.needsRemoving = True

  # Draws barrel
  def draw(self, surface, pygame):
    if self.isBroken is True:
      surface.blit(self.brokenImage, (self.x, self.y))
    else :
      surface.blit(self.image, (self.x, self.y))

  # Initiates object
  def __init__(self, slot):
    self.slot = slot
    self.x = self.slots[slot][0]
    self.y = self.slots[slot][1] + 24
