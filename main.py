import pygame
import random
from time import sleep
from screeninfo import get_monitors
import time
from os import startfile
import sys
import numpy as np

class Game():
    def __init__(self, genome):
        self.genome = genome
        self.fitness = 0
        self.last_dist = np.inf
        
        self.width, self.height = int(str(get_monitors()[0]).split(',')[2].split('=')[1]), int(str(get_monitors()[0]).split(',')[3].split('=')[1])
        self.start_width = int(self.width/3)
        self.pad_width = self.start_width*2
        self.pad_height = self.height

        self.FPS = 60
        self.timer = 0
        self.last_fruit_time = 0
        
        self.fight_width = 36
        self.fight_height = 38
        
        self.enemy_width = 26
        self.enemy_height = 20
        
        self.shotcount = 0
        
        pygame.init()
        self.gamepad = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('전투기게임')
        self.fighter = pygame.image.load('fighter.png')
        self.enemy = pygame.image.load('enemy.png')
        self.bullet = pygame.image.load('bullet.png')
        self.clock = pygame.time.Clock()

    def drawScore(self, count):
        self.shotcount = count
        font = pygame.font.Font('neodgm.ttf', 30)
        text = font.render('Enemy Kills: ' + str(count), True, (255,255,255))
        self.gamepad.blit(text, (10, 0))

    def drawPassed(self, count):
        font = pygame.font.Font('neodgm.ttf', 30)
        text = font.render(f'Enemy Passed: {count}/3', True, (255,0,0))
        self.gamepad.blit(text, (280, 0))

    def drawObject(self, obj, x, y):
        self.gamepad.blit(obj, (x,y))

    def get_inputs(self, enemy_x, enemy_y, x, y):
        result = [0, 0, 0, 0]
        if  enemy_x == x:
            result[1] = 1
        elif enemy_x > x:
            result[2] = 1
        elif enemy_x < x:
            result[0] = 1
        result[3] = ((enemy_y - y)/100)
        return np.array(result)

    def runGame(self):
        isShot = False
        shotcount = 0
        enemypassed = 0

        x = self.pad_width*0.45
        y = self.pad_height*0.9
        x_change = 0

        bullet_xy = []
        enemy_x = random.randrange(self.start_width+self.enemy_width, self.pad_width-self.enemy_width)
        enemy_y = 0
        enemy_speed = 18
        background_image = pygame.image.load('background.jpg')
        background_image = pygame.transform.scale(background_image, (int(self.pad_width/2), self.pad_height))

        while True:
            self.timer += 0.1
            if self.fitness < -self.FPS/2 or self.timer - self.last_fruit_time > 0.1 * self.FPS * 5:
                #self.fitness -= FPS/2
                print('Terminate!')
                return self.fitness, self.shotcount
            for event in pygame.event.get():            
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pressed = pygame.key.get_pressed()
                    if event.key == pygame.K_SPACE:
                        if len(bullet_xy) < 2*3:  
                            bullet_x = x + self.fight_width/2 - 5
                            bullet_y = y - self.fight_height
                            bullet_xy.append([bullet_x, bullet_y])
                            
                            bullet_x = x + self.fight_width/2 + 5
                            bullet_y = y - self.fight_height
                            bullet_xy.append([bullet_x, bullet_y])
            inputs = self.get_inputs(enemy_x, enemy_y, x, y)
            outputs = self.genome.move(inputs)
            outputs = np.argmax(outputs)

            if outputs == 0:
                x_change = 0
            elif outputs == 1:
                x_change -= 1
            elif outputs == 2:
                x_change += 1
            elif outputs == 3:
                if len(bullet_xy) < 2*3:
                    bullet_x = x + self.fight_width/2 - 5
                    bullet_y = y - self.fight_height
                    bullet_xy.append([bullet_x, bullet_y])

                    bullet_x = x + self.fight_width/2 + 5
                    bullet_y = y - self.fight_height
                    bullet_xy.append([bullet_x, bullet_y])
            elif outputs == 4:
                if len(bullet_xy) < 2*3:
                    bullet_x = x + self.fight_width/2 - 5
                    bullet_y = y - self.fight_height
                    bullet_xy.append([bullet_x, bullet_y])

                    bullet_x = x + self.fight_width/2 + 5
                    bullet_y = y - self.fight_height
                    bullet_xy.append([bullet_x, bullet_y])
                    x_change -= 1
            elif outputs == 5:
                if len(bullet_xy) < 2*3:
                    bullet_x = x + self.fight_width/2 - 5
                    bullet_y = y - self.fight_height
                    bullet_xy.append([bullet_x, bullet_y])

                    bullet_x = x + self.fight_width/2 + 5
                    bullet_y = y - self.fight_height
                    bullet_xy.append([bullet_x, bullet_y])
                    x_change += 1
            
            self.gamepad.fill((0,0,0))
            self.gamepad.blit(background_image, (self.start_width, 0))
            x += x_change
            if x < self.start_width+self.enemy_width:
                x = self.pad_width - self.fight_width
            elif x > self.pad_width - self.fight_width:
                x = self.start_width+self.enemy_width
            if y < enemy_y + self.enemy_height:
                if (enemy_x > x and enemy_x < x + self.fight_width) or \
                   (enemy_x + self.enemy_width > x and enemy_x+ self.enemy_width < x + self.fight_width):
                    self.fitness -= 6
                    return self.fitness, self.shotcount
            self.drawObject(self.fighter, x, y)
            if len(bullet_xy) != 0:
                for i, bxy in enumerate(bullet_xy):
                    bxy[1] -= 5
                    bullet_xy[i][1] = bxy[1]
                    if bxy[1] < enemy_y:
                        if bxy[0] > enemy_x and bxy[0] < enemy_x + self.enemy_width:
                            bullet_xy.remove(bxy)
                            isShot = True
                            self.shotcount += 1
                            self.fitness += 15
                            self.last_fruit_time = self.timer
                    if bxy[1] <= 0:
                        try:
                            bullet_xy.remove(bxy)
                        except:
                            pass
            if len(bullet_xy) != 0:
                for bx, by in bullet_xy:
                    self.drawObject(self.bullet, bx, by)
            self.drawScore(self.shotcount)
            enemy_y += enemy_speed    
            if enemy_y > self.pad_height:
                enemy_x = random.randrange(self.start_width+self.enemy_width, self.pad_width-self.enemy_width)
                enemy_y = 0
                enemypassed += 1
                self.fitness -= 10
            if enemypassed == 3:
                return self.fitness, self.shotcount
            if self.last_dist > abs(x-enemy_x):
                self.fitness += 1
            else:
                self.fitness -= 2
            self.drawPassed(enemypassed)
            if isShot:
                enemy_speed += 1
                if enemy_speed >= 26:
                    enemy_speed = 26
                enemy_x = random.randrange(self.start_width+self.enemy_width, self.pad_width-self.enemy_width)
                enemy_y = 0                      
                isShot = False
                
            self.drawObject(self.enemy, enemy_x, enemy_y)
                    
            pygame.display.update()
            self.clock.tick(self.FPS)
