#The layout for the screen was imported 
# we decided to use sprites because it has attributes like height, width etc..
# https://www.geeksforgeeks.org/pygame-creating-sprites/

import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Iggy's Game!")
points = 0
game_speed = 5
gamne_over = False 
obstacle_spawn = False
obstacle_cooldown = 5000
obstacle_timer = 0  
#jump_velocity
JUMP_VEL = 0

iggy_duck = screen.blit(pygame.image.load("assets/dog/ducking.PNG"))
iggy_jump_1 = screen.blit(pygame.image.load("assets/leap_1.PNG"))


 
# For if the game ends 
def end_game(): 
    global points, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(points)}", True, "black")
    score_rect = score_text.get_rect(center=(640,340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 0
    obstacle_group.empty()

#Groups

obstacle_group = pygame.sprite.Group()
lion_group = pygame.sprite.GroupSingle()


#font for the display on the screen
game_font = pygame.font.Font("assets/Creampeach.ttf", 24)

#calculates the score of iggy and displays it 
def score():
    global points, game_speed
    points +=1
    if points % 100 == 0 :
        game_speed += 1   
    text = game_font.render("Points: "+ str(points), True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (1000, 40)
    screen.blit(text, textRect)

#IGGY
#this iggy class is for the player 
#we start the class by inheriting from sprite
#got this inheritance code from a tutoril from the channel link below 
# https://www.youtube.com/@BaralTech

class Iggy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        #iggy's positions
        self.x = x
        self.y = y

    #creating a list to contains a lion racing images 
        self.racing_sprites = []
    #creating a list to containing a lion ducking images 
        self.iggy_jump_sprites = []
   
   #images of iggy racing/ducking using .append(pygame.transform.scale(pygame.image.load(""))) to set and enlarge images of iggy racing/ducking 

        self.racing_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Running_1.PNG"), (300, 190)))
        self.racing_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/running_2.PNG"), (300, 190)))

        self.iggy_jump_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/dog/ducking.PNG"), (330, 150)))
        
    #images  
        self.current_image = 0 
        self.image = self.racing_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x, self.y)) 

        #the gravity attribute monitors when iggy is not on the floor and to bring it back down
        self.sim_grav = 4.5

        self.iggy_jump = False
    #the speed attribute controls the speed of iggy throughout the game 
        self.speed = 50


    def jump(self):
        if self.rect.centery >= 550:
            while self.rect.centery - self.speed > 40:
                self.rect.centery -= 1

    #this function updates the images (swapping the image to look like actively racing)
    def update(self):
        self.animate()
        self.apply_gravity()
    # The animate function is switching between the pictures of Iggy at .05 speed. 
    # If Iggy is at the second photo, he'll reset back to the first image. Making the racing illusion
    def animate(self):
        self.current_image += 0.08 
        if self.current_image >= 2:
            self.current_image = 0 
        
        if self.iggy_jump:
            self.image = self.racing_sprites[int(self.current_image)]
        else:
            self.image = self.racing_sprites[int(self.current_image)]



      
  
        #self.jump_img = jumping1_image 
        self.rect = self.image.get_rect(center=(self.x, self.y))

    
    def simulate_gravity(self):
        self.iggy_jump = True 
        self.rect.centery = 550

    def control_gravity(self):
        self.iggy_jump = False
        self.rect.century = 550
    
 
    def apply_gravity(self):
        if self.rect.centery <= 550:
            self.rect.centery += self.sim_grav

    # The kiwi class is the obstacle that the player faces 
    # Similar to the Iggy class we inheret from sprite      


class kiwi(pygame.sprite.Sprite):
              
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.sprites = []
        for i in range(1,7):
            current_sprite = pygame.transform.scale(pygame.image.load("assets/kiki_bots.PNG"), (50,50))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.x -= game_speed
        self.rect = self.image.get_rect(center=(self.x, self.y))



#ground_design
ground_image = pygame.image.load("assets/grass.jpg")
ground_rescaled = pygame.transform.scale(ground_image, (1280,200))
ground_start = 0
ground_rect = ground_rescaled.get_rect(center=(640,690))

lion_group = pygame.sprite.GroupSingle()


#lion object 
x = 250
y = 550
lion = Iggy(x,y)
lion_group.add(lion)
# def jump(lion):
#     if lion.rect.centery >= 510:
#         while lion.rect.centery - lion.jump_vel > 40:
#             lion.rect.centery -= 1
#             lion = Iggy(250,650)


while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        iggy_duck()
    elif keys == pygame.K_SPACE or keys == pygame.K_UP:
        iggy_jump_1()

    screen.fill("light blue")
    
# Collisions 
    game_over = False

    if pygame.sprite.spritecollide(lion_group.sprite, obstacle_group, False):
        game_over = True 
        
    if game_over:
        end_game()
    
    if not game_over:
        game_speed += 0.00025
    
    if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
        obstacle_spawn = True
    
    if obstacle_spawn:
        obstacle_random = random.randint(1,50)
        if obstacle_random in range (1,7):
            pass
        for obstacle_random in range (7, 10):
            new_obstacle = kiwi(1280, 510)
            obstacle_group.add(new_obstacle)
            obstacle_timer = pygame.time.get_ticks()
            obstacle_spawn = False
    

            

    lion_group.update()
    lion_group.draw(screen)

    obstacle_group.update()
    obstacle_group.draw(screen)

    #game spped should increase as the game goes
    #it will increase everytime this while loop runs
    game_speed += 0.0025

    ground_start -= game_speed

    ground_start -=1
    screen.blit(ground_rescaled, (ground_start, 550))
    screen.blit(ground_rescaled, (ground_start + 1280, 550))

    #the if statement keeps the ground running on an infinate loop
    if ground_start <= -1280:
        ground_start = 0


    score()
    pygame.display.update()
    clock.tick(120)




