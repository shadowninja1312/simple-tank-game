import pygame
import os
import math
from cmath import pi
import sys
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1300, 731
WIN = pygame.display.set_mode((WIDTH, HEIGHT) , vsync=1)
pygame.display.set_caption("TANKS!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255 ,0 , 0)
DARK_BLUE = (31 , 37 , 57)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('TANK_ASSETS/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('TANK_ASSETS/Gun+Silencer.mp3')
EXPLOSION_SOUND = pygame.mixer.Sound('TANK_ASSETS/explosion.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
TITLE_FONT = pygame.font.SysFont('comicsans', 100)

HITBOXES = False
FPS = 60
VEL = 5
BULLET_VEL =5
MAX_BULLETS = 1
TANK_WIDTH, TANK_HEIGHT = 150, 83

RIGHT_HIT = pygame.USEREVENT + 1
LEFT_HIT = pygame.USEREVENT + 2
RIGHT_HEAD_SHOT = pygame.USEREVENT + 3
LEFT_HEAD_SHOT = pygame.USEREVENT + 4

RIGHT_TANK_IMAGE = pygame.image.load(os.path.join('TANK_ASSETS', 'tank.png'))
RIGHT_TANK = pygame.transform.rotate(pygame.transform.scale(RIGHT_TANK_IMAGE, (TANK_WIDTH, TANK_HEIGHT)), 360)
RIGHT_TANK = pygame.transform.flip(RIGHT_TANK,True,False)

LEFT_TANK_IMAGE = pygame.image.load(os.path.join('/home/linus/TANK_ASSETS', 'tank.png'))
LEFT_TANK = pygame.transform.rotate(pygame.transform.scale(LEFT_TANK_IMAGE, (TANK_WIDTH, TANK_HEIGHT)), 0)

LEFTmissile = pygame.image.load(os.path.join('/home/linus/TANK_ASSETS', 'missile.png'))
LEFTmissile = pygame.transform.rotate(pygame.transform.scale(LEFTmissile, (100, 50)), 180)
LEFTmissile = pygame.transform.flip(LEFTmissile,True,True)

RIGHTmissile = pygame.image.load(os.path.join('/home/linus/TANK_ASSETS', 'missile.png'))
RIGHTmissile = pygame.transform.rotate(pygame.transform.scale(RIGHTmissile, (100, 50)), 0)
RIGHTmissile = pygame.transform.flip(RIGHTmissile,True,False)

LEFT_BARREL = pygame.image.load(os.path.join('TANK_ASSETS' , 'barrel.jpg'))
LEFT_BARREL = pygame.transform.scale(LEFT_BARREL , (80,16))
RIGHT_BARREL = pygame.image.load(os.path.join('TANK_ASSETS' , 'barrel.jpg'))
RIGHT_BARREL = pygame.transform.flip(RIGHT_BARREL , False,False)
RIGHT_BARREL = pygame.transform.scale(RIGHT_BARREL ,(80,16) )

background = pygame.transform.scale(pygame.image.load(os.path.join('TANK_ASSETS', 'background.jpeg')), (WIDTH, HEIGHT))

explosion = pygame.image.load(os.path.join('TANK_ASSETS', 'explosion.png'))
explosion = pygame.transform.rotate(pygame.transform.scale(
    explosion, (200, 150)), 0)

class Button():
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = TITLE_FONT.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        WIN.blit(self.image, self.rect)
        WIN.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
            

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = TITLE_FONT.render(self.text_input, True, "green")
        else:
            self.text = TITLE_FONT.render(self.text_input, True, "white")
def MISSILEPATH(startx, starty, power, ang, time):
    angle = ang
    velx = math.cos(angle) * power*2.5
    vely = math.sin(angle) * power*2.5

    distX = velx * time
    distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)
    newx = round(distX + startx)
    newy = round(starty - distY)


    return (newx, newy)
def draw_window(LEFT, RIGHT, LEFT_bullets, RIGHT_bullets, LEFT_health, RIGHT_health  , left_bullet_angle , right_bullet_angle , left_shot_angle , right_shot_angle , LEFT_BOTTOM , LEFT_TOP , RIGHT_BOTTOM , RIGHT_TOP):
    WIN.blit(background, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)
    leftmissile = pygame.transform.rotate(LEFTmissile,left_bullet_angle)
    rightmissile = pygame.transform.rotate(RIGHTmissile , right_bullet_angle)
    LEFTBARREL = pygame.transform.rotate(LEFT_BARREL , left_shot_angle)
    RIGHTBARREL = pygame.transform.rotate(RIGHT_BARREL , right_shot_angle)
    LEFT_health_text = HEALTH_FONT.render(
        "Health: " + str(LEFT_health), 1, BLACK)
    RIGHT_health_text = HEALTH_FONT.render(
        "Health: " + str(RIGHT_health), 1, BLACK)
    WIN.blit(LEFT_health_text, (WIDTH - LEFT_health_text.get_width() - 10, 10))
    WIN.blit(RIGHT_health_text, (10, 10))
    WIN.blit(LEFTBARREL,(LEFT.x + 100 - LEFTBARREL.get_width()/2 , LEFT.y+20 - LEFTBARREL.get_height()))
    WIN.blit(RIGHTBARREL,(RIGHT.x+ - RIGHTBARREL.get_width(), RIGHT.y+20-RIGHTBARREL.get_height()))
    WIN.blit(RIGHT_TANK, (RIGHT.x - RIGHT_TANK.get_width()/2, RIGHT.y))
    WIN.blit(LEFT_TANK, (LEFT.x, LEFT.y))
    if  HITBOXES == True:
        pygame.draw.rect(WIN , WHITE , LEFT_BOTTOM)
        pygame.draw.rect(WIN , WHITE , LEFT_TOP)
        pygame.draw.rect(WIN , WHITE , RIGHT_BOTTOM)
        pygame.draw.rect(WIN , WHITE , RIGHT_TOP)


    for bullet in LEFT_bullets:
        WIN.blit(leftmissile, (bullet.x , bullet.y))
        if  HITBOXES == True:
            pygame.draw.rect(WIN,WHITE,bullet)
    for bullet in RIGHT_bullets:
        WIN.blit(rightmissile, (bullet.x , bullet.y))
        if HITBOXES == True :
            pygame.draw.rect(WIN,WHITE , bullet)

    pygame.display.update()
def LEFT_handle_movement(keys_pressed, LEFT , LEFT_TOP , LEFT_BOTTOM):
    if keys_pressed[pygame.K_a] and LEFT.x - VEL > 0:  
        LEFT.x -= VEL
        LEFT_TOP.x -=VEL
        LEFT_BOTTOM.x -=VEL
    if keys_pressed[pygame.K_d] and LEFT.x + VEL + LEFT.width < BORDER.x:  
        LEFT.x += VEL
        LEFT_TOP.x +=VEL
        LEFT_BOTTOM.x +=VEL
def RIGHT_handle_movement(keys_pressed, RIGHT,RIGHT_TOP,RIGHT_BOTTOM):
    if keys_pressed[pygame.K_LEFT] and RIGHT.x-LEFT_TANK.get_width()/2 - VEL > BORDER.x + BORDER.width:  
        RIGHT.x -= VEL
        RIGHT_TOP.x -=VEL
        RIGHT_BOTTOM.x -=VEL
    if keys_pressed[pygame.K_RIGHT] and RIGHT.x + VEL + RIGHT.width < WIDTH:  
        RIGHT.x += VEL
        RIGHT_TOP.x +=VEL
        RIGHT_BOTTOM.x +=VEL
def handle_bullets(LEFT_bullets, RIGHT_bullets, LEFT, RIGHT,LEFT_TOP,LEFT_BOTTOM,RIGHT_TOP,RIGHT_BOTTOM,left_shot_angle,right_shot_angle ):
    left_time = 0
    right_time = 0
    original_left = LEFT
    original_right = RIGHT
    left_angle = left_shot_angle*pi/180
    right_angle = right_shot_angle*pi/180
    for bullet in LEFT_bullets:
        left_time = bullet.x - original_left
        if left_time<=0:
            left_time = original_left - bullet.x
        if original_left-bullet.x == 0:
            bullet.x = bullet.x+1
        left_time = left_time/100
        if RIGHT_bullets == LEFT_bullets:
            LEFT_bullets.remove(bullet)
            RIGHT_bullets.remove(bullet)
        bullet.x, bullet.y=MISSILEPATH(bullet.x , bullet.y , BULLET_VEL, left_angle, left_time)
        if RIGHT_BOTTOM.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RIGHT_HIT))
            WIN.blit(explosion , (bullet.x-100 , bullet.y-150))
            pygame.display.update()
            pygame.time.delay(100)
            LEFT_bullets.remove(bullet)
            pygame.display.update()
        elif RIGHT_TOP.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RIGHT_HEAD_SHOT))
            WIN.blit(explosion , (bullet.x -100, bullet.y-150))
            pygame.display.update()
            pygame.time.delay(100)
            LEFT_bullets.remove(bullet)
            pygame.display.update()
        elif bullet.x > WIDTH or bullet.x < 0 or bullet.y<0:
            LEFT_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            WIN.blit(explosion , (bullet.x , HEIGHT - 150))
            pygame.display.update()
            pygame.time.delay(100)
            EXPLOSION_SOUND.play()
            LEFT_bullets.remove(bullet)
            pygame.display.update()
            

    for bullet in RIGHT_bullets:
        right_time = original_right - bullet.x
        if right_time <0:
            right_time = bullet.x - original_right
        elif bullet.x-original_right==0:
            bullet.x = bullet.x-1
        right_time = right_time/100
        bullet.x , bullet.y=MISSILEPATH(bullet.x , bullet.y , BULLET_VEL , right_angle , right_time)
        if LEFT_bullets == RIGHT_bullets:
            LEFT_bullets.remove(bullet)
            RIGHT_bullets.remove(bullet)
        if LEFT_BOTTOM.colliderect(bullet):
            pygame.event.post(pygame.event.Event(LEFT_HIT))
            WIN.blit(explosion , (bullet.x , HEIGHT-155))
            pygame.display.update()
            pygame.time.delay(100)
            RIGHT_bullets.remove(bullet)
            pygame.display.update()
        elif LEFT_TOP.colliderect(bullet):
            pygame.event.post(pygame.event.Event(LEFT_HEAD_SHOT))
            WIN.blit(explosion , (bullet.x , HEIGHT-155))
            pygame.display.update()
            pygame.time.delay(100)
            RIGHT_bullets.remove(bullet)
            pygame.display.update()            
        elif bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0:
            RIGHT_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            WIN.blit(explosion , (bullet.x , HEIGHT - 155))
            pygame.display.update()
            pygame.time.delay(100)
            EXPLOSION_SOUND.play()
            RIGHT_bullets.remove(bullet)
            pygame.display.update()
