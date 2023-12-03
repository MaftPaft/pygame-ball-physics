import re
import pygame as pg
import math
import random
from pygame.math import Vector2
from math import sin, cos, atan2, pi
def converter(num):
    return float(str(num).replace("(", '').replace("+0j)", ''))

def mouse_pressed():
    return pg.mouse.get_pressed()

white = (255,255,255)
black = (0,0,0)

# Classes to make Sprites
class SpriteClass(pg.sprite.Sprite):
    def __init__(self, x, y, sz, sz2, color, spedx, spedy):
        pg.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pg.Surface([sz, sz2])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = spedx
        self.speedy = spedy
        self.dx = 1
        self.dy = 1
        self.offx = (self.rect.width / 2)
        self.offy = (self.rect.height / 2)
    
    
    def draw_blit(self, surface, window):
        window.blit(surface, (self.rect.x, self.rect.y))
    def draw(self,window):
        pg.draw.rect(window,white,self.rect)

    def rotate(self, angle):
        surf = pg.Surface((self.rect.width, self.rect.height), pg.SRCALPHA)
        surf.fill(self.color)
        rotation = pg.transform.rotate(surf, angle)
        return rotation
    def centered(self):
        self.rect.x -= self.rect.width/2
        self.rect.y -= self.rect.height/2

def colliderpie(rect, circlex, circley, circleradius):
    '''
    colliderpie(...)[0] = anglepoint
    colliderpie(...)[1] = line
    colliderpie(...)[2] = isclipped
    '''
    rectx = rect.x
    recty = rect.y
    rectwidth = rect.width
    rectheight = rect.height
    realx = rectx + (rectwidth /2)
    realy = recty + (rectheight /2)
    angle = atan2(realx-circlex, realy-circley)
    ps = (circleradius * sin(angle) + circlex, circleradius * cos(angle) + circley)
    clip = [(circlex, circley), (ps[0], ps[1])]
    clipped = rect.clipline(clip[0][0], clip[0][1], clip[1][0], clip[1][1])
    if clipped:
        return (ps, clip, clipped)
    else:
        return (ps, clip, None)

# Circle Class
class CircleClass(object):
    def __init__(self, x, y, radius, color, window, speedxx, speedyy, dex, dey):
        self.x = x
        self.y = y
        self.center = (self.x, self.y)
        self.radius = radius
        self.area = math.pi * (self.radius * self.radius)
        self.color = color
        self.speedx = speedxx
        self.speedy = speedyy
        self.dx = dex
        self.dy = dey

    #draw your circle class on the screen
    def draw(self, window, outlined=False, outlinedcolor=(255,255,255), outlinedwidth=2):
        pg.draw.circle(window, self.color, (self.x, self.y), self.radius)
        if outlined == True:
            pg.draw.circle(window, outlinedcolor, (self.x, self.y), self.radius + outlinedwidth, outlinedwidth)
    
    
    def rotatepoint(self, pointpositionx, pointpositiony, length, angle):
        point = Vector2(pointpositionx, pointpositiony)
        self.x = length * sin(angle) + point.x
        self.y = length * cos(angle) + point.y


