#! /usr/bin/python

import os
import sys
import time
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import Shader
from panda3d.core import AntialiasAttrib
from direct.interval.IntervalGlobal import *
from cubeModel.PandaRubikState import PandaRubikState

import simplepbr

class Viewer3d(ShowBase):
    def __init__(self, mix, solution):
        self.mix = mix
        self.solution = solution
        ShowBase.__init__(self)
        simplepbr.init()
        base.disableMouse()

        self.cube = PandaRubikState(6, 6, 13, self)

        # Scene
        self.render.setAntialias(AntialiasAttrib.MMultisample)
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Camera
        self.camera_theta = pi / 4
        self.camera_phi = pi / 4
        self.camera_distance = 30

        self.update_camera_position()

        # Add the cameraFollowMouse procedure to the task manager
        # Handles mouse movments
        self.taskMgr.add(self.cameraFollowMouse, "cameraFollowMouse")

        # Catch Panda3D events
        self.accept('escape', sys.exit)
        self.accept('m', self.mixCube)
        self.accept('s', self.solveCube)
        self.accept('shift-=', self.zoomIn)
        # self.accept('wheel-up', self.zoomIn)
        self.accept('-', self.zoomOut)
        # self.accept('wheel-down', self.zoomOut)

        self.accept("mouse1", self.start_drag)
        self.accept("mouse1-up", self.stop_drag)

        # Inits
        self.mouse_dragging = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def cameraFollowMouse(self, task):
        if self.mouse_dragging and self.mouseWatcherNode.hasMouse():
            mouse_device = self.win.getPointer(0)
            mouse_x = mouse_device.getX()
            mouse_y = mouse_device.getY()

            theta_delta = (self.last_mouse_x - mouse_x) * 0.01
            phi_delta = (self.last_mouse_y - mouse_y) * 0.01

            self.last_mouse_x = mouse_x
            self.last_mouse_y = mouse_y

            self.camera_theta += theta_delta
            self.camera_phi = max(0.01, min(pi - 0.01, self.camera_phi + phi_delta))

            self.update_camera_position()

        return task.cont

    def update_camera_position(self):
        camera_x = self.camera_distance * sin(self.camera_phi) * cos(self.camera_theta) + self.cube.position_x
        camera_y = self.camera_distance * sin(self.camera_phi) * sin(self.camera_theta) + self.cube.position_y
        camera_z = self.camera_distance * cos(self.camera_phi) + self.cube.position_z

        self.camera.setPos(camera_x, camera_y, camera_z)
        self.make_camera_look_at_cube()

    def make_camera_look_at_cube(self):
        self.camera.lookAt(self.cube.position_x, self.cube.position_y, self.cube.position_z)

    def start_drag(self):
        if self.mouseWatcherNode.hasMouse():
            mouse_device = self.win.getPointer(0)
            mouse_x = mouse_device.getX()
            mouse_y = mouse_device.getY()

            if (self.last_mouse_x == 0):
                self.last_mouse_x = mouse_x
                self.last_mouse_y = mouse_y

            self.mouse_dragging = True

    def stop_drag(self):
        self.mouse_dragging = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0

    def zoomIn(self):
        self.camera_distance = max(self.camera_distance - 1, 20)
        self.update_camera_position()

    def zoomOut(self):
        self.camera_distance += 1
        self.update_camera_position()

    def mixTaskFunction(self, task):
        self.cube.applyMove(self.mix[self.mixIndex])
        self.mixIndex += 1
        if self.mixIndex < len(self.mix):
            return task.again

    def mixCube(self):
        self.mixIndex = 0
        mixTask = taskMgr.doMethodLater(0.5, self.mixTaskFunction, 'mixTask')

    def solveTaskFunction(self, task):
        self.cube.applyMove(self.solution[self.solveIndex])
        self.solveIndex += 1
        if self.solveIndex < len(self.solution):
            return task.again

    def solveCube(self):
        self.solveIndex = 0
        solveTask = taskMgr.doMethodLater(0.5, self.solveTaskFunction, 'solveTask')

def showcase3DFdec(mix, solution):
    viewer = Viewer3d(mix, solution)
    viewer.run()