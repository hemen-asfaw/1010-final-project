#REMINDER: remove print statemtnes we had for debudding  
import pygame
import os
import random
import sys
import time
pygame.init()
pygame.mixer.init()#sounds

screen_x = 1280
screen_y = 720
screen = pygame.display.set_mode((screen_x, screen_y))
game_name_display = pygame.display.set_caption("Iggy Runs!!")
clock = pygame.time.Clock()
speed_game = 9
ground_start = 0




Running =[]
run1_image = pygame.image.load("assets/Running_1.PNG")
scale_run1_image = pygame.transform.scale(run1_image,(250, 140))
Running.append(scale_run1_image) 

run2_image = pygame.image.load("assets/running_2.PNG")
scale_run2_image = pygame.transform.scale(run2_image,(250, 140))
Running.append(scale_run2_image)


OBSTACLES = [] 

kiwi_image = pygame.image.load("assets/kiki_bots.PNG") 
kiwi_rescaled = pygame.transform.scale(kiwi_image,(100, 100))
OBSTACLES.append(kiwi_rescaled)

book1_image = pygame.image.load("assets/obstacle_1.PNG") 
book1_rescaled = pygame.transform.scale(book1_image,(100, 100))
OBSTACLES.append(book1_rescaled)

book2_image = pygame.image.load("assets/obstacle_2.PNG") 
book2_rescaled = pygame.transform.scale(book2_image,(100, 100))
OBSTACLES.append(book2_rescaled)

Grass = pygame.image.load(os.path.join("assets/grass.jpg"))

game_font = pygame.font.Font("assets/Creampeach.ttf", 24)

#sounds

game_over_snd = pygame.mixer.Sound("assets/sounds/game.over.wav")
jump_snd = pygame.mixer.Sound("assets/sounds/point.wav")
theme_song_snd = pygame.mixer.Sound("assets/sounds/theme.song.wav")
menu_snd = pygame.mixer.Sound("assets/sounds/intro.wav")
roar_snd = pygame.mixer.Sound("assets/sounds/roar.wav")



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
        # self.set_sound()

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


    # def set_sound(self):
    #     path = os.path.join("assets/sounds/point.wav")
    #     self.sound = pygame.mixer.Sound(path)

    def jump(self):
        # self.sound.play()
        if self.iggy_jump:
            self.y -= self.gravity * 4
            self.gravity -= 0.5 # change speed of the jump
        if self.gravity < -(self.GRAVITY):
            self.iggy_jump = False
            self.gravity = self.GRAVITY

class Obstacles():

    def __init__(self, type):
        #image is for the what image we're adding 
        #type is for the type of obstacle which is either kiwi or the book 
        self.y = 250
        self.x = 510
        self.image = OBSTACLES[type] 
        self.type = type 
        self.rect = self.image.get_rect(center=(self.x, self.y))   
        self.rect.x = screen_x

    def update(self):
        self.rect.x -= speed_game 

    def display(self, screen):
        screen.blit(self.image, self.rect)


class kiwibot(Obstacles):
    def __init__(self):
        # self.type = OBSTACLES[0]
        super().__init__(0)
        self.rect.y = 550


class Book(Obstacles):
    def __init__(self): 
        super().__init__(random.randint(1,2))
        self.rect.y = 400


def main_function(): 
    global speed_game, ground_start, points 
    player = Iggy()
    points = 0
    active_obstacles = [] # List of obstacles on the screen at any given moment 
    demise_counter  = 0




    def score():
        global points, speed_game
        points +=1
        if points % 100 == 0 :
            speed_game += 1   
        text = game_font.render("Points: "+ str(points), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)
        
    

    
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

        if len(active_obstacles) == 0:
            spawn_rate = random.randint(0,2)
            if spawn_rate == 0:
                active_obstacles.append(kiwibot())
            elif spawn_rate == 1:
                active_obstacles.append(Book())

        
        for obstacle in active_obstacles:
            print(obstacle.rect.x)
            obstacle.display(screen)
            obstacle.update()
            if player.rect.colliderect(obstacle.rect):
                
                pygame.time.delay(2000)

                speed_game = 9

                demise_counter += 1
                menu(demise_counter)

                pygame.draw.rect(screen , (255, 0, 0), player.rect, 2)
            theme_song_snd.play()
            if obstacle.rect.x < - obstacle.rect.width:
                active_obstacles.pop()
                




        
 
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
        score()

  




        pygame.display.update()
        

def menu(demise_counter):
    
    global points 
    while True:
        

        screen.fill((255, 255, 255))
        # font = pygame.font.Font('freesansbold.ttf', 30)

        if demise_counter == 0:
            menu_snd.play()
            text_var = """Press Any Key to Make Iggy Run! 
            Press the space bar or up key to jump and avoid getting hit by the kiwi bots! Don't let the flying books get you either!""" 
            start_text = game_font.render(text_var, True, (0,0,0))
        elif demise_counter > 0:
            game_over_snd.play()
            start_text = game_font.render("Try Again? :(", True, (0, 0, 0))
            score = game_font.render("Iggy Points: " + str(points), True, (0, 0, 0))
            score_rect = score.get_rect()
            score_rect.center = (screen_x // 2, screen_y // 2 + 50)
            screen.blit(score, score_rect)

        text_rect = start_text.get_rect()
        text_rect.center = (screen_x // 2, screen_y // 2)
        screen.blit(start_text, text_rect)
        screen.blit(Running[0], (screen_x // 2 - 20, screen_y // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get(): 
            # if event.type == pygame.QUIT:
            #     run = False
            if event.type == pygame.QUIT:
                print("quitting")
                pygame.quit()
                sys.exit() 

            if event.type == pygame.KEYDOWN:
                roar_snd.play()
                main_function()


menu(demise_counter=0)


        

#references 
#https://youtu.be/ST-Qq3WBZBE


#https://youtu.be/K6mJqSnwj1g sounds
