import pygame as pg
import mygame as mg
from math import *
from random import *
white=mg.white
black=mg.black

pg.init()
w,h=1800,1300
win=pg.display.set_mode((w,h))
fps=120

sz=25

big = mg.CircleClass(w/2,h/2,500,(0,0,0),win,0,0,0,0)
balls = [mg.CircleClass(w/1.5,h/2,sz,white,win,0,0,0,0)]

for n in range(10):
    sz=randint(1,50)
    balls.append(mg.CircleClass(randint(big.x-big.radius,big.radius+big.x),randint(big.y-big.radius,big.radius+big.y),sz,white,win,0,0,0,0))

def collisions(x1,y1,x2,y2,r1,r2):
    d = hypot(x1-x2,y1-y2)
    return [d >= r1+r2, d > r1+r2, d <= r1+r2, d < r1+r2]


v = 0
speed=0
run=True
clock=pg.time.Clock()
while run:
    mx,my=pg.mouse.get_pos()
    mp=pg.mouse.get_pressed()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run=False
        if i.type == pg.MOUSEBUTTONUP:
            if i.button == pg.BUTTON_LEFT:
                try:
                    sz=randint(1,50)
                    balls.extend(mg.CircleClass(uniform(big.x-big.radius,big.x+big.radius),uniform(big.y-big.radius,big.y+big.radius),sz,white,win,0,0,0,0) for _ in range(10))
                except Exception as e:
                    print(e)
            if i.button == pg.BUTTON_RIGHT:
                for x in range(int(len(balls)/2)):
                    balls.pop(x)
    
    win.fill(black)
    
    big.draw(win,True,(255,0,0),1)

    up = pg.key.get_pressed()[pg.K_UP]
    down = pg.key.get_pressed()[pg.K_DOWN]
    left = pg.key.get_pressed()[pg.K_LEFT]
    right = pg.key.get_pressed()[pg.K_RIGHT]
    if True in [up,down,left,right]:
        if speed < 0.1:
            speed+=0.001
    else:
        speed *= 0.9
    dt = fps/(1+clock.get_fps())

    for i,b in enumerate(balls):
        cols = collisions(b.x,b.y,big.x,big.y,b.radius-b.radius,big.radius-b.radius)
        
        b.x += b.dx*dt
        b.y += b.dy*dt
        b.dy += 0.025
        vel = pg.Vector2(b.dx,b.dy)
        p = pg.Vector2(b.x,b.y)
        p.normalize_ip()
        vel = vel.dot(p)
        if up:
            b.dy -= speed
            
        if down:
            b.dy += speed
            
        if right:
            b.dx += speed
            
        if left:
            b.dx -= speed
            
        
        
        if cols[0]:
            a = atan2(b.x-big.x,b.y-big.y)
            b.dx-=(big.radius-b.radius)*sin(a)/250*abs(vel*0.9)
            b.dy-=(big.radius-b.radius)*cos(a)/250*abs(vel*0.9)
            b.dx*=0.5
            b.dy*=0.5
            if cols[1]:
                a = atan2(b.x-big.x,b.y-big.y)
                b.x = (big.radius-b.radius)*sin(a)+big.x
                b.y = (big.radius-b.radius)*cos(a)+big.y
                b.dx*=0.9
                b.dy*=0.9
        for e in balls:
            if balls.index(e) != balls.index(b):
                othercol=collisions(e.x,e.y,b.x,b.y,e.radius,b.radius)
                
                if othercol[2]:
                    e.dx+=(e.x-b.x)/100*abs(vel)*(1/e.radius*b.radius)
                    e.dy+=(e.y-b.y)/100*abs(vel)*(1/e.radius*b.radius)
                    e.dx*=0.9
                    e.dy*=0.9
                    if othercol[3]:
                        a = atan2(e.x-b.x,e.y-b.y)
                        e.x = (b.radius+e.radius)*sin(a)+b.x
                        e.y = (b.radius+e.radius)*cos(a)+b.y
                        e.dx*=0.919
                        e.dy*=0.919

                    
        pg.draw.circle(win,b.color,(b.x,b.y),b.radius,1)

    pg.display.update()
    clock.tick(fps)
pg.quit()