#This is the class for adding gravity to CircleClass
class Space:
    
    def __init__(self):
        self.objs=[]
        self.static_objs=[]
    def add(self,obj):
        self.objs.append(obj)
    def update(self,window,obj,gravity=0.0025):
        if obj in self.objs:
            pg.draw.circle(window,obj.color,(obj.x,obj.y),obj.radius)
            obj.x+=obj.speedx
            obj.y+=obj.speedy
            obj.speedy+=gravity
        else:
            pg.draw.circle(window,obj.color,(obj.x,obj.y),obj.radius)
    def add_static(self,obj):
        self.static_objs.append(obj)
    def move(self,bounce=1):
        for i in range(len(self.objs)):
            ball = self.objs[i]
            for j in range(i+1,len(self.objs)):
                ball1 = self.objs[i]
                ball2 = self.objs[j]
                if circleCollides(ball1.x, ball1.y, ball2.x, ball2.y, ball1.radius, ball2.radius):
                    overlap = ball1.radius + ball2.radius - math.sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)
                    epsilon=1e-4
                    angle=math.atan2(ball2.y-ball1.y,ball2.x-ball1.x)
                    ball1.x -= (overlap / 2 + epsilon) * math.cos(angle)
                    ball1.y -= (overlap / 2 + epsilon) * math.sin(angle)
                    ball2.x += (overlap / 2 + epsilon) * math.cos(angle)
                    ball2.y += (overlap / 2 + epsilon) * math.sin(angle)
                    collision = pg.Vector2(ball2.x-ball1.x,ball2.y-ball1.y)
                    collision.normalize_ip()
                    velocity = pg.Vector2(ball2.speedx-ball2.speedx,ball2.speedy-ball1.speedy)
                    normal = velocity.dot(collision)

                    if normal < 0:
                        e=bounce
                        j = -(1+e)*normal
                        j /= 1/ball1.radius + 1/ball2.radius
                        impulse = j*collision
                        ball1.speedx -= 1 / ball1.radius * impulse.x
                        ball1.speedy -= 1 / ball1.radius * impulse.y
                        ball2.speedx += 1 / ball2.radius * impulse.x
                        ball2.speedy += 1 / ball2.radius * impulse.y
            if self.static_objs:
                for s in self.static_objs:
                    if circleCollides(s.x,s.y,ball.x,ball.y,s.radius,ball.radius):
                        overlap = ball.radius + s.radius - math.sqrt((ball.x - s.x) ** 2 + (ball.y - s.y) ** 2)
                        epsilon=1e-4
                        angle=math.atan2(s.y-ball.y,s.x-ball.x)
                        ball.x -= (overlap / 2 + epsilon) * math.cos(angle)
                        ball.y -= (overlap / 2 + epsilon) * math.sin(angle)
                        collision = pg.Vector2(s.x-ball.x,s.y-ball.y)
                        collision.normalize_ip()
                        velocity = pg.Vector2(s.speedx-s.speedx,s.speedy-ball.speedy)
                        normal = velocity.dot(collision)

                        if normal < 0:
                        
                            e=bounce
                            j = -(1+e)*normal
                            j /= 1/ball.radius + 1/s.radius
                            impulse = j*collision
                            ball.speedx -= 1 / ball.radius * impulse.x
                            ball.speedy -= 1 / ball.radius * impulse.y

                    
    
    def boundaries(self,width,height,obj):
        if obj.y >= height-obj.radius:
            obj.speedy*= -0.8
            obj.speedx*= 0.98
            obj.y = height-obj.radius
        if obj.x >= width-obj.radius or obj.x <= obj.radius:
            obj.speedx *= -0.8
            if obj.x < obj.radius:
                obj.x = obj.radius
            elif obj.x > width - obj.radius:
                obj.x = width - obj.radius




#text on screen
class pygame_text:
    def __init__(self,x,y,font,fontsize,color,text):
        self.x,self.y=x,y
        self.font=font
        self.fontsize=fontsize
        self.color=color
        self.text=text
        
    def update(self,window):
        font = pg.font.SysFont(self.font, self.fontsize)
        surface = font.render(self.text,False,self.color)
        window.blit(surface,(self.x,self.y))
        

# collision detection (only for CircleSprites)
def circleCollides(x1, y1, x2, y2, radius1, radius2):
    distance = math.hypot(x1 - x2, y1 - y2)
    collided = distance <= radius1 + radius2
    return collided == True
    
