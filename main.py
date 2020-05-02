import pygame 
import random
import math
from pygame import mixer


#initialize the pygame
pygame.init()

#create game 

#anything in this window would be an event
screen = pygame.display.set_mode((800, 600))
 
#background
background =pygame.image.load('background2.png')
#background sound
mixer.music.load('background.wav')
mixer.music.play(-1) #-1 for playing on loop

#Tittle and iCON
pygame.display.set_caption("Space Invaders") 
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Player 
playerImg =pygame.image.load('mainchar.png')
playerX = 370
playerY = 480
playerX_change =0

#Enemy

enemyImg =[]
enemyX =[]
enemyY=[]
enemyX_change =[]
enemyY_change =[]
num_of_enemies = 6
for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('enemy.png'))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(3)
	enemyY_change.append(40)




#Bullet 
bulletImg =pygame.image.load('bullet.png')
bulletX = random.randint(0,800)
bulletY = 480
bulletX_change =0
bulletY_change =10
#ready state is when is you cant see bullet oon screen
#fire state is when bullet is in motion
bullet_state ="ready"

#Score
score_value =0
font =pygame.font.Font('freesansbold.ttf',32)

textX =10
textY =10

#Game Over Text

over_font =pygame.font.Font('freesansbold.ttf',64)




def show_score(x,y):
	#render() to create an image (Surface) of the text, then blit this image onto another Surface
	score =font.render("Score:"+str(score_value),True,(255,255,255))
	screen.blit(score,(x,y))

def game_over_text():
	over_text =over_font.render("GAME OVER",True,(255,255,255))
	screen.blit(over_text,(200,200))

def player(x,y):
	 #drawing an image on screen
	screen.blit(playerImg ,(x,y))

def enemy(x,y,i):
	 #drawing an image on screen
	screen.blit(enemyImg[i],(x,y))
def fire_bullet(x,y):
         	global bullet_state
         	bullet_state ="fire"
         	screen.blit(bulletImg,(x + 16,y + 10))     #16 - for center of spaceship and 10 just above the spaceship
def isCollision(enemyX,enemyY,bulletX,bulletY):
	distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY- bulletY,2)))
	if distance <27:
		return True
	else:
		return False
# Game loop
running =True
while running:
	#RGB 
	screen.fill((0, 0, 0))
	#background image
	screen.blit(background,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False 
		# IF KEYSTROKE IS PRESSED THIS WILL CHECKS IT'S RIGHT OR LEFT
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change  = -5
			
			if event.key == pygame.K_RIGHT:
				playerX_change = 5
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					bullet_sound=mixer.Sound('laser.wav')
					bullet_sound.play()
					bulletX = playerX
					fire_bullet(bulletX,bulletY)
				
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0

	#checking boundary of spaceship
	playerX += playerX_change

 	#when the spaceship hits the zero co ords 
	if playerX <=0:
		playerX = 0
		#size of spaceship is 64 pixel so 800-64
	elif playerX >=736: 
		playerX = 736


	#bullet movement
	if bulletY <=0:
		bulletY =480
		bullet_state ="ready"
	if bullet_state == "fire" :
		fire_bullet(bulletX,bulletY)
		bulletY -=  bulletY_change
	
	

	for i in range(num_of_enemies):

		#Game Over
		if enemyY[i]>440:
			for j in range(num_of_enemies):
				enemyY[j] =2000
			game_over_text()
			break



		#enemy movement
		enemyX[i]+= enemyX_change[i]
	 	#when the enemy hits the zero co ords 
		if enemyX[i] <= 0:
			enemyX_change[i] = 3
			enemyY[i] += enemyY_change[i]
			#size of enemy is 64 pixel so 800-64
		elif enemyX[i] >=736: 
			enemyX_change[i] = -3
			enemyY[i] += enemyY_change[i]

		#collision 
		collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			explosion_sound =mixer.Sound('explosion.wav')
			explosion_sound.play()
			bulletY =480
			bullet_state ="ready"
			score_value +=1
			enemyX[i] = random.randint(0,735)
			enemyY[i] = random.randint(50,150)

		enemy(enemyX[i],enemyY[i],i)



	player(playerX,playerY)
	show_score(textX,textY)
	pygame.display.update()
