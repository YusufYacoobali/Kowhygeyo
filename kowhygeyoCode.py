# import modules
import pygame, sys
from pygame.locals import *
pygame.init()

# set all variables
screen_y = 650
screen_x = 1000
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Kowhygeyo")
font = pygame.font.SysFont('avenir', 30, True)
platforms = []
goblins = []
bullets = []
endMonster = []
tile_size = 40
lives = 3
scroll = [1000,1860]
isJump = False
jumpCount = 9
right = False
left = False
still = True

# load and scale all images
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg , (1000,650))
dirtBlock = pygame.image.load("dirtBlock.png")
dirtBlock = pygame.transform.scale(dirtBlock , (tile_size,tile_size))
stand = pygame.image.load("standing.png")
stand = pygame.transform.scale(stand, (tile_size,tile_size))
walkL = pygame.image.load("L1.png")
walkL = pygame.transform.scale(walkL, (tile_size,tile_size))
walkR = pygame.image.load("R1.png")
walkR = pygame.transform.scale(walkR, (tile_size,tile_size))
rockBlock = pygame.image.load("rockBlock1.jpg")
rockBlock = pygame.transform.scale(rockBlock, (tile_size,tile_size))
dirt = pygame.image.load("dirt.png")
dirt = pygame.transform.scale(dirt, (tile_size,tile_size))
help = pygame.image.load("help.png")
help = pygame.transform.scale(help, (tile_size, 60))
tree = pygame.image.load("tree.png")
tree = pygame.transform.scale(tree, (tile_size, 60))
bulletR = pygame.image.load("bulletR.png")
bulletR = pygame.transform.scale(bulletR, (10, 8))
bulletL = pygame.image.load("bulletL.png")
bulletL = pygame.transform.scale(bulletL, (10, 8))
bigBad = pygame.image.load("bigBad.png")
bigBad = pygame.transform.scale(bigBad, (80, 120))
family = pygame.image.load("family.png")
family = pygame.transform.scale(family, (tile_size, 60))

# create player class
class player():

    def __init__(self):
        self.rect = pygame.Rect(1500, 2360, tile_size, tile_size) # player position
        self.vel = 7

    def draw(self, screen):
        if right == True:  # what image to use when moving in a direction
            screen.blit(walkR, (box.rect.x - scroll[0], box.rect.y - scroll[1]))
        elif left == True:
            screen.blit(walkL, (box.rect.x - scroll[0], box.rect.y - scroll[1]))
        else:
            screen.blit(stand, (box.rect.x - scroll[0], box.rect.y - scroll[1]))

    def move(self, x, y):

        # Move each axis separately. This checks for collisions in both axis
        if x != 0:
            self.moveSingleAxis(x, 0)
        if y != 0:
            self.moveSingleAxis(0, y)

    def moveSingleAxis(self, x, y):

        self.rect.x += x
        self.rect.y += y

        for p in platforms:
            if self.rect.colliderect(p.rect): # this deals with collisions
                if x > 0:
                    self.rect.right = p.rect.left
                if x < 0:
                    self.rect.left = p.rect.right
                if y > 0:
                    self.rect.bottom = p.rect.top
                if y < 0:
                    self.rect.top = p.rect.bottom

# class for bullets
class projectile():

    def __init__(self, facing):
        bullets.append(self)   # control all bullets with this list
        self.rect = pygame.Rect(box.rect.x - scroll[0] + 5 , box.rect.y - scroll[1] + 20, 10, 8)
        self.facing = facing   # this handles which way the bullets will go
        self.vel = 7 * facing    # this is added to bullets x-coordinate so it either moves right or left


# enemy class
class enemy(object):
    walkRE = pygame.image.load("R1E.png")
    walkLE = pygame.image.load("L1E.png")
    walkRE = pygame.transform.scale(walkRE, (tile_size, tile_size))
    walkLE = pygame.transform.scale(walkLE, (tile_size, tile_size))

    def __init__(self, x, y, end):
        goblins.append(self)  # all goblins controlled from goblins list
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, tile_size, tile_size) # creates a rectangle in which the enemy will be in
        self.end = end
        self.vel = 3    # speed of goblins
        self.path = [self.x, self.end]  # this is how far the enemy travels

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:    # if position + speed is less than the limit then keep going
                self.x += self.vel
            else:
                self.vel = self.vel * -1     # if its greater then speed is made negative so goes the other way
        else:
            if self.x - self.vel > self.path[0]:    # if the enemy is going left
                self.x += self.vel
            else:
                self.vel = self.vel * -1

# class for final boss
class monster():

    def __init__(self, x, y, end):
        endMonster.append(self)    # easy to control the final boss by using a list. Also great if game is extended to many levels.
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 80, 120)    # made for collision handling
        self.end = end
        self.vel = 3
        self.health = 40     # final boss will have a health bar so this is its health
        self.path = [self.x, self.end]
        self.hitbox = (self.x - scroll[0], self.y - scroll[1] - 80, 80, 120)    # made to create health bar
        self.visible = True    # enemy will disappear when health is zero

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False  # final boss is killed

