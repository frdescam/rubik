#! /usr/bin/python

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from RubikMoves import Moves

VERTICES = (
    ( 1, -1, -1), ( 1,  1, -1), (-1,  1, -1), (-1, -1, -1),
    ( 1, -1,  1), ( 1,  1,  1), (-1, -1,  1), (-1,  1,  1)
)
EDGES = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
CENTERS = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4), (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))
             # yellow       # green       # white       # blue        # orange       # red
COLORS = ((1, 0.8, 0), (0, 0.5, 0), (0.95, 0.95, 0.95), (0, 0, 0.75), (0.9, 0.5, 0), (0.7, 0, 0))
MOVES = {
            # (axis, slice, dir)
            Moves.L: (0, 0, 1), Moves.PR: (0, 2, 1), Moves.D: (1, 0, 1),
            Moves.PU: (1, 2, 1), Moves.B: (2, 0, 1), Moves.PF: (2, 2, 1),
            Moves.PL: (0, 0, -1), Moves.R: (0, 2, -1), Moves.PD: (1, 0, -1),
            Moves.U: (1, 2, -1), Moves.PB: (2, 0, -1), Moves.F: (2, 2, -1),
        }

class Cubie3D():
    def __init__(self, id, N, scale):
        self.N = N
        self.scale = scale
        self.init_i = [*id]
        self.current_i = [*id]
        self.rot = [[1 if i==j else 0 for i in range(3)] for j in range(3)] # identity matrix

    def reset(self):
        self.current_i = [*self.init_i]
        self.rot = [[1 if i==j else 0 for i in range(3)] for j in range(3)]

    def isAffected(self, axis, slice, dir):
        return self.current_i[axis] == slice

    def update(self, axis, slice, dir):

        if not self.isAffected(axis, slice, dir):
            return

        i, j = (axis+1) % 3, (axis+2) % 3
        for k in range(3):
            self.rot[k][i], self.rot[k][j] = -self.rot[k][j]*dir, self.rot[k][i]*dir

        self.current_i[i], self.current_i[j] = (
            self.current_i[j] if dir < 0 else self.N - 1 - self.current_i[j],
            self.current_i[i] if dir > 0 else self.N - 1 - self.current_i[i] )

    def transformMat(self):
        scaleA = [[s*self.scale for s in a] for a in self.rot]  
        scaleT = [(p-(self.N-1)/2)*2.1*self.scale for p in self.current_i] 
        return [*scaleA[0], 0, *scaleA[1], 0, *scaleA[2], 0, *scaleT, 1]

    def draw(self, animate, angle, axis, slice, dir):

        glPushMatrix()

        if animate and self.isAffected(axis, slice, dir):
            glRotatef( angle*dir, *[1 if i==axis else 0 for i in range(3)] )
        glMultMatrixf( self.transformMat() )

        glBegin(GL_QUADS)
        for i in range(len(CENTERS)):
            glColor3fv(COLORS[i])
            for j in CENTERS[i]:
                glVertex3fv(VERTICES[j])
        glEnd()

        glPopMatrix()

class Rubik3D():
    def __init__(self, N, scale):
        self.N = N
        nbr = range(self.N)
        self.cubes = [Cubie3D((x, y, z), self.N, scale) for x in nbr for y in nbr for z in nbr] # create the 27 cubies for a 3x3x3 Rubik

    def mainloop(self, mix, solution):

        rot_cube_map  = { K_UP: (-1, 0), K_DOWN: (1, 0), K_LEFT: (0, -1), K_RIGHT: (0, 1)} # rotate all rubik to change perspective view

        ang_x, ang_y, rot_cube = 0, 0, (0, 0)
        animate, animate_ang, animate_speed = False, 0, 5
        action = (0, 0, 0)

        showing_solution = False
        showing_mix = False

        while True:

            # KEY EVENTS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        return()
                    if event.key in rot_cube_map:
                        rot_cube = rot_cube_map[event.key]
                    if not animate and event.key == K_m:
                        animate = True
                        action = MOVES[next(mix)]
                        showing_mix = True
                    if not animate and event.key == K_s:
                        animate = True
                        action = MOVES[next(solution)]
                        showing_solution = True
                    if not animate and event.key == K_r:
                        for cube in self.cubes:
                            cube.reset()
                if event.type == KEYUP:
                    if event.key in rot_cube_map:
                        rot_cube = (0, 0)

            # DISPLAY PARAMETERS

            ang_x += rot_cube[0]*2
            ang_y += rot_cube[1]*2

            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            glTranslatef(0, 0, -40)

            glRotatef(ang_y, 0, 1, 0)
            glRotatef(ang_x, 1, 0, 0)

            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

            # ANIMATION

            if animate:
                if animate_ang >= 90:
                    for cube in self.cubes:
                        cube.update(*action)
                    animate, animate_ang = False, 0

            for cube in self.cubes:
                cube.draw(animate, animate_ang, *action)

            if animate:
                animate_ang += animate_speed

            # MIX & SOLUTION ANIMATIONS

            if showing_mix and not animate:
                try:
                    action = MOVES[next(mix)]
                    animate = True
                except StopIteration:
                    showing_mix = False

            if showing_solution and not animate:
                try:
                    action = MOVES[next(solution)]
                    animate = True
                except StopIteration:
                    showing_solution = False

            pygame.display.flip()
            pygame.time.wait(10)

def showcase3DOpenGL(mix, solution):

    pygame.init()
    display_size = (800,600)
    screen = pygame.display.set_mode(display_size, DOUBLEBUF|OPENGL)

    glEnable(GL_DEPTH_TEST) 
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display_size[0]/display_size[1]), 0.1, 50.0)

    cube = Rubik3D(3, 2) # create a 3x3x3 rubik, scale of 2 
    cube.mainloop(mix.asLimitedMoves(), solution.asLimitedMoves())

    pygame.quit()