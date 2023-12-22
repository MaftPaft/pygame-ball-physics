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

sz=10

big = mg.CircleClass(w/2,h/2,500,(0,0,0),win,0,0,0,0)
balls = [mg.CircleClass(w/1.5,h/2,sz,white,win,0,0,0,0)]

data = {}
vels={}
for n in range(10):
    balls.append(mg.CircleClass(randint(big.x-big.radius,big.radius+big.x),randint(big.y-big.radius,big.radius+big.y),sz,white,win,0,0,0,0))

def flat_float(num: float):
    n = ""
    strnum=str(num)
    for i in range(len(strnum)):
        if strnum[i] == ".":
            n+=strnum[i]+strnum[i+1]
            break
        else:
            n+=strnum[i]
    return float(n)
  
def collisions(x1,y1,x2,y2,r1,r2):
    d = hypot(x1-x2,y1-y2)
    return [d >= r1+r2, d > r1+r2]
v = 0
avrg = 0
toggle = -1
run=True
clock=pg.time.Clock()
while run:
    mx,my=pg.mouse.get_pos()
    mp=pg.mouse.get_pressed()
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run=False
        if i.type == pg.KEYUP:
            if i.key == pg.K_SPACE:
                balls.extend(mg.CircleClass(randint(big.x-big.radius,big.radius+big.x),randint(big.y-big.radius,big.radius+big.y),sz,white,win,0,0,0,0) for _ in range(10))
        if i.type == pg.MOUSEBUTTONUP:
            if i.button == pg.BUTTON_RIGHT:
                for x in range(int(len(balls)/2)): 
                    if len(data) == len(balls): 
                        data.pop(balls[x])
                    vels.pop(balls[x])
                    balls.pop(x)
            if i.button == pg.BUTTON_MIDDLE:
                toggle *= -1
    
    win.fill(black)
    
    big.draw(win,True,(255,0,0),5)
    if mp[0]:
        big.x,big.y=mx,my
    dt = fps/(1+clock.get_fps())
    for b in balls:
        
        cols = collisions(b.x,b.y,big.x,big.y,b.radius-b.radius,big.radius-b.radius)
        if b not in data:
            data[b] = []
        b.x += b.dx
        b.y += b.dy
        b.dy += 0.025
        vel = pg.Vector2(b.dx,b.dy)
        p = pg.Vector2(b.x,b.y)
        p.normalize_ip()
        vel = vel.dot(p)
        vels[b] = abs(vel)
        v = max(list(vels.items()),key=(lambda x: x[1]))
        avrg = sum(list(vels.values()))/len(list(vels.values()))
        if b not in v:
            if toggle == -1:
                b.color=(255,255,255)
            else:
                if b in data:
                    data.pop(b)
                b.color=(55,55,55)
        if b != v[0]:
            b.dx += (v[0].x-b.x)*1e-3
            b.dy += (v[0].y-b.y)*1e-3
        if cols[0]:
            b.dx += (big.x-b.x)/55
            b.dy += (big.y-b.y)/55
            b.dx*=0.8
            b.dy*=0.8
            if cols[1]:
                a = atan2(b.x-big.x,b.y-big.y)
                b.x = (big.radius-b.radius)*sin(a)+big.x
                b.y = (big.radius-b.radius)*cos(a)+big.y
        b.draw(win)
    mg.pygame_text(0,0,"",50,(155,155,255),f"velocities: {flat_float(avrg)}").update(win)
    mg.pygame_text(0,55,"",50,(255,155,155),f"max: {flat_float(v[1])}").update(win)
    mg.pygame_text(0,110,"",50,(155,255,155),f"diff: {flat_float(flat_float(v[1])/(1+flat_float(avrg)))}").update(win)
    v[0].color = (0,0,255)
    pg.draw.circle(win,(0,255,0),(v[0].x,v[0].y),v[0].radius*3,2)
    for a,c in data.items():
        c.append([pg.Vector2(a.x,a.y),10*pi,collisions(a.x,a.y,big.x,big.y,a.radius-a.radius,big.radius-a.radius)[0]])
        for n in c:
            n[1]-=pi
            if n[1] <= 0:
                c.remove(n)
            if n[2]:
                c.clear()
        for i in range(1,len(c)):
            pg.draw.line(win,white,(c[i][0].x,c[i][0].y),(c[i-1][0].x,c[i-1][0].y),int(c[i][1]))

    pg.display.update()
    clock.tick(fps)
pg.quit()
