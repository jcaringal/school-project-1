import pygame
import sys
import random  # Required to generate random positions
import asyncio

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
score_font = pygame.font.Font(None, 35)
pygame.display.set_caption("Platformer with Coins")
clock = pygame.time.Clock()

async def main():
  background = (30, 30, 40)
	red = (255, 0, 0)
	blue = (0, 122, 255)
	yellow = (255, 223, 0)

  player_image = pygame.image.load("assets/player.png")
  player_rect = pygame.Rect(380, 100, 40, 40)
  player_vel_x = 0
  player_vel_y = 0
  player_speed = 6
  doubleJump = 1
  score = 0

  gravity = 0.8
  jumppower = -25
  is_grounded = False  

  platforms = [
    pygame.Rect(0, 550, 800, 50),     
    pygame.Rect(100, 400, 250, 20),   
    pygame.Rect(450, 300, 250, 20)    
]
  cupcake_image = pygame.image.load("assets/cupcake.png")
  cupcakes = []
  for _ in range(10):
    		cx = random.randint(50, 750)
    		cy = random.randint(50, 500)
    		cupcakes.append(pygame.Rect(cx, cy, 16, 16))


  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
           
    	keys = pygame.key.get_pressed()
   		player_vel_x = 0
    	if keys[pygame.K_LEFT]:
        	player_vel_x = -player_speed
    	if keys[pygame.K_RIGHT]:
        	player_vel_x = player_speed
    	if keys[pygame.K_UP] and is_grounded:
        	player_vel_y = jumppower
        	is_grounded = False
			elif keys[pygame.K_UP] and doubleJump == 1:
				player_vel_y = jumppower
				doubleJump -= 1

    	player_vel_y += gravity
    	player_rect.x += player_vel_x
    	if player_rect.left < 0: player_rect.left = 0
    	if player_rect.right > width: player_rect.right = width
    	player_rect.y += player_vel_y
    	is_grounded = False  
    		for platform in platforms:
        		if player_rect.colliderect(platform):
            		if player_vel_y > 0:  # Falling down
                		player_rect.bottom = platform.top
                		player_vel_y = 0
                		is_grounded = True
            		elif player_vel_y < 0:  # Jumping up
                		  player_rect.top = platform.bottom
                			player_vel_y = 0
    		if player_rect.bottom > 550:
        		player_rect.bottom = 550
        		player_vel_y = 0
        		is_grounded = True

    		for cupcake in cupcakes[:]:
       	if player_rect.colliderect(cupcake):
            cupcakes.remove(cupcake)
		 		cupcakes.append(pygame.Rect(random.randint(50, 700), random.randint(50, 500), 16, 16))
				score += 1
    		screen.fill(background)
    		for platform in platforms:
        		pygame.draw.rect(screen, blue, platform)
    		for cupcake in cupcakes:
        		pygame.draw.rect(screen, yellow, cupcake)
            screen.blit(cupcake_image, cupcake)
    			
        pygame.draw.rect(screen, red, player_rect)
        screen.blit(player_image, player_rect)

			  score_surface = score_font.render(f"Score: {score}", True, (255,255,255))
			  screen.blit(text_surface, (20, 20))

    		pygame.display.flip()
    		clock.tick(60)
        await asyncio.sleep(0)

pygame.quit()
asyncio.run(main())
