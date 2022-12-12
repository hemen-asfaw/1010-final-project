import pygame
import os
import random
import sys
pygame.init()

screen_x = 1280
screen_y = 720
screen = pygame.display.set_mode((screen_x, screen_y))
game_name_display = pygame.display.set_caption("Iggy Runs!!")
clock = pygame.time.Clock()

Running =[]
run1_image = pygame.image.load("assets/Running_1.PNG")
scale_run1_image = pygame.transform.scale(run1_image,(300, 190))
Running.append(scale_run1_image) 

run2_image = pygame.image.load("assets/running_2.PNG")
scale_run2_image = pygame.transform.scale(run2_image,(300, 190))
Running.append(scale_run2_image)

Jumping = pygame.image.load(os.path.join("assets", "leap_1.PNG"))

Obstacles = [pygame.image.load(os.path.join("assets", "kiki_bots.PNG")),
                pygame.image.load(os.path.join("assets", "obstacle_1.PNG")),
                pygame.image.load(os.path.join("assets", "obstacle_2.PNG"))]
Grass = pygame.image.load(os.path.join("assets", "grass.jpg"))

class Iggy():
    #we're setting iggy at a stationary position because it does not change its position
    x = 250
    y = 510 
    gravity = 8.5 
    
    def __init__(self):
        self.iggy_run = True 
        self.iggy_jump = False 
        self.run_img = Running
        self.jump_img = Jumping
    
        self.Gravity = self.gravity
        self.current_image = 0 
        self.image = self.run_img[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    #In the update funcion we will put in the different actions of iggy that will change as game goes on 
    def update(self, inputs):
        #keys = pygame.key.get_pressed()

        if self.iggy_run:
            self.run()
        if self.iggy_jump:
            self.jump()
        # if self.current_image >= 10:
        #     self.step_index = 0
        
        if inputs == pygame.K_UP and not self.iggy_jump:
            self.iggy_run = False 
            self.iggy_jump = True  

        elif inputs == pygame.K_SPACE and not self.iggy_jump:
            self.iggy_run = False 
            self.iggy_jump = True
        else: 
            self.iggy_run = True
            self.iggy_jump = False
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
        self.image = self.jump_img
        if self.iggy_jump:
            self.iggy_jump.y -= self.gravity *4
            self.gravity -= 0.8
        if self.gravity < -(self.Gravity):
            self.iggy_jump = False
            self.Gravity = self.gravity
        


def main_function():
    running = True 
    player = Iggy()

    #in the while loop we will have all the things that should be runnning 
    #endlessly throughout the game  
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                pygame.quit()
                sys.exit() 
        
        screen.fill("light blue")
        player.display()
        player_input = pygame.key.get_pressed()

        player.update(player_input)
        pygame.display.update()


main_function()

        



