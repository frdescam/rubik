#! /usr/bin/python

import os
import sys
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Vec3
from panda3d.core import Point3
from panda3d.core import Shader
from panda3d.core import AntialiasAttrib
from direct.interval.IntervalGlobal import *

import simplepbr


class MyApp(ShowBase):
    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def __init__(self):
        ShowBase.__init__(self)
        simplepbr.init()
        self.render.setAntialias(AntialiasAttrib.MMultisample)
        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        
        # Load and transform the cube actor.
        self.rotation_cube = self.loader.loadModel(os.getcwd() + "/rubik/central_cube.gltf")
        self.rotation_cube.setZ(3)
        self.rotation_cube.reparentTo(self.render)

        self.static_cube = self.loader.loadModel(os.getcwd() + "/rubik/central_cube.gltf")
        self.static_cube.setZ(3)
        self.static_cube.reparentTo(self.render)

        self.white_cube = self.loader.loadModel(os.getcwd() + "/rubik/cube_0_0_white.gltf")
        self.white_cube.reparentTo(self.static_cube)
        self.white_cube2 = self.loader.loadModel(os.getcwd() + "/rubik/cube_0_2_white.gltf")
        self.white_cube2.reparentTo(self.static_cube)
        self.orange_cube = self.loader.loadModel(os.getcwd() + "/rubik/cube_0_2_orange.gltf")
        self.orange_cube.reparentTo(self.static_cube)

        self.interval1 = self.rotation_cube.hprInterval(1.0, Vec3(360, 0, 0))

        self.interval2 = self.rotation_cube.hprInterval(1.0, Vec3(0, 360, 0))

        self.accept('escape', sys.exit)
        self.accept('a', self.sampleMove)
        # self.accept('x', self.unparentAll)
        self.accept('z', self.sampleMove2)

    # def unparentAll(self):
    #     self.hpr = self.white_cube.getHpr(self.scene)
    #     self.white_cube.reparentTo(self.static_cube)
    #     self.white_cube2.reparentTo(self.static_cube)
    #     self.orange_cube.reparentTo(self.static_cube)
    #     self.white_cube.setHpr(self.scene, self.hpr)

    def sampleMove(self):
        if not self.interval2.isPlaying():
            self.wcHpr = self.white_cube.getHpr(self.scene)
            self.wc2Hpr = self.white_cube2.getHpr(self.scene)
            self.white_cube.reparentTo(self.rotation_cube)
            self.white_cube2.reparentTo(self.rotation_cube)
            self.orange_cube.reparentTo(self.static_cube)
            self.white_cube.setHpr(self.scene, self.wcHpr)
            self.white_cube2.setHpr(self.scene, self.wc2Hpr)
            self.interval1.start(0, 0.5)

    def sampleMove2(self):
        if not self.interval1.isPlaying():
            self.wcHpr = self.white_cube.getHpr(self.scene)
            self.wc2Hpr = self.white_cube2.getHpr(self.scene)
            self.rotation_cube.setHpr(0, 0, 0)
            self.white_cube.setHpr(self.scene, self.wcHpr)
            self.white_cube2.setHpr(self.scene, self.wc2Hpr)

            self.wcHpr = self.white_cube.getHpr(self.scene)
            self.wc2Hpr = self.white_cube2.getHpr(self.scene)
            self.white_cube.reparentTo(self.rotation_cube)
            self.white_cube2.reparentTo(self.rotation_cube)
            self.orange_cube.reparentTo(self.rotation_cube)
            self.white_cube.setHpr(self.scene, self.wcHpr)
            self.white_cube2.setHpr(self.scene, self.wc2Hpr)
            self.interval2.start(0, 0.5)

app = MyApp()
app.run()

def showcaseFdec(mix, solution):

    pygame.init()
    display_size = (800,600)
    screen = pygame.display.set_mode(display_size, DOUBLEBUF|OPENGL)

    glEnable(GL_DEPTH_TEST) 
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display_size[0]/display_size[1]), 0.1, 50.0)

    cube = Rubik3D(3, 2) # create a 3x3x3 rubik, scale of 2 
    cube.mainloop(mix, solution)

    pygame.quit()
    quit()

# Test
showcaseFdec()