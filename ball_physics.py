import pygame as pg
import mygame as mg
from mygame import black,white, circleCollides
import random
#initalize
pg.init()
#screen size
width,height=800,900
win=pg.display.set_mode((width,height))
#radius of the objects
rad=50
colors=(random.randint(15,255),random.randint(15,255),random.randint(15,255))

#The Space class adds gravity to my objects (only works for CircleClass objects)
space = mg.Space()

#adding the ball to space for gravity
space.add(mg.CircleClass(width/2-50,height/2-200,rad,colors,win,0,0,0,0))

#Adding static objects based on the size of the screen
for n in range(int(width*height/10**4.5)):
    #random sizes added to the space
    radius = random.randint(5,50) 
    space.add_static(mg.CircleClass(random.randint(radius,width-radius),random.randint(radius,height-radius),random.randint(5,50),(155,155,155),win,0,0,0,0))
    #move the static objects if any of the static objects collide
    for s in space.static_objs:
        for ss in space.static_objs:
            if circleCollides(s.x,s.y,ss.x,ss.y,s.radius,ss.radius):
                s.x+=(s.x-ss.x)
                s.y+=(s.y-ss.y)
#gravity
g = 0.0025

run=True
clock=pg.time.Clock()
while run:
    #mouse data
    mx,my=pg.mouse.get_pos()
    mp=pg.mouse.get_pressed()
    #events
    for i in pg.event.get():
        #check if user closes window
        if i.type == pg.QUIT:
            run=False
    #fill window
    win.fill(black)

    #detects if user pressed mouse button left and if mouse is not near another object
    if mp[0] and mouse_collision == False:
        #adding objects to the space with random color to the mouse coordinates
        colors=(random.randint(15,255),random.randint(15,255),random.randint(15,255))
        space.add(mg.CircleClass(mx,my,rad,colors,win,0,0,0,0))
    

    
    for obj in space.objs:
        #updating the gravity and drawing the objects
        space.update(win,obj,g)
        #detecting the collisions of the sides of screen window
        space.boundaries(width,height,obj)
        #detects if mouse is near another object
        mouse_collision=circleCollides(obj.x,obj.y,mx,my,obj.radius,obj.radius)
    for statics in space.static_objs:
        #updating all static objects
        space.update(win,statics)
    
    #collisions of other objects and static objects with a bounciness set to 0.5
    space.move(0.5)

    pg.display.update()
    clock.tick()
