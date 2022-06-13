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
    r=None
    mx=None
    my=None
    mp=None
    dof=None
    rx=None
    ry=None
    ra=None
    xo=None
    yo=None
    ra=pa
    for r in range(1):
        dof=0
        aTan=-1/tan(ra) if ra>0 or ra<0 else -1
        if ra<180 and ra>0:
            print('looking up')
            ry = int(py)
            ry = ry>>6
            ry = ry<<6
            ry-=0.0001
            rx = py-ry
            rx = rx*aTan
            rx+=px
            yo = -64
            xo = -yo*aTan
            print(rx, ry, yo, xo, 'looking up')
        if ra>180 and ra<360:
            print('looking down')
            ry = int(py)
            ry = ry>>6
            ry = ry<<6
            ry+= 64
            rx = py-ry
            rx = rx*aTan
            rx+=px
            yo = 64
            xo = -yo*aTan
        if ra==0 or 180:
            rx=px
            ry=py
            dof=8
        while dof<8:
            mx = int(rx)
            mx = mx>>6
            my = int(ry)
            my = my>>6
            mp=my*mapX+mx
            if mp>0 and mp<mapX*mapY and map[mp]==1:
                dof = 8
            else:
                rx+=xo
                ry+=yo
                dof+=1
        glColor3f(0,1,0)
        glLineWidth(1)
        glBegin(GL_LINES)
        glVertex2i(px,py)
        glVertex2i(rx,ry)
        print(px, py, rx, ry, pa, ra)
        glEnd()

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