def angle_left_bullet(LEFT_bullets,  LEFT ,left_shot_angle, ):
    angle_of_left_bullet = None
    left_time = 0
    original_left = LEFT.x
    left_angle = left_shot_angle*pi/180
    for bullet in LEFT_bullets:
        left_time = bullet.x - original_left
        if left_time <=0:
            left_time = original_left - bullet.x
        left_time = left_time/100
        prev_left_bullet_x , prev_left_bullet_y = (MISSILEPATH(bullet.x , bullet.y , BULLET_VEL,left_angle, left_time-0.001))
        angle_of_left_bullet = math.atan2( prev_left_bullet_y - bullet.y, prev_left_bullet_x - bullet.x ) * ( 180 / math.pi )
        angle_of_left_bullet = 0-angle_of_left_bullet
        if angle_of_left_bullet !=None:
            return(angle_of_left_bullet)
def angle_right_bullet( RIGHT_bullets,  RIGHT,right_shot_angle):
    angle_of_right_bullet = None
    right_time = 0
    original_right = RIGHT.x
    right_angle = right_shot_angle*pi/180
    for bullet in RIGHT_bullets:
        right_time = original_right - bullet.x
        if right_time <=0:
            right_time = bullet.x - original_right
        right_time = right_time/100
        prev_right_bullet_x , prev_right_bullet_y = (MISSILEPATH(bullet.x , bullet.y , BULLET_VEL, right_angle, right_time - 0.001))
        angle_of_right_bullet = math.atan2( prev_right_bullet_y - bullet.y, prev_right_bullet_x - bullet.x ) * ( 180 / math.pi )
        angle_of_right_bullet = 0-angle_of_right_bullet+180
        if angle_of_right_bullet != None:
            return(angle_of_right_bullet)
