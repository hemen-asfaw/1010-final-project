import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Iggy Runs!!")
game_font = pygame.font.Font("assets/Creampeach.ttf", 24)
jump_vel = 8.5


# Classes


class book(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1


class Dino (pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []
        

        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/Running_1.PNG"), (300, 190)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/running_2.PNG"), (300, 190)))

        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load("assets/dog/ducking.PNG"), (330, 150)))

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.jump_velocity = 50
        self.gravity = 4.5
        self.jumping = False

    def jump(self):
        print("jumping")
        if self.jumping:
            self.rect.y -= self.jump_velocity * 4
            self.jump_velocity -= 0.8
        if self.jump_velocity < - jump_vel:
            self.jumping = False
            self.jump_velocity = jump_vel

    # def duck(self):
    #     self.ducking = True
    #     self.rect.centery = 380

    # def unduck(self):
    #     self.ducking = False
    #     self.rect.centery = 510

    def apply_gravity(self):
        if self.rect.centery <= 510:
            self.rect.centery += self.gravity

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 2:
            self.current_image = 0

        # if self.ducking:
        #     self.image = self.ducking_sprites[int(self.current_image)]
        # else:
        #     self.image = self.running_sprites[int(self.current_image)]


class Kiwi(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
    
        self.sprites = []
        # for i in range(1, 7):
        #     current_sprite = pygame.transform.scale(
        #         pygame.image.load("assets/kiki_bots.PNG"), (100, 100))
        #     self.sprites.append(current_sprite)
        self.image = pygame.transform.scale(pygame.image.load("assets/kiki_bots.PNG"), (100, 100))
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


class Book(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([280, 295, 350])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/obstacle_1.PNG"), (84, 62)))
        
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]

# Variables


game_speed = 5
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

# Surfaces

ground_image = pygame.image.load("assets/grass.jpg")
ground_rescaled = pygame.transform.scale(ground_image, (1280, 200))
ground_start = 0
ground_rect = ground_rescaled.get_rect(center=(640, 690))
# cloud = pygame.image.load("assets/cloud.png")
# cloud = pygame.transform.scale(cloud, (200, 80))

# Groups

cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()

# Objects
dinosaur = Dino(250, 510)
dino_group.add(dinosaur)

# Sounds


# Events
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)

# Functions


def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()




while True:
    keys = pygame.key.get_pressed()
    # if keys[pygame.K_DOWN]:
    #     dinosaur.duck()
    # else:
    #     # if dinosaur.ducking:
    #     #     dinosaur.unduck()
    for event in pygame.event.get():
        #keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            print("quitting")
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dinosaur.jump()
      

    screen.fill("light blue")

    # Collisions
    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        game_over = True
        
    if game_over:
        end_game()

    if not game_over:
        game_speed += 0.0025
        

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            obstacle_random = random.randint(1, 100)
            if obstacle_random > 99:
                print("spawning: " + str(obstacle_random))
                new_obstacle = Kiwi(1280, 510)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            # elif obstacle_random in range(7, 10):
            #     new_obstacle = book()
            #     obstacle_group.add(new_obstacle)
            #     obstacle_timer = pygame.time.get_ticks()
            #     obstacle_spawn = False

        player_score += 0.1
        player_score_surface = game_font.render(
            str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (1150, 10))

        cloud_group.update()
        cloud_group.draw(screen)

        ptero_group.update()
        ptero_group.draw(screen)

        dino_group.update()
        dino_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        ground_start -= game_speed

        screen.blit(ground_rescaled, (ground_start, 550))
        screen.blit(ground_rescaled, (ground_start + 1280, 550))

        if ground_start <= -1280:
            ground_start = 0

    clock.tick(120)
    pygame.display.update()

    