# creates all platforms
class platform(object):

    def __init__(self, pos):
        platforms.append(self)    # control all platforms from this list
        self.rect = pygame.Rect(pos[0], pos[1], tile_size, tile_size)

# introduction to game
def intro():

    i = 0
    screen.fill((0,0,0))
    text = font.render("PRESS E TO INTERACT WITH CHARACTERS", 1, (255,255,255))
    screen.blit(text, (500 - (text.get_width() / 2), 280))
    pygame.display.update()    # display needs to be updated so text is shown
    while i < 30:
        pygame.time.delay(100)    # pause is created for user to read
        i += 1

# if you collide with an enemy or run out of lives
def lose():
    global lives
    global scroll  # scroll gives the illusion of a moving camera when infact all images move
    i = 0
    if lives > 0:
        lives -= 1
        box.rect.x = 1500   # takes player back to starting position
        box.rect.y = 2360
        scroll = [1000, 1860]  # resets camera to starting position
    else:
        music = pygame.mixer.music.load('gameOver.wav') # game over music is loaded and played
        pygame.mixer.music.play(0)
        screen.fill((255, 255, 255))
        text = font.render("YOU LOST", 1, (0, 0, 0))
        screen.blit(text, (500 - (text.get_width() / 2), 280))
        text3 = font.render("ARE YOU THAT BAD?", 1, (0, 0, 0))
        screen.blit(text3, (500 - (text3.get_width() / 2), 300))
        pygame.display.update()
        while i < 300:
            pygame.time.delay(3000)
            i += 1
            raise SystemExit

# interaction with female bunny for story
def interact1():

    i = 0
    global help
    if box.rect.x > 2340 and box.rect.x < 2460:  # when bunny is in the right range then you can interact
        screen.fill((255, 255, 255))
        text = font.render("HEY IM BUCKLEY AND MY HUSBAND HAS BEEN KIDNAPPED", 1, (0, 0, 0))
        text2 = font.render("IM SCARED BUT YOU CAN USE MY GUN. PRESS SPACE TO SHOOT", 1, (0, 0, 0))
        screen.blit(text, (600 - (text.get_width() / 2), 200))
        screen.blit(text2, (550 - (text.get_width() / 2), 230))    # displays text
        help = pygame.transform.scale(help, (100, 150))   # scales and displays bunny in the cutscene
        screen.blit(help, (100, 200))
        pygame.display.update()
        while i < 50:
            pygame.time.delay(80)
            i += 1
        help = pygame.transform.scale(help, (tile_size, 60))    # scales bunny back to normal size

# talking to kidnapped bunny
def interact2():

    i = 0
    global family
    if box.rect.x > 10150 and box.rect.x < 10250:
        screen.fill((255,255,255))
        text = font.render("THANK YOU SO MUCH FOR SAVING ME. I MISS MY WIFE", 1, (0, 0, 0))
        text2 = font.render("YOU HAVE COMPLETED THE GAME", 1, (0, 0, 0))
        text3 = font.render("MADE BY: YUSUF YACOOBALI", 1, (0, 0, 0))
        screen.blit(text, (600 - (text.get_width() / 2), 200))
        screen.blit(text2, (600 - (text.get_width() / 2), 400))
        screen.blit(text3, (600 - (text.get_width() / 2), 430))
        family = pygame.transform.scale(family, (100, 150))
        screen.blit(family, (100, 200))
        pygame.display.update()
        while i < 70:
            pygame.time.delay(80)
            i += 1
        raise SystemExit  # exits game because game is finished


def loadMap(path):  # function reads map from text file and adds to a list
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    level = []
    for row in data:
        level.append(list(row))
    return level

level = loadMap('gameMap') # using the map loading function

# this section reads the map list created and turns set values into the objects needed
x = 0
y = -155
for row in level:
    for col in row:
        if col == "-":
            platform((x, y))
        elif col == "|":
            enemy(x, y, x + 200)
        elif col == "b":
            helpB = pygame.Rect(x, y, tile_size, 60)
        elif col == "t":
            treeP = pygame.Rect(x, y, tile_size, 60)
        elif col == "e":
            familyB = pygame.Rect(x, y, tile_size, 60)
        elif col == "k":
            monster(x, y, x + 300)
        x += tile_size   # moves along horizontally
    y += tile_size    # moves downwards after each row is complete
    x = 0   # when in next column, this makes the row start at the beginning

