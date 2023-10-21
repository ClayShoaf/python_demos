import pygame
import sys
import os
import pymunk
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.a_walk = []
        for i in range(1,9):
            self.a_walk.append(pygame.transform.rotozoom(pygame.image.load(f"graphics/jack/Run ({i}).png").convert_alpha(),0,0.12))
        self.a_walk_frames = len(self.a_walk) - 1
        self.a_die = []
        for i in range(1,10):
            self.a_die.append(pygame.transform.rotozoom(pygame.image.load(f"graphics/jack/Dead ({i}).png").convert_alpha(),0,0.12))
        self.a_die_frames = len(self.a_die) - 1
        self.a_stand = []
        for i in range(1,10):
            self.a_stand.append(pygame.transform.rotozoom(pygame.image.load(f"graphics/jack/Idle ({i}).png").convert_alpha(),0,0.12))
        self.a_stand_frames = len(self.a_stand) - 1
        self.a_index = 0
        self.a_jump = pygame.transform.rotozoom(pygame.image.load("graphics/jack/Jump (5).png").convert_alpha(),0,0.12)
        #self.a_stand = pygame.transform.rotozoom(pygame.image.load('graphics/jack/Idle (8).png').convert_alpha(),0,0.12)
        self.image = self.a_walk[self.a_index]
        self.rect = self.image.get_rect(midbottom = (200,floor))
        self.gravity = 0
        self.move = False
        self.jump = False
        self.double_jump = True
        self.left = False
        self.unsafe = True

    def player_input(self):
        keys = pygame.key.get_pressed()
        if self.jump:
            if self.rect.bottom == floor:
                self.double_jump = True
                self.gravity = -15
                self.jump = False
            elif self.double_jump:
                self.double_jump = False
                self.gravity = -15
                self.jump = False
        if self.rect.left >= 0 and self.rect.right <= width:
            if keys[pygame.K_RIGHT]:
                self.rect.x += 3
                self.move = True
                if self.left:
                    for i in range(len(self.a_walk)):
                        self.a_walk[i] = pygame.transform.flip(self.a_walk[i],True,False)
                    for i in range(len(self.a_stand)):
                        self.a_stand[i] = pygame.transform.flip(self.a_stand[i],True,False)
                    for i in range(len(self.a_die)):
                        self.a_die[i] = pygame.transform.flip(self.a_die[i],True,False)
                    #self.a_stand = pygame.transform.flip(self.a_stand,True,False)
                    self.a_jump = pygame.transform.flip(self.a_jump,True,False)
                    self.left = False
            elif keys[pygame.K_LEFT]:
                self.rect.x -= 3
                self.move = True
                if not self.left:
                    for i in range(len(self.a_walk)):
                        self.a_walk[i] = pygame.transform.flip(self.a_walk[i],True,False)
                    for i in range(len(self.a_stand)):
                        self.a_stand[i] = pygame.transform.flip(self.a_stand[i],True,False)
                    for i in range(len(self.a_die)):
                        self.a_die[i] = pygame.transform.flip(self.a_die[i],True,False)
                    #self.a_stand = pygame.transform.flip(self.a_stand,True,False)
                    self.a_jump = pygame.transform.flip(self.a_jump,True,False)
                    self.left = True
            else:
                self.move = False
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    # step through the animation index `a_index`
    def a_step(self, length):
        if self.a_index < length:
            self.a_index += 1
        else:
            self.a_index = 0

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.a_jump
        elif self.move:
            self.image = self.a_walk[min(self.a_index, self.a_walk_frames)]
        elif DEAD and not INTRO:
            self.image = self.a_die[self.a_index]
        else:
            self.image = self.a_stand[self.a_index]

    def apply_gravity(self):
        self.rect.bottom = min(self.rect.bottom + self.gravity, floor)
        self.gravity += 1
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

class Monster(pygame.sprite.Sprite):
    def __init__(self, race, speed, points, bounce):
        super().__init__()
        self.race = race
        self.speed = speed
        self.points = points
        self.bounce = bounce
        self.a_list = []
        for i in range(1, len(os.listdir(f"graphics/{race}")) + 1):
            self.a_list.append(pygame.image.load(f"graphics/{race}/{race}{i}.png").convert_alpha())
        self.a_index = 0
        self.a_list_frames = len(self.a_list) - 1
        self.image = self.a_list[self.a_index]
        if race == "bat":
            self.elevation = floor - random.randint(30,250)
        else:
            self.elevation = floor
        self.rect = self.image.get_rect(midbottom = (random.randint(800,1000),self.elevation))

    # step through the animation index `a_index`
    def a_step(self):
        if self.a_index < self.a_list_frames:
            self.a_index += 1
        else:
            self.a_index = 0

    def update(self):
        self.rect.x -= self.speed
        self.image = self.a_list[self.a_index]
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

def display_score():
    current_time = pygame.time.get_ticks()//1000 - start_time
    score_surf = test_font.render(str(current_time + kills), False, 'Black')
    score_rect = score_surf.get_rect(center = (width/2, 50))
    screen.blit(score_surf,score_rect)
    return current_time + kills

