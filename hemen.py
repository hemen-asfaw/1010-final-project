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
    # x = 250
    # y = 510 
    GRAVITY = 10
    
    def __init__(self):
        self.iggy_jump = False 
        self.run_img = Running
        #self.jump_img = Jumping
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
        # if self.current_image >= 10:
        #     self.step_index = 0

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
    



    # def jump(self):
    #     #self.image = self.jump_img
    #     #time.sleep(1)
    #     self.y -= self.gravity *4
    #     self.gravity -= 0.8
    #     #self.iggy_run = False
    #     print(self.y)
    #     if self.y == 505:
    #         self.y += self.gravity *4
    #         self.gravity += 0.8
    #         if self.y == 510:
    #             self.iggy_run = False


        # self.y = 800
        # print(self.y)
        # time.sleep(3)
        # self.y = 510
        # #time.sleep(1)
        # self.iggy_run = True
        # self.image = self.jump_img
        # print(self.y)
        # self.y -= self.gravity *4
        # self.gravity -= 0.8
        
        # if self.y == 505:
        #     print("FIRST") 
        #     self.iggy_jump = False
        

        #     #self.gravity < -self.Gravity
        #     self.y += self.gravity *10
        #     self.gravity += 0.8
        #     self.y = 510
        #     #self.iggy_jump = False
        #     # self.Gravity = self.gravity
        #     print("come down")

        #     # if self.y == 510:
        #     #     self.iggy_jump = True


            

def main_function(): 
    player = Iggy()

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
        pygame.display.update()


main_function()

        



