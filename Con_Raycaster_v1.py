#--------------------GITHUB-ConnorTippets-------------------------
#Based on 3DSages C compiled OpenGL Raycaster v1
#You can find 3DSage on github
#WASD to move player.

mapX = 8
mapY = 8
mapS = 64
from math import *
from math import pi as PI
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
#P2 = PI/2
#P3 = 3*PI/2
WIDTH, HEIGHT = 1024,512
px,py,pdx,pdy,pa=None,None,None,None,1
def degToRad(a):
    return a*PI/180

map = [
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,0,0,0,1,1,1,1,
    0,0,1,1,1,1,1,1,
    0,0,0,0,1,1,1,1,
    1,0,1,0,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1
]

def drawMap2D():
    x,y,xo,yo=None,None,None,None
    for y in range(mapY):
        for x in range(mapX):
            if map[y*mapX+x]==1:
                glColor3f(1,1,1)
            else:
                glColor3f(0,0,0)
            xo=(x*mapS)
            yo=(y*mapS)
            glBegin(GL_QUADS)
            glVertex2i(xo+1,yo+1)
            glVertex2i(xo+1,yo+mapS-1)
            glVertex2i(xo+mapS-1,yo+mapS-1)
            glVertex2i(xo+mapS-1,yo+1)
            glEnd()

def FixAng(a):
    if a>359:
        a-=360
    if a<0:
        a+=360
    return a

distance = lambda ax,ay,bx,by,ang: cos(degToRad(ang))*(bx-ax)-sin(degToRad(ang))*(by-ay)

def drawPlayer():
    glColor3f(1,1,0)
    glPointSize(8)
    glBegin(GL_POINTS)
    glVertex2i(px,py)
    glEnd()
    glPointSize(3)
    glBegin(GL_LINES)
    glVertex2i(px,py)
    glVertex2i(int(px+pdx*5),int(py+pdy*5))
    glEnd()

def drawRays3D():
    global px, py, pa
    glColor3f(0,1,1)
    glBegin(GL_QUADS)
    glVertex2i(526,  0)
    glVertex2i(1006,  0)
    glVertex2i(1006,160)
    glVertex2i(526,160)
    glEnd()
    glColor3f(0,0,1)
    glBegin(GL_QUADS)
    glVertex2i(526,160)
    glVertex2i(1006,160)
    glVertex2i(1006,320)
    glVertex2i(526,320)
    glEnd()
    
    r,mx,my,mp,dof,side = None,None,None,None,None,None
    vx,vy,rx,ry,ra,xo,yo,disV,disH = None,None,None,None,None,None,None,None,None
    
    ra=FixAng(pa+30)
    
    for r in range(60):
        dof=0
        side=0
        disV=100000
        Tan=tan(degToRad(ra))
        if cos(degToRad(ra))>0.001: #looking left
            rx = px
            rx = rx>>6
            rx = int(rx)
            rx = rx<<6
            rx+=64
            ry = (px-rx)*Tan+py
            xo = 64
            yo = -xo * Tan
        elif cos(degToRad(ra))<-0.001: #looking right
            rx = px
            rx = rx>>6
            rx = int(rx)
            rx = rx<<6
            rx-=0.0001
            ry = (px-rx)*Tan+py
            xo = -64
            yo = -xo * Tan
        else:
            rx = px
            ry = py
            dof = 8
        
        while dof<8:
            mx = int(rx)
            mx = mx>>6
            my = int(ry)
            my = my>>6
            mp=my*mapX+mx
            if mp>0 and mp<mapX*mapY and map[mp] == 1:
                dof = 8
                disV = cos(degToRad(ra))
                disV = disV*(rx-px)
                disV-=sin(degToRad(ra))*(ry-py)
            else:
                rx+=xo
                ry+=yo
                dof+=1
        vx=rx
        vy=ry
        dof=0
        disH=100000
        Tan=1/(Tan+1)
        if sin(degToRad(ra))>0.001: #looking up
            ry = py
            ry = ry>>6
            ry = int(ry)
            ry = ry<<6
            ry-=0.0001
            rx = (py-ry)*Tan+px
            yo = -64
            xo = -yo*Tan
        elif sin(degToRad(ra))<-0.001: #looking down
            ry = py
            ry = ry>>6
            ry = int(ry)
            ry = ry<<6
            ry+=64
            rx = (py-ry)*Tan+px
            yo = 64
            xo = -yo*Tan
        else:
            rx=px
            ry=py
            dof=8
        
        while dof<8:
            mx = int(rx)
            mx = mx>>6
            my = int(ry)
            my = my>>6
            mp = my*mapX+mx
            if mp>0 and mp<mapX*mapY and map[mp]==1:
                dof = 8
                disH = cos(degToRad(ra))*(rx-px)
                disH-=sin(degToRad(ra))*(ry-py)
            else:
                rx+=xo
                ry+=yo
                dof+=1
        
        hx=rx
        hy=ry
        glColor3f(0,0.8,0)
        if disV<disH:
            rx=vx
            ry=vy
            disH=disV
            glColor3f(0,0.6,0)
        else:
            rx=hx
            ry=hy
            disV=disH
            glColor3f(0,0.8,0)
        glLineWidth(2)
        glBegin(GL_LINES)
        px,py = int(px), int(py)
        rx,ry = int(rx), int(ry)
        glVertex2i(px,py)
        glVertex2i(rx,ry)
        glEnd()
        
        ca=FixAng(pa-ra)
        disH=disH*cos(degToRad(ca))
        lineH = int((mapS*320)/(disH))
        if lineH>320:
            lineH=320
        lineOff = 160 - (lineH>>1)
        
        glLineWidth(8)
        glBegin(GL_LINES)
        glVertex2i(r*8+530,lineOff)
        glVertex2i(r*8+530,lineOff+lineH)
        glEnd()
        
        ra=FixAng(ra-1);

def display():
    global px, py, pdx, pdy, pa
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    drawMap2D()
    drawPlayer()
    drawRays3D()
    glutSwapBuffers()

def buttons(key,x,y):
    global px, py, pdx, pdy, pa
    if key == b'a':
        pa-=0.1
        if pa<0:
            pa=360
        pdx=int(cos(pa)*5)
        pdy=int(sin(pa)*5)
    if key == b'd':
        pa+=0.1
        if pa>360:
            pa=0
        pdx=int(cos(pa)*5)
        pdy=int(sin(pa)*5)
    if key == b'w':
        px = int(px+pdx)
        py = int(py+pdy)
        print(px,py)
    if key == b's':
        px = int(px-pdx)
        py = int(py-pdy)
    glutPostRedisplay()

def init():
    global px, py, pdx, pdy, pa
    px = 300-mapS
    py = 300
    pdx=cos(pa)*5
    pdy=sin(pa)*5
    glClearColor(0.3,0.3,0.3,0)
    gluOrtho2D(0,WIDTH,HEIGHT,0)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIDTH,HEIGHT)
glutCreateWindow("GITHUB-ConnorTippets")
init()
glutDisplayFunc(display)
glutKeyboardFunc(buttons)
glutMainLoop()