def detect_collisions(enemies, player):
    global DEAD, kills
    if DEAD:
        return pygame.sprite.Group(), player
    for enemy in enemies:
        def check_points():
            if enemy.rect.collidepoint(player.rect.bottomleft):
                return True
            elif enemy.rect.collidepoint(player.rect.bottomright):
                return True
            elif enemy.rect.collidepoint(player.rect.midbottom):
                return True
            elif player.rect.collidepoint(enemy.rect.midtop):
                return True
            else: return False

        # Had to make `player.unsafe` check because otherwise, if you hit two enemies at once, player will die
        if (player.gravity >= 0 or not player.unsafe) and check_points():
                kills += enemy.points
                display_score()
                player.double_jump = True
                enemies.remove(enemy)
                player.gravity = min(player.gravity,-enemy.bounce)
                player.unsafe = False
        elif player.unsafe and player.rect.colliderect(enemy.rect):
            player.gravity = 0
            DEAD = True
            enemies = pygame.sprite.Group()
            return enemies, player
    return enemies, player

# Create the world
pygame.init()
width,height = 800,400
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Jumpy Jump")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
floor = 300
start_time = 0
kills = 0
final_score = 0
high_score = 0

# Setup the characters
player = pygame.sprite.GroupSingle()
player.add(Player())
bats = pygame.sprite.Group()
spiders = pygame.sprite.Group()

# Background assets
ground_surface = pygame.image.load('graphics/ground.png').convert()
sky_surface = pygame.image.load('graphics/Sky.png').convert()

#Intro screen
player_dead = pygame.image.load('graphics/jack/Dead (10).png').convert_alpha()
player_dead = pygame.transform.rotozoom(player_dead,0,.4)
player_stand_rect = player_dead.get_rect(midbottom = (width/2,floor))

# Timers
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1200)
animation_timer = enemy_timer + 1
pygame.time.set_timer(animation_timer, 50)
bat_timer = animation_timer + 1
pygame.time.set_timer(bat_timer, 100)
spider_timer = bat_timer + 1
pygame.time.set_timer(spider_timer, 1)

# Set Starting options
DEAD = True
DEBUG = False
INTRO = True

# MAIN LOOP
while True:
    # check for input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not DEAD:
            # timer events
            if event.type == animation_timer:
                if player.sprite.move:
                    player.sprite.a_step(player.sprite.a_walk_frames)
                else:
                    player.sprite.a_step(player.sprite.a_stand_frames)
            if event.type == bat_timer:
                for bat in bats.sprites():
                    bat.a_step()
            if event.type == spider_timer:
                for spider in spiders.sprites():
                    spider.a_step()
            if event.type == enemy_timer:
                for i in range(final_score // 100 + 1):
                    choice = random.randint(0,2)
                    if choice > 0:
                        spiders.add(Monster("spider", 4, 5, 18))
                    else:
                        bats.add(Monster("bat", 5, 10, 10))

            # key press events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.sprite.jump = True
                if event.unicode == 'd':
                    DEBUG = not DEBUG
                    print("Debug ON") if DEBUG else print("Debug OFF")

        elif INTRO:
            if event.type == animation_timer:
                if player.sprite.move:
                    player.sprite.a_step(player.sprite.a_walk_frames)
                else:
                    player.sprite.a_step(player.sprite.a_stand_frames)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.sprite.jump = True
                if event.key == pygame.K_RETURN:
                    start_time = pygame.time.get_ticks()//1000
                    kills = 0
                    player.sprite.rect.midbottom = (200,floor)
                    player.sprite.gravity = 0
                    DEAD = False
                    INTRO = False
        else:
            if event.type == animation_timer and player.sprite.a_index < player.sprite.a_die_frames:
                player.sprite.a_step(player.sprite.a_die_frames)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                start_time = pygame.time.get_ticks()//1000
                kills = 0
                player.sprite.rect.midbottom = (200,floor)
                player.sprite.gravity = 0
                player.sprite.a_index = 0
                DEAD = False

    # active game loop
    if not DEAD:
        # draw background
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        # draw and update score
        final_score = display_score()

        # character updates
        player.update()
        spiders.update()
        bats.update()

        # debugging stuff
        if DEBUG:
            pygame.draw.rect(screen, 'Blue', player.sprite.rect)
            for bat in bats:
                pygame.draw.rect(screen, 'Orange', bat)
            for spider in spiders:
                pygame.draw.rect(screen, 'Pink', spider)
            pygame.draw.circle(screen, 'Yellow', pygame.mouse.get_pos(), 5)
            
        # draw characters
        bats.draw(screen)
        spiders.draw(screen)
        player.draw(screen)

        # check for collison
        bats, player.sprite = detect_collisions(bats, player.sprite)
        spiders, player.sprite = detect_collisions(spiders, player.sprite)
        if DEAD:
            bats = pygame.sprite.Group()
            player.sprite.a_index = 0
        player.sprite.unsafe = True

    # intro screen
    elif INTRO:
        screen.fill((94,94,94))
        instruct_top = test_font.render("USE ARROW KEYS TO MOVE < ^ >", False, 'Black')
        top_rect = instruct_top.get_rect(center = (width/2, 50))
        instruct_bot = test_font.render("Press ENTER to start", False, 'Black')
        bot_rect = instruct_bot.get_rect(center = (width/2, 100))
        player.update()
        player.draw(screen)
        screen.blit(instruct_top,top_rect)
        screen.blit(instruct_bot,bot_rect)

    # death screen
    else:
        screen.fill((94,94,94))
        high_score = max(final_score, high_score)
        final_surf = test_font.render("HIGH SCORE: " + str(high_score), False, 'Black')
        final_rect = final_surf.get_rect(center = (width/2, 50))
        dead_surf = player.sprite.a_die[player.sprite.a_index]
        screen.blit(final_surf,final_rect)
        screen.blit(dead_surf, player.sprite.rect)

    pygame.display.update()
    clock.tick(60)
