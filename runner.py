from tracemalloc import start
import pygame
from sys import exit


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) / 1000
    score_surf = custom_font.render(f'{current_time:.0f}', True, (64, 64, 64))
    score_rect = score_surf.get_rect(midtop=(400, 50))
    screen.blit(score_surf, score_rect)
    # pygame.draw.rect(screen, '#c0e8ec', score_rect)
    # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
    return current_time


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
custom_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
start_time = 0

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# score_surf = custom_font.render('My game', True, (64,64,64))
# score_rect = score_surf.get_rect(midtop = (400, 50))

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(900, 300))

snail_surf_2 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect_2 = snail_surf_2.get_rect(midbottom=(900, 300))

player_surf = pygame.image.load(
    'graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0
move_left = False
move_right = False

fly_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_rect = fly_surf.get_rect(midbottom=(900, 100))
fly1_frame = 0
fly_surf_2 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_rect_2 = fly_surf.get_rect(midbottom=(900, 100))
fly2_frame = 0

while True:

    # Event loop
    for event in pygame.event.get():

        # Checking for player exiting game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Checking for all keys pressed down
        if event.type == pygame.KEYDOWN:
            if game_active:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w) and player_rect.bottom >= 300:
                    player_gravity = -20
                if event.key == pygame.K_d and player_rect.left <= 800:
                    move_right = True
                if event.key == pygame.K_a and player_rect.left >= 0:
                    move_left = True

            else:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    snail_rect.left = 900
                    fly_rect.left = 900
                    player_rect.left = 80
                    fly_rect_2.left = 900

        # Checking for all keys pressed up
        if event.type == pygame.KEYUP:
            if game_active:
                if event.key == pygame.K_a or player_rect.left < 0:
                    move_left = False
                if event.key == pygame.K_d or player_rect.left > 800:
                    move_right = False

        # Checking for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = -20

    if game_active:

        # Drawing all background textures
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        # screen.blit(score_surf, score_rect)
        current_time = display_score()
        # Drawing and moving snail in loop
        snail_rect.left -= 3
        if snail_rect.left < -100:
            snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 300:
            player_rect.bottom = 300
        
        if player_rect.left > 740: player_rect.left = 739
        if player_rect.left < 0: player_rect.left = 1
        
        screen.blit(player_surf, player_rect)

        if snail_rect.colliderect(player_rect):
            game_active = False

        if current_time >= 5:
            if fly1_frame < 30:
                fly_surf = pygame.image.load(
                    'graphics/Fly/Fly1.png').convert_alpha()
                fly1_frame += 1
            elif fly1_frame < 60:
                fly_surf = pygame.image.load(
                    'graphics/Fly/Fly2.png').convert_alpha()
                fly1_frame += 1
            else:
                fly1_frame = 0
            fly_rect.left -= 1
            screen.blit(fly_surf, fly_rect)

        if fly_rect.colliderect(player_rect):
            game_active = False

        if current_time >= 10:
            screen.blit(snail_surf_2, snail_rect_2)
            snail_rect_2.left -= 5

        if current_time >= 23:
            if fly2_frame < 30:
                fly_surf_2 = pygame.image.load(
                    'graphics/Fly/Fly1.png').convert_alpha()
                fly2_frame += 1
            elif fly2_frame < 60:
                fly_surf_2 = pygame.image.load(
                    'graphics/Fly/Fly2.png').convert_alpha()
                fly2_frame += 1
            else:
                fly2_frame = 0
            fly_rect_2.left -= 1
            screen.blit(fly_surf_2, fly_rect_2)

        if move_left == True:
            player_rect.left -= 3
        if move_right == True:
            player_rect.left += 3

    else:
        move_left = False
        move_right = False
        screen.fill('black')
        start_time = pygame.time.get_ticks()
        game_over_surf = custom_font.render('Game Over', True, 'White')
        game_over_rect = game_over_surf.get_rect(midtop=(400, 150))
        screen.blit(game_over_surf, game_over_rect)
        final_score = current_time
        final_score_surf = custom_font.render(
            f'Score: {final_score:.0f}', True, 'White')
        final_score_rect = final_score_surf.get_rect(midtop=(400, 200))
        screen.blit(final_score_surf, final_score_rect)

    pygame.display.update()
    clock.tick(60)
