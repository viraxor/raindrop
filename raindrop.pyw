import pygame
from pygame.locals import *
from pygame import freetype
import sys
import random
import time
import winsound

pygame.init()
freetype.init()
width, height = 640, 480
screen=pygame.display.set_mode((width, height))

with open("skin.ini") as skin_file:
    skin_settings = skin_file.read()
    skin_settings_lines = skin_settings.split('\n')
    ctx, skin = skin_settings_lines[0].split('=')
    ctx, font = skin_settings_lines[1].split('=')

game_font = freetype.Font(font, size=24)

winsound.PlaySound('skins/' + skin + '/music.wav', winsound.SND_LOOP + winsound.SND_ASYNC)

game_icon = pygame.image.load('raindrop.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption('Raindrop')

def start():
    global player_x, rain_drop_x, rain_drop_y, player, rain_drop, player, playerstate, slowtime, slowtime_x, slowtime_y, slowtime_mode, slowtimeobj_enable, shield, shield_x, shield_y, shield_mode, shieldobj_enable, score, score_text, powerup_text
    player_x = 0
    rain_drop_x = 0
    rain_drop_y = 0
    slowtime_x = 0
    slowtime_y = 0
    shield_x = 0
    shield_y = 0
    score = 0
    player = pygame.image.load('skins/' + skin + '/robotalive_right.png')
    rain_drop = pygame.image.load('skins/' + skin + '/raindrop.png')
    slowtime = pygame.image.load('skins/' + skin + '/slowtime.png')
    shield = pygame.image.load('skins/' + skin + '/shield.png')
    score_text, rect = game_font.render('Score: ' + str(score), (0, 255, 0))
    powerup_text, rect = game_font.render('', (255, 0, 225))
    playerstate = 'r'
    slowtime_mode = False
    slowtimeobj_enable = False
    shield_mode = False
    shieldobj_enable = False

start()

keys = [False, False]

while 1:
    screen.fill(0)
    score_text, rect = game_font.render('Score: ' + str(score), (0, 255, 0))
    screen.blit(score_text, (0, 0))
    screen.blit(powerup_text, (240, 0))
    screen.blit(player, (player_x, 350))
    if shieldobj_enable:
        shield_y+=12
        screen.blit(shield, (shield_x, shield_y))
    if slowtimeobj_enable:
        slowtime_y+=12
        screen.blit(slowtime, (slowtime_x, slowtime_y))
    if shield_mode:
        powerup_text, rect = game_font.render('SHIELD', (255, 0, 225))
        shield_current = int(time.perf_counter())
        if shield_current - shield_start == 5:
            powerup_text, rect = game_font.render('', (255, 0, 225))
            shield_mode = False
    if slowtime_mode:
        powerup_text, rect = game_font.render('SLOW MODE', (255, 0, 225))
        slowtime_current = int(time.perf_counter())
        if slowtime_current - slowtime_start == 5:
            powerup_text, rect = game_font.render('', (255, 0, 225))
            slowtime_mode = False
        rain_drop_y+=6
    else:
        rain_drop_y+=12
    screen.blit(rain_drop, (rain_drop_x, rain_drop_y))
    pygame.display.flip()
    if random.randint(0, 5000) == 27:
        powerupobj_choose = random.randint(1, 2)
        if powerupobj_choose == 1:
            slowtime_x = random.randint(0, 575)
            slowtimeobj_enable = True
        if powerupobj_choose == 2:
            shield_x = random.randint(0, 575)
            shieldobj_enable = True
    if slowtime_y > 350:
        for i in range(78):
            if player_x + i == slowtime_x:
                slowtime_start = int(time.perf_counter())
                slowtime_mode = True
        slowtimeobj_enable = False
        slowtime_y = 0
    if shield_y > 350:
        for i in range(78):
            if player_x + i == shield_x:
                shield_start = int(time.perf_counter())
                shield_mode = True
        shieldobj_enable = False
        shield_y = 0
    if rain_drop_y > 350:
        for i in range(78):
            if shield_mode:
                pass
            else:
                if player_x + i == rain_drop_x:
                    if playerstate == 'r':
                        player = pygame.image.load('skins/' + skin + '/robotdead_right.png')
                    elif playerstate == 'l':
                        player = pygame.image.load('skins/' + skin + '/robotdead_left.png')
                    screen.blit(player, (player_x, 350))
                    pygame.display.flip()
                    time.sleep(3)
                    start()
                    score-=1
        score+=1
        rain_drop_x = random.randint(0, 575)
        rain_drop_y = 0
    for event in pygame.event.get(): 
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key==K_a:
                keys[0]=True
            elif event.key==K_d:
                keys[1]=True
            elif event.key==K_LEFT:
                keys[0]=True
            elif event.key==K_RIGHT:
                keys[1]=True
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_a:
                keys[0]=False
            elif event.key==pygame.K_d:
                keys[1]=False
            elif event.key==pygame.K_LEFT:
                keys[0]=False
            elif event.key==pygame.K_RIGHT:
                keys[1]=False
    if keys[1]:
        player_x+=10
        if shield_mode:
            player = pygame.image.load('skins/' + skin + '/robotshield_right.png')
        else:
            player = pygame.image.load('skins/' + skin + '/robotalive_right.png')
        playerstate = 'r'
    elif keys[0]:
        player_x-=12
        if shield_mode:
            player = pygame.image.load('skins/' + skin + '/robotshield_left.png')
        else:
            player = pygame.image.load('skins/' + skin + '/robotalive_left.png')
        playerstate = 'l'
    if player_x < 0:
        player_x = 0
    elif player_x > 550:
        player_x = 550
    clock = pygame.time.Clock()
    clock.tick(60)
