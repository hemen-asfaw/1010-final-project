import pygame
import os
import random
import sys
import time
pygame.init()

screen_x = 1280
screen_y = 720
screen = pygame.display.set_mode((screen_x, screen_y))
game_name_display = pygame.display.set_caption("Iggy Runs!!")
clock = pygame.time.Clock()
speed_game = 5
ground_start = 0


Running =[]
run1_image = pygame.image.load("assets/Running_1.PNG")
scale_run1_image = pygame.transform.scale(run1_image,(300, 190))
Running.append(scale_run1_image) 

run2_image = pygame.image.load("assets/running_2.PNG")
scale_run2_image = pygame.transform.scale(run2_image,(300, 190))
Running.append(scale_run2_image)


Obstacles = [pygame.image.load(os.path.join("assets", "kiki_bots.PNG")),
                pygame.image.load(os.path.join("assets", "obstacle_1.PNG")),
                pygame.image.load(os.path.join("assets", "obstacle_2.PNG"))]
Grass = pygame.image.load(os.path.join("assets/grass.jpg"))

game_font = pygame.font.Font("assets/Creampeach.ttf", 24)






class Iggy():
    #we're setting iggy at a stationary position because it does not change its position
    # x = 250
    # y = 510 
    GRAVITY = 10
    
    def __init__(self):
        self.iggy_jump = False 
        self.run_img = Running
        self.y = 250
        self.x = 510
        self.gravity = self.GRAVITY 
        self.current_image = 0 
        self.image = self.run_img[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    #In the update funcion we will put in the different actions of iggy that will change as game goes on 
    def update(self, inputs):
        if inputs[pygame.K_SPACE] or inputs[pygame.K_UP]:
            self.iggy_jump = True

        if self.iggy_jump:
            self.jump()
        else:
            self.y = 510
            self.x = 250
            self.run()

        self.rect.x = self.x
        self.rect.y = self.y
    #come back to this if problem with iggy appearing
    def run(self):
        self.current_image += 0.08 
        if self.current_image >= 2:
            self.current_image = 0 
        self.image = self.run_img[int(self.current_image)]
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def display(self):
        screen.blit(self.image, self.rect)

    def jump(self):
        #self.image = self.jump_img
        if self.iggy_jump:
            self.y -= self.gravity * 4
            self.gravity -= 0.5 # change speed of the jump
        if self.gravity < -(self.GRAVITY):
            self.iggy_jump = False
            self.gravity = self.GRAVITY
    




def main_function(): 
    global speed_game, ground_start, points 
    player = Iggy()
    points = 0
    
    

    
    #in the while loop we will have all the things that should be runnning 
    #endlessly throughout the game  
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                pygame.quit()
                sys.exit() 
        
        player_input = pygame.key.get_pressed()

        print(player.y)
        print(player.iggy_jump)

        screen.fill("light blue")
        player.display()
        player.update(player_input)
        
 
        ground_rescaled = pygame.transform.scale(Grass, (1280,100))
        #ground_rect = ground_rescaled.get_rect(center=(640,690))

        speed_game += 0.0025

        ground_start -= speed_game
 
        ground_start -=1
        screen.blit(ground_rescaled, (ground_start, 645))
        screen.blit(ground_rescaled, (ground_start + 1280, 645))

        #the if statement keeps the ground running on an infinate loop
        if ground_start <= -1280:
            ground_start = 0
        pygame.display.update()

main_function()

        

#references 
#https://youtu.be/ST-Qq3WBZBE
