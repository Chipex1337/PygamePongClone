import pygame
import random
#Inits and other things that need to get called first, above this is only imports

pygame.init()
pygame.display.set_caption("Pong Clone")
clock = pygame.time.Clock()

#Colors, here we have some colors which we will be using

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Variables, here I usually place things such as static variables and others that might not change

ScreenSize = (800, 600)
GameRunning = True
PlayerSpeed = 8

#Other vars

roundStartTicks = 0

#Classes, here we throw some classes to have them all together in one place

class player:
	def __init__(self, y, x):
		self.y = y
		self.x = x
	def draw(self):
		pygame.draw.rect(game_Screen, WHITE, (self.x, self.y, 25, 100), 0)

class ball:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.xVel = 0
		self.yVel = 0
	def update(self):
		self.x += self.xVel
		self.y += self.yVel
		if self.y <= 0:
			self.yVel = self.yVel*-1
		elif self.y >= 550:
			self.yVel = self.yVel*-1
	def draw(self):
		pygame.draw.rect(game_Screen, WHITE, (self.x, self.y, 50, 50), 0)

class ScoreBoard:
	def __init__(self, player1Score, player2Score):
		self.player1Score = player1Score
		self.player2Score = player2Score
	def AddScore(self, Bool):
		if Bool:
			self.player1Score += 1
		else:
			self.player2Score += 1
		print("Current Scores: Player 1: ", self.player1Score, " Player2: ", self.player2Score)

#this is also horrible but it works
def DrawAll(object1, object2, object3):
	object1.draw()
	object2.draw()
	object3.draw()

#this is alright, shouldn't be breakable
def PlayerMover(object, val):
	object.y += val
	if object.y < 0:
		object.y = 0
	if object.y > 500:
		object.y = 500

#Called at start of round

def KickOffBall():
	if random.randint(0, 1) == 1:
		Ball.xVel = 12
	else:
		Ball.xVel = -12

#This function resets everything back to how it was at the start
#TODO ROUNDSTARTICKS changes to 0, but when printed in the game loop shows previous value, wtf
def resetRound():
	global roundStartTicks
	roundStartTicks = 0
	Ball.x = 375
	Ball.y = 275
	Ball.xVel = 0
	Ball.yVel = 0
	Player1.y = 250
	Player2.y = 250

#This function is here to reduce the amount of math that needs to be done

def possibleCollision():
	if Ball.x <= 50:
		print("CHECK COLLISION 1")
		checkCollision(Player1, Ball)
		if Ball.x <= 0:
			print("SCORE FOR 1")
			Scores.AddScore(True)
			resetRound()
	elif Ball.x >= 700:
		print("CHECK COLLISION 2")
		checkCollision(Player2, Ball)
		if Ball.x >= 750:
			print("SCORE FOR 2")
			Scores.AddScore(False)
			resetRound()

def checkCollision(Object, Projectile):
	if Object.y <= Projectile.y + 50 and Object.y + 100 > Projectile.y:
		print("REFLECTION")
		Projectile.xVel = Projectile.xVel*-1
		Projectile.yVel = random.randint(-8, 8)

#Lets get a screen up

game_Screen = pygame.display.set_mode(ScreenSize)
game_Screen.fill(BLACK)
pygame.display.flip()

#Start the objects
Player1 = player(250, 25)
Player2 = player(250, 750)
Ball = ball(375, 275)
Scores = ScoreBoard(0, 0)

#oh boy here comes the main game loop, prepare for hours of writing and debugging code

while GameRunning:
	#debug prints

	print(roundStartTicks)

	#this terribleness checks whether a key is held down, allowing for continuous movement

	roundStartTicks += 1

	pressed_keys = pygame.key.get_pressed()
	if pressed_keys[pygame.K_UP]:
		PlayerMover(Player2, -PlayerSpeed)
	elif pressed_keys[pygame.K_DOWN]:
		PlayerMover(Player2, PlayerSpeed)
	if pressed_keys[pygame.K_w]:
		PlayerMover(Player1, -PlayerSpeed)
	elif pressed_keys[pygame.K_s]:
		PlayerMover(Player1, PlayerSpeed)

	if roundStartTicks == 75:
		KickOffBall()

	Ball.update()
	possibleCollision()

	#I know it can run more efficiently but tbh if this code is too slow for your device you should stop using an arduino as your primary computer
	game_Screen.fill(BLACK)
	DrawAll(Player1, Player2, Ball)
	pygame.display.flip()
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GameRunning = False
			pygame.quit();