def intersect_line_line(P0, P1, Q0, Q1):  
    d = (P1[0]-P0[0]) * (Q1[1]-Q0[1]) + (P1[1]-P0[1]) * (Q0[0]-Q1[0]) 
    if d == 0:
        return None
    t = ((Q0[0]-P0[0]) * (Q1[1]-Q0[1]) + (Q0[1]-P0[1]) * (Q0[0]-Q1[0])) / d
    u = ((Q0[0]-P0[0]) * (P1[1]-P0[1]) + (Q0[1]-P0[1]) * (P0[0]-P1[0])) / d
    if 0 <= t <= 1 and 0 <= u <= 1:
        return P1[0] * t + P0[0] * (1-t), P1[1] * t + P0[1] * (1-t)
    return None



num = 0
rot = 1
off = 1
ron = (200, random.randint(0, 240), 50)
getVrotationx = []
getVrotationy = []

class points:
    def __init__(self, targetspos, targetsradius, radius=5, numV=0, rotatedV=90):
        global rot, off
        super().__init__()
        self.radius = radius
        self.speed = 0
        self.pos = Vector2(targetspos)
        self.front = Vector2(0, targetsradius)
        self.left = self.front.rotate(90)
        self.right = self.front.rotate(-90)
        self.sidev = []
        self.rotatedV = rotatedV
        for i in range(numV):
            ron = (240, random.randint(0, 240), 50)
            self.sidev.append(self.front.rotate(rotatedV))
            self.sidev[0] = self.front.rotate(rotatedV)
            if rot <= len(self.sidev) - 1 and len(self.sidev) > 0:
                self.sidev[rot] = self.sidev[rot - 1].rotate(rotatedV)
                rot += 1
            else:
                rot = 1
            for s in self.sidev:
                for others in self.sidev:
                    if circleCollides(self.pos[0]+s[0], self.pos[1]+s[1], self.pos[0]+others[0], self.pos[1]+others[1], self.radius, self.radius):
                        others.rotate_ip(rotatedV / off)
                        s.rotate_ip(rotatedV / off)
                    
                    if circleCollides(self.pos[0]+s[0], self.pos[1]+s[1], self.pos[0]+others[0], self.pos[1]+others[1], self.radius, self.radius) and s[1] >= 50 and s[0] <= 0 or circleCollides(self.pos[0]+s[0], self.pos[1]+s[1], self.pos[0]+others[0], self.pos[1]+others[1], self.radius, self.radius) and s[1] <= -50:
                        s.rotate_ip(rotatedV / off)
                        off += numV / 1
                
                
        for s in self.sidev:
            getVrotationx.append(s[0])
            getVrotationy.append(s[1])
        
    def rotate(self):
        self.front.rotate_ip(self.speed)
        for s in self.sidev:
            s.rotate_ip(self.speed)
    
    
    def vector(self, Vector, choosexy):
        return self.sidev[Vector][choosexy]
    
    
    def drawpoints(self, window, color=(255, 0, 0)):
        global num
        pg.draw.circle(window, color, list(map(int, self.pos+self.front)), self.radius)
        pg.draw.line(window, color, self.pos, self.pos+self.front, 2)
        
        for s in self.sidev:
            pg.draw.circle(window, color, list(map(int, self.pos+s)), self.radius)
            pg.draw.line(window, ron, self.pos, self.pos+s, 2)

class pgimage:
    def __init__(self, x, y, stringimage):
        self.image = pg.image.load(stringimage)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
    def draw(self, window, surface):
        window.blit(surface, (self.x, self.y))



# Colliding the sides of the window
def col_right(objectx, window_width):
    collided = objectx >= window_width
    return collided == True

def col_bottom(objecty, window_height):
    collided = objecty >= window_height
    return collided == True

def col_left(objectx, left=0):
    collided = objectx <= left
    return collided == True
    
def col_top(objecty, top=0):
    collided = objecty <= top
    return collided == True

grouping = []
def grouped(*group):
    grouping = []
    grouping.append(group)
    res = str(group)[1:-1]
    return res

def screen(width, height):
    return pg.display.set_mode((width, height))
    