# very important function, this redraws the screen every time the game loop is run
def redrawGameWindow():

    screen.blit(bg, (0, 0))
    text1 = font.render("LIVES: " + str(lives), 1, (255, 255, 255))
    screen.blit(text1, (850, 0))   # permenant display of lives left
    screen.blit(help, (helpB.x - scroll[0], helpB.y - scroll[1] - 20))  # displays pink bunny
    screen.blit(family, (familyB.x - scroll[0], familyB.y - scroll[1] - 20))   # displays kidnapped bunny
    screen.blit(tree, (treeP.x - scroll[0], treeP.y - scroll[1] - 15))  # displays tree
    # Note how all the coordinates have a scroll value. This moves the images when the player moves so its like a camera moving

    for b in bullets:  # displays all bullets in bullets list
            screen.blit(bulletR, (b.rect.x, b.rect.y))

    # displays player with its draw function
    box.draw(screen)

    # displays different platforms depending on coordinates
    for p in platforms:
        if p.rect.x < 900 :
            screen.blit(rockBlock, (p.rect.x - scroll[0], p.rect.y - scroll[1]))
        elif p.rect.x > 900 and p.rect.y > 2420:
            screen.blit(dirt, (p.rect.x - scroll[0], p.rect.y - scroll[1]))
        else:
            screen.blit(dirtBlock, (p.rect.x - scroll[0], p.rect.y - scroll[1]) )

    # displays goblin picture depending on direction
    for g in goblins:
        g.move()
        if g.vel > 0:
            screen.blit(g.walkRE, (g.x - scroll[0], g.y - scroll[1]))
        else:
            screen.blit(g.walkLE, (g.x - scroll[0], g.y - scroll[1]))
        g.rect = pygame.Rect(g.x, g.y, tile_size,tile_size)  # this makes sure the collision box follows the goblins

    # easy way to display the final boss. Also a list incase it needs to be expanded in the future
    for e in endMonster:
        if e.visible == True:  # only if health > 0
            e.move()
            screen.blit(bigBad, (e.x - scroll[0], e.y - scroll[1] - 80))
            e.hitbox = (e.x - scroll[0], e.y - scroll[1] - 80, 80, 120)
            pygame.draw.rect(screen, (255, 0, 0), (e.hitbox[0], e.hitbox[1] - 20, 80, 10))  # health bar (red)
            pygame.draw.rect(screen, (0, 255, 0), (e.hitbox[0], e.hitbox[1] - 20, 80 - (2 * (40 - e.health)), 10))  # health bar (green)
            e.rect = pygame.Rect(e.x, e.y, 80, 120)

    # this updates the screen each time so each time while loop is run the display is updated
    pygame.display.update()

# player object is created
box = player()

# background music is the first thing to be run
music = pygame.mixer.music.load('epicBg.wav')
pygame.mixer.music.play(-1)

# intro is run with music
intro()

# game loop which happens non stop until game is finished or player loses all their lives
while True:

    # this is used to see if the player has actually moves. Later on it helps solve a scrolling issue
    movex = box.rect.x

    # permenant force of gravity
    box.move(0,3)

    # helps detect what keys have been pressed
    key = pygame.key.get_pressed()

    # if goblins collide with player the lose function is called
    for g in goblins:
        if box.rect.colliderect(g):
            lose()

        # when goblins collide with bullets, the goblin and bullet is removed
        for bullet in bullets:
            if bullet.rect.colliderect((g.rect.x - scroll[0] + 5, g.rect.y - scroll[1] + 20, 20, 20)):
                bullets.pop(bullets.index(bullet))
                goblins.pop(goblins.index(g))

    for e in endMonster:
        if e.visible == True:
            for b in bullets:      # if final boss is still alive and bullets collide then take away health
                    if b.rect.colliderect(e.hitbox):
                        e.hit()
                        bullets.pop(bullets.index(b))

            if box.rect.colliderect(e):    # if player collides with final boss then call lose function
                lose()

    if box.rect.y > 2600:
        lose()

    for event in pygame.event.get():   # if user quits display then let them
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:  # shoots when spacebar is pressed down only once, so only one bullet per press
                if right == True:
                    projectile(1) # 1 or -1 is facing (dictates direction of bullet depending on which way player is facing)
                if left == True:
                    projectile(-1)

    for b in bullets:    # moves bullets
        b.rect.x += b.vel

    if key[pygame.K_LEFT]:   # if left is pressed camera moves left so player stays in centre of screen
        right = False
        left = True
        box.move(-box.vel, 0)  # this moves player
        if box.rect.x == movex - box.vel:   # checks of player actually moved or is blocked by a platform
            scroll[0] -= box.vel

    if key[pygame.K_RIGHT]:
        right = True
        left = False
        box.move(box.vel, 0)
        if box.rect.x == movex + box.vel: # solves platform/stuck/scrolling issue
            scroll[0] += box.vel

    if not (isJump):
        if key[pygame.K_UP]:
            isJump = True    # if up is pressed this allows player to jump
    else:
        if jumpCount >= -9:
            neg = 1     # this makes player return to ground
            if jumpCount < 0:
                neg = -1
            box.move(0, -(jumpCount**2) * 0.5 * neg)   # takes the shape of a negative parabola because of the power
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 9

    if key[pygame.K_e]:      # control interactions depending on distance. The functions inside also check for the right distance
        if box.rect.x < 3000:
            interact1()
        elif box.rect.x > 8000:
            interact2()

    redrawGameWindow()   # the redraw function is called and everything is drawn on the display