def draw_winner(text):
    run = True
    while run :
        draw_text = WINNER_FONT.render(text, 1, BLACK)
        press_to_continue = HEALTH_FONT.render("Press any button to continue", 1, BLACK)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2-10,draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(1000)
        WIN.blit(press_to_continue , (WIDTH/2 - press_to_continue.get_width()/2 , 200))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main_menu()
def main(run):

    LEFT = pygame.Rect(100, 600, TANK_WIDTH, TANK_HEIGHT)
    RIGHT = pygame.Rect(WIDTH-250, 600, TANK_WIDTH, TANK_HEIGHT)
    LEFT_TOP = pygame.Rect(133,600,67,25)
    LEFT_BOTTOM = pygame.Rect(100,650,TANK_WIDTH,100)
    RIGHT_TOP = pygame.Rect(WIDTH-200-LEFT_TANK.get_width()/2,600,67,25)
    RIGHT_BOTTOM  =pygame.Rect(WIDTH-250 -LEFT_TANK.get_width()/2,650,TANK_WIDTH,150)
    LEFT_bullets = []
    RIGHT_bullets = []
    left_shot_angle = 22
    right_shot_angle = 157 
    added_angle = 1
    LEFT_health = 100
    RIGHT_health = 100
    left_start = LEFT.x
    right_start = RIGHT.x
    clock = pygame.time.Clock()
    while run:  
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                global HITBOXES
                if event.key == pygame.K_EQUALS:
                    if HITBOXES ==True:
                        HITBOXES = False
                    else :
                        HITBOXES =True
                if event.key == pygame.K_LCTRL and len(LEFT_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(LEFT.x +50, LEFT.y - 20, 100, 50)
                    left_start = LEFT.x
                    LEFT_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(RIGHT_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(RIGHT.x -100, RIGHT.y - 20, 100, 50)

                    right_start = RIGHT.x
                    RIGHT_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                

            if event.type == LEFT_HIT:
                RIGHT_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == LEFT_HEAD_SHOT:
                RIGHT_health -= 10
                BULLET_HIT_SOUND.play()
            if event.type == RIGHT_HIT:
                LEFT_health -=1
                BULLET_HIT_SOUND.play()
            if event.type == RIGHT_HEAD_SHOT:
                LEFT_health -=10
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if RIGHT_health <= 0:
            winner_text = "RIGHT Wins!"

        if LEFT_health <= 0:
            winner_text = "LEFT Wins!"

        if winner_text != "":
            draw_winner(winner_text)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_w] and left_shot_angle<90:
            left_shot_angle +=added_angle
        if keys_pressed[pygame.K_s] and left_shot_angle>0:
            left_shot_angle -=added_angle
        if keys_pressed[pygame.K_UP] and right_shot_angle>90:
            right_shot_angle -=added_angle
        if keys_pressed[pygame.K_DOWN] and right_shot_angle<180:
            right_shot_angle +=added_angle

        left_bullet_angle=0
        right_bullet_angle=0
        if angle_left_bullet(LEFT_bullets,LEFT,left_shot_angle) !=None:
            left_bullet_angle = angle_left_bullet(LEFT_bullets, LEFT,left_shot_angle)
        if angle_right_bullet(RIGHT_bullets,RIGHT,right_shot_angle) !=None:
            right_bullet_angle = angle_right_bullet(RIGHT_bullets , RIGHT , right_shot_angle )

        RIGHT_handle_movement(keys_pressed, RIGHT , RIGHT_TOP , RIGHT_BOTTOM )
        LEFT_handle_movement(keys_pressed, LEFT,LEFT_TOP , LEFT_BOTTOM)
        handle_bullets(LEFT_bullets, RIGHT_bullets, left_start, right_start,LEFT_TOP,LEFT_BOTTOM,RIGHT_TOP,RIGHT_BOTTOM,left_shot_angle , right_shot_angle )
 
        draw_window(LEFT, RIGHT, LEFT_bullets, RIGHT_bullets,LEFT_health, RIGHT_health , left_bullet_angle , right_bullet_angle , left_shot_angle , right_shot_angle, LEFT_BOTTOM , LEFT_TOP , RIGHT_BOTTOM , RIGHT_TOP)

    main(True)
    
def how_to_play():
    button_surface = pygame.image.load(
    os.path.join('/home/linus/TANK_ASSETS',"cross.png"))
    button_surface = pygame.transform.scale(button_surface, (50,50))
    run = True        
    how_to_play = pygame.image.load(os.path.join('/home/linus/TANK_ASSETS' , "how to play.jpg"))
    how_to_play = pygame.transform.scale(how_to_play , (WIDTH , HEIGHT))
    escape = Button(button_surface ,WIDTH-20 ,20,"")

    while run ==True:
        pygame.init()
        WIN.blit(how_to_play , (0,0))
        escape.update()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                    run = False
            elif event.type ==pygame.MOUSEBUTTONDOWN:
                if escape.checkForInput(pygame.mouse.get_pos()):
                    main_menu()
def main_menu():

    run = True
    WIN.blit(background, (0, 0))
    button_surface = pygame.image.load(
    os.path.join('/home/linus/TANK_ASSETS',"button.jpg"))
    button_surface = pygame.transform.scale(button_surface, (650 -239, 150))
    TITLE_TEXT = TITLE_FONT.render("TANKS!", 1, BLACK)
    while run == True:
        WIN.blit(background, (0, 0))
        WIN.blit(TITLE_TEXT , (650 - TITLE_TEXT.get_width()/2 , 40))
        start = Button(button_surface , 650 , 300 , "Start")
        how_to_play_button = Button(button_surface , 650 , 600 , "how to play")
        
        for button in (start, how_to_play_button):
            button.update()
            button.changeColor(pygame.mouse.get_pos())
            button.update()  
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.checkForInput(pygame.mouse.get_pos()):
                    main(True)
                if how_to_play_button.checkForInput(pygame.mouse.get_pos()):
                    how_to_play()
                    run = False
        pygame.display.update()
if __name__ == "__main__":
    main_menu()
