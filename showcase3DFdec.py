#! /usr/bin/python

import os
import sys
import time
from math import pi, sin, cos
import numpy as np
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Vec3
from panda3d.core import Point3
from panda3d.core import Shader
from panda3d.core import AntialiasAttrib
from direct.interval.IntervalGlobal import *
from rubikState import Moves

import simplepbr


class Viewer3d(ShowBase):
    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def __init__(self, mix, solution):
        self.mix = mix
        self.solution = solution
        ShowBase.__init__(self)
        simplepbr.init()

        self.loadCube()

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

        # Define rotation intervals
        self.z_axis_cw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(360, 0, 0))
        self.z_axis_ccw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(-360, 0, 0))
        self.x_axis_cw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(0, 360, 0))
        self.x_axis_ccw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(0, -360, 0))
        self.y_axis_cw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(0, 0, 360))
        self.y_axis_ccw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(0, 0, -360))

        self.accept('escape', sys.exit)
        self.accept('m', self.mixCube)
        self.accept('s', self.solveCube)

    def reparentCube(self, cube, parent):
        # cube[1] = cube[0].getPos(self.scene)
        cube[2] = cube[0].getHpr(self.scene)
        cube[0].reparentTo(parent)
        cube[0].setHpr(self.scene, cube[2])

    def reparentFace(self, face, parent):
        for line in face:
            for cube in line:
                self.reparentCube(cube, parent)

    def reparentAll(self, parent):
        self.reparentFace(self.downFace, parent)
        self.reparentFace(self.upFace, parent)
        self.reparentFace(self.frontFace, parent)
        self.reparentFace(self.backFace, parent)
        self.reparentFace(self.rightFace, parent)
        self.reparentFace(self.leftFace, parent)

    def __rotateFaceCW(self, oldFace) :
        newFace = np.array([[oldFace[2][0], oldFace[1][0], oldFace[0][0]], [oldFace[2][1], oldFace[1][1], oldFace[0][1]], [oldFace[2][2], oldFace[1][2], oldFace[0][2]]])
        return newFace

    def __rotateFaceCCW(self, oldFace) :
        newFace = np.array([[oldFace[0][2], oldFace[1][2], oldFace[2][2]], [oldFace[0][1], oldFace[1][1], oldFace[2][1]], [oldFace[0][0], oldFace[1][0], oldFace[2][0]]])
        return newFace

    def applyU(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.upFace:
            for cube in line:
                self.reparentCube(cube, self.rotation_cube)
        self.y_axis_cw_rot_interval.start(0, 0.25)

        # Apply state move
        self.upFace = self.__rotateFaceCW(self.upFace)

        newFrontFace = self.frontFace.copy()
        newBackFace = self.backFace.copy()
        newRightFace = self.rightFace.copy()
        newLeftFace = self.leftFace.copy()

        newFrontFace[0] = self.rightFace[0]
        newBackFace[0] = self.leftFace[0]
        newRightFace[0] = self.backFace[0]
        newLeftFace[0] = self.frontFace[0]

        self.frontFace = newFrontFace
        self.backFace = newBackFace
        self.rightFace = newRightFace
        self.leftFace = newLeftFace

    def applyPrimeU(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.upFace:
            for cube in line:
                self.reparentCube(cube, self.rotation_cube)
        self.y_axis_ccw_rot_interval.start(0, 0.25)

        # Apply state move
        self.upFace = self.__rotateFaceCCW(self.upFace)

        newFrontFace = self.frontFace.copy()
        newBackFace = self.backFace.copy()
        newRightFace = self.rightFace.copy()
        newLeftFace = self.leftFace.copy()

        newFrontFace[0] = self.leftFace[0]
        newBackFace[0] = self.rightFace[0]
        newRightFace[0] = self.frontFace[0]
        newLeftFace[0] = self.backFace[0]

        self.frontFace = newFrontFace
        self.backFace = newBackFace
        self.rightFace = newRightFace
        self.leftFace = newLeftFace

    def applyTwoU(self) : 
        self.applyU()
        self.applyU()

    def applyD(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.downFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.y_axis_ccw_rot_interval.start(0, 0.25)

        # Apply state move
        self.downFace = self.__rotateFaceCW(self.downFace)

        newFrontFace = self.frontFace.copy()
        newBackFace = self.backFace.copy()
        newRightFace = self.rightFace.copy()
        newLeftFace = self.leftFace.copy()

        newFrontFace[2] = self.leftFace[2]
        newBackFace[2] = self.rightFace[2]
        newRightFace[2] = self.frontFace[2]
        newLeftFace[2] = self.backFace[2]

        self.frontFace = newFrontFace
        self.backFace = newBackFace
        self.rightFace = newRightFace
        self.leftFace = newLeftFace

    def applyPrimeD(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.downFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.y_axis_cw_rot_interval.start(0, 0.25)

        # Apply state move
        self.downFace = self.__rotateFaceCCW(self.downFace)

        newFrontFace = self.frontFace.copy()
        newBackFace = self.backFace.copy()
        newRightFace = self.rightFace.copy()
        newLeftFace = self.leftFace.copy()

        newFrontFace[2] = self.rightFace[2]
        newBackFace[2] = self.leftFace[2]
        newRightFace[2] = self.backFace[2]
        newLeftFace[2] = self.frontFace[2]

        self.frontFace = newFrontFace
        self.backFace = newBackFace
        self.rightFace = newRightFace
        self.leftFace = newLeftFace

    def applyTwoD(self) : 
        self.applyD()
        self.applyD()

    def applyR(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.rightFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.x_axis_cw_rot_interval.start(0, 0.25)

        # Apply state move
        self.rightFace = self.__rotateFaceCW(self.rightFace)

        newFrontFace = self.frontFace.copy()
        newBackFace = self.backFace.copy()
        newUpFace = self.upFace.copy()
        newDownFace = self.downFace.copy()

        newFrontFace[0][2] = self.downFace[0][2]
        newFrontFace[1][2] = self.downFace[1][2]
        newFrontFace[2][2] = self.downFace[2][2]

        newBackFace[0][0] = self.upFace[2][2]
        newBackFace[1][0] = self.upFace[1][2]
        newBackFace[2][0] = self.upFace[0][2]

        newUpFace[0][2] = self.frontFace[0][2]
        newUpFace[1][2] = self.frontFace[1][2]
        newUpFace[2][2] = self.frontFace[2][2]

        newDownFace[0][2] = self.backFace[2][0]
        newDownFace[1][2] = self.backFace[1][0]
        newDownFace[2][2] = self.backFace[0][0]

        self.frontFace = newFrontFace
        self.backFace = newBackFace
        self.upFace = newUpFace
        self.downFace = newDownFace

    def applyPrimeR(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.rightFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.x_axis_ccw_rot_interval.start(0, 0.25)

        # Apply state move
        self.rightFace = self.__rotateFaceCCW(self.rightFace)

        newFrontFace = self.frontFace.copy()
        newBackFace = self.backFace.copy()
        newUpFace = self.upFace.copy()
        newDownFace = self.downFace.copy()

        newFrontFace[0][2] = self.upFace[0][2]
        newFrontFace[1][2] = self.upFace[1][2]
        newFrontFace[2][2] = self.upFace[2][2]

        newBackFace[0][0] = self.downFace[2][2]
        newBackFace[1][0] = self.downFace[1][2]
        newBackFace[2][0] = self.downFace[0][2]

        newUpFace[0][2] = self.backFace[2][0]
        newUpFace[1][2] = self.backFace[1][0]
        newUpFace[2][2] = self.backFace[0][0]

        newDownFace[0][2] = self.frontFace[0][2]
        newDownFace[1][2] = self.frontFace[1][2]
        newDownFace[2][2] = self.frontFace[2][2]

        self.frontFace = newFrontFace
        self.backFace = newBackFace
        self.upFace = newUpFace
        self.downFace = newDownFace

    def applyTwoR(self) : 
        self.applyR()
        self.applyR()
        
    def applyL(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.leftFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.x_axis_ccw_rot_interval.start(0, 0.25)

        # Apply state move
        self.leftFace = self.__rotateFaceCW(self.leftFace)

        newFrontFace = self.frontFace.copy()
        newBackFace = self.backFace.copy()
        newUpFace = self.upFace.copy()
        newDownFace = self.downFace.copy()

        newFrontFace[0][0] = self.upFace[0][0]
        newFrontFace[1][0] = self.upFace[1][0]
        newFrontFace[2][0] = self.upFace[2][0]

        newBackFace[0][2] = self.downFace[2][0]
        newBackFace[1][2] = self.downFace[1][0]
        newBackFace[2][2] = self.downFace[0][0]

        newUpFace[0][0] = self.backFace[2][2]
        newUpFace[1][0] = self.backFace[1][2]
        newUpFace[2][0] = self.backFace[0][2]

        newDownFace[0][0] = self.frontFace[0][0]
        newDownFace[1][0] = self.frontFace[1][0]
        newDownFace[2][0] = self.frontFace[2][0]

        self.frontFace = newFrontFace
        self.backFace = newBackFace
        self.upFace = newUpFace
        self.downFace = newDownFace

    def applyPrimeL(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.leftFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.x_axis_cw_rot_interval.start(0, 0.25)

        # Apply state move
        self.leftFace = self.__rotateFaceCCW(self.leftFace)

        newFrontFace = self.frontFace.copy()
        newBackFace = self.backFace.copy()
        newUpFace = self.upFace.copy()
        newDownFace = self.downFace.copy()

        newFrontFace[0][0] = self.downFace[0][0]
        newFrontFace[1][0] = self.downFace[1][0]
        newFrontFace[2][0] = self.downFace[2][0]

        newBackFace[0][2] = self.upFace[2][0]
        newBackFace[1][2] = self.upFace[1][0]
        newBackFace[2][2] = self.upFace[0][0]

        newUpFace[0][0] = self.frontFace[0][0]
        newUpFace[1][0] = self.frontFace[1][0]
        newUpFace[2][0] = self.frontFace[2][0]

        newDownFace[0][0] = self.backFace[2][2]
        newDownFace[1][0] = self.backFace[1][2]
        newDownFace[2][0] = self.backFace[0][2]

        self.frontFace = newFrontFace
        self.backFace = newBackFace
        self.upFace = newUpFace
        self.downFace = newDownFace

    def applyTwoL(self) : 
        self.applyL()
        self.applyL()

    def applyF(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.frontFace:
            for cube in line:
                self.reparentCube(cube, self.rotation_cube)
        self.z_axis_ccw_rot_interval.start(0, 0.25)

        # Apply state move
        self.frontFace = self.__rotateFaceCW(self.frontFace)

        newRightFace = self.rightFace.copy()
        newLeftFace = self.leftFace.copy()
        newUpFace = self.upFace.copy()
        newDownFace = self.downFace.copy()

        newRightFace[0][0] = self.upFace[2][0]
        newRightFace[1][0] = self.upFace[2][1]
        newRightFace[2][0] = self.upFace[2][2]

        newLeftFace[0][2] = self.downFace[0][0]
        newLeftFace[1][2] = self.downFace[0][1]
        newLeftFace[2][2] = self.downFace[0][2]

        newUpFace[2][0] = self.leftFace[2][2]
        newUpFace[2][1] = self.leftFace[1][2]
        newUpFace[2][2] = self.leftFace[0][2]

        newDownFace[0][0] = self.rightFace[2][0]
        newDownFace[0][1] = self.rightFace[1][0]
        newDownFace[0][2] = self.rightFace[0][0]

        self.rightFace = newRightFace
        self.leftFace = newLeftFace
        self.upFace = newUpFace
        self.downFace = newDownFace

    def applyPrimeF(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.frontFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.z_axis_cw_rot_interval.start(0, 0.25)

        # Apply state move
        self.frontFace = self.__rotateFaceCCW(self.frontFace)

        newRightFace = self.rightFace.copy()
        newLeftFace = self.leftFace.copy()
        newUpFace = self.upFace.copy()
        newDownFace = self.downFace.copy()

        newRightFace[0][0] = self.downFace[0][2]
        newRightFace[1][0] = self.downFace[0][1]
        newRightFace[2][0] = self.downFace[0][0]

        newLeftFace[0][2] = self.upFace[2][2]
        newLeftFace[1][2] = self.upFace[2][1]
        newLeftFace[2][2] = self.upFace[2][0]

        newUpFace[2][0] = self.rightFace[0][0]
        newUpFace[2][1] = self.rightFace[1][0]
        newUpFace[2][2] = self.rightFace[2][0]

        newDownFace[0][0] = self.leftFace[0][2]
        newDownFace[0][1] = self.leftFace[1][2]
        newDownFace[0][2] = self.leftFace[2][2]

        self.rightFace = newRightFace
        self.leftFace = newLeftFace
        self.upFace = newUpFace
        self.downFace = newDownFace

    def applyTwoF(self) : 
        self.applyF()
        self.applyF()

    def applyB(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.backFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.z_axis_cw_rot_interval.start(0, 0.25)

        # Apply state move
        self.backFace = self.__rotateFaceCW(self.backFace)

        newRightFace = self.rightFace.copy()
        newLeftFace = self.leftFace.copy()
        newUpFace = self.upFace.copy()
        newDownFace = self.downFace.copy()

        newRightFace[0][2] = self.downFace[2][2]
        newRightFace[1][2] = self.downFace[2][1]
        newRightFace[2][2] = self.downFace[2][0]

        newLeftFace[0][0] = self.upFace[0][2]
        newLeftFace[1][0] = self.upFace[0][1]
        newLeftFace[2][0] = self.upFace[0][0]

        newUpFace[0][0] = self.rightFace[0][2]
        newUpFace[0][1] = self.rightFace[1][2]
        newUpFace[0][2] = self.rightFace[2][2]

        newDownFace[2][0] = self.leftFace[0][0]
        newDownFace[2][1] = self.leftFace[1][0]
        newDownFace[2][2] = self.leftFace[2][0]

        self.rightFace = newRightFace
        self.leftFace = newLeftFace
        self.upFace = newUpFace
        self.downFace = newDownFace


    def applyPrimeB(self) :
        # Apply graphical move
        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.backFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.z_axis_ccw_rot_interval.start(0, 0.25)

        # Apply state move
        self.backFace = self.__rotateFaceCCW(self.backFace)

        newRightFace = self.rightFace.copy()
        newLeftFace = self.leftFace.copy()
        newUpFace = self.upFace.copy()
        newDownFace = self.downFace.copy()

        newRightFace[0][2] = self.upFace[0][0]
        newRightFace[1][2] = self.upFace[0][1]
        newRightFace[2][2] = self.upFace[0][2]

        newLeftFace[0][0] = self.downFace[2][0]
        newLeftFace[1][0] = self.downFace[2][1]
        newLeftFace[2][0] = self.downFace[2][2]

        newUpFace[0][0] = self.leftFace[2][0]
        newUpFace[0][1] = self.leftFace[1][0]
        newUpFace[0][2] = self.leftFace[0][0]

        newDownFace[2][0] = self.rightFace[2][2]
        newDownFace[2][1] = self.rightFace[1][2]
        newDownFace[2][2] = self.rightFace[0][2]

        self.rightFace = newRightFace
        self.leftFace = newLeftFace
        self.upFace = newUpFace
        self.downFace = newDownFace

    def applyTwoB(self) : 
        self.applyB()
        self.applyB()


    def applyMove(self, move) :
        match move:
            case "F" :
                self.applyF()
            case "B" :
                self.applyB()
            case "U" :
                self.applyU()
            case "D" :
                self.applyD()
            case "R" :
                self.applyR()
            case "L" :
                self.applyL()
            case "F'" :
                self.applyPrimeF()
            case "B'" :
                self.applyPrimeB()
            case "U'" :
                self.applyPrimeU()
            case "D'" :
                self.applyPrimeD()
            case "R'" :
                self.applyPrimeR()
            case "L'" :
                self.applyPrimeL()
            case "2F" :
                self.applyTwoF()
            case "2B" :
                self.applyTwoB()
            case "2U" :
                self.applyTwoU()
            case "2D" :
                self.applyTwoD()
            case "2R" :
                self.applyTwoR()
            case "2L" :
                self.applyTwoL()

    def mixTaskFunction(self, task):
        self.applyMove(self.mix[self.mixIndex])
        self.mixIndex += 1
        if self.mixIndex < len(self.mix):
            return task.again

    def mixCube(self):
        self.mixIndex = 0
        mixTask = taskMgr.doMethodLater(0.5, self.mixTaskFunction, 'mixTask')

    def solveTaskFunction(self, task):
        self.applyMove(self.solution[self.solveIndex])
        self.solveIndex += 1
        if self.solveIndex < len(self.solution):
            return task.again

    def solveCube(self):
        self.solveIndex = 0
        solveTask = taskMgr.doMethodLater(0.5, self.solveTaskFunction, 'solveTask')

    def loadCube(self):
        # Load central cubes        
        self.rotation_cube = self.loader.loadModel(os.getcwd() + "/3dModels/central_cube.gltf")
        self.rotation_cube.setZ(3)
        self.rotation_cube.reparentTo(self.render)

        self.static_cube = self.loader.loadModel(os.getcwd() + "./3dModels/central_cube.gltf")
        self.static_cube.setZ(3)
        self.static_cube.reparentTo(self.render)

        # Load down face cubes
        self.cube_front_down_left_corner = self.loader.loadModel(os.getcwd() + "/3dModels/corner_cubes/cube_front_down_left_corner.gltf")
        self.cube_front_down_left_corner.reparentTo(self.static_cube)

        self.cube_front_down_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_front_down_edge.gltf")
        self.cube_front_down_edge.reparentTo(self.static_cube)

        self.cube_front_down_right_corner = self.loader.loadModel(os.getcwd() + "/3dModels/corner_cubes/cube_front_down_right_corner.gltf")
        self.cube_front_down_right_corner.reparentTo(self.static_cube)
        
        self.cube_down_left_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_down_left_edge.gltf")
        self.cube_down_left_edge.reparentTo(self.static_cube)

        self.cube_down_center = self.loader.loadModel(os.getcwd() + "/3dModels/center_cubes/cube_down_center.gltf")
        self.cube_down_center.reparentTo(self.static_cube)

        self.cube_down_right_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_down_right_edge.gltf")
        self.cube_down_right_edge.reparentTo(self.static_cube)

        self.cube_back_down_left_corner = self.loader.loadModel(os.getcwd() + "/3dModels/corner_cubes/cube_back_down_left_corner.gltf")
        self.cube_back_down_left_corner.reparentTo(self.static_cube)

        self.cube_back_down_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_back_down_edge.gltf")
        self.cube_back_down_edge.reparentTo(self.static_cube)

        self.cube_back_down_right_corner = self.loader.loadModel(os.getcwd() + "/3dModels/corner_cubes/cube_back_down_right_corner.gltf")
        self.cube_back_down_right_corner.reparentTo(self.static_cube)

        # Load up face cubes
        self.cube_front_up_left_corner = self.loader.loadModel(os.getcwd() + "/3dModels/corner_cubes/cube_front_up_left_corner.gltf")
        self.cube_front_up_left_corner.reparentTo(self.static_cube)

        self.cube_front_up_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_front_up_edge.gltf")
        self.cube_front_up_edge.reparentTo(self.static_cube)

        self.cube_front_up_right_corner = self.loader.loadModel(os.getcwd() + "/3dModels/corner_cubes/cube_front_up_right_corner.gltf")
        self.cube_front_up_right_corner.reparentTo(self.static_cube)
        
        self.cube_up_left_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_up_left_edge.gltf")
        self.cube_up_left_edge.reparentTo(self.static_cube)

        self.cube_up_center = self.loader.loadModel(os.getcwd() + "/3dModels/center_cubes/cube_up_center.gltf")
        self.cube_up_center.reparentTo(self.static_cube)

        self.cube_up_right_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_up_right_edge.gltf")
        self.cube_up_right_edge.reparentTo(self.static_cube)

        self.cube_back_up_left_corner = self.loader.loadModel(os.getcwd() + "/3dModels/corner_cubes/cube_back_up_left_corner.gltf")
        self.cube_back_up_left_corner.reparentTo(self.static_cube)

        self.cube_back_up_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_back_up_edge.gltf")
        self.cube_back_up_edge.reparentTo(self.static_cube)

        self.cube_back_up_right_corner = self.loader.loadModel(os.getcwd() + "/3dModels/corner_cubes/cube_back_up_right_corner.gltf")
        self.cube_back_up_right_corner.reparentTo(self.static_cube)

        # Load front face cubes
        self.cube_front_left_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_front_left_edge.gltf")
        self.cube_front_left_edge.reparentTo(self.static_cube)

        self.cube_front_center = self.loader.loadModel(os.getcwd() + "/3dModels/center_cubes/cube_front_center.gltf")
        self.cube_front_center.reparentTo(self.static_cube)

        self.cube_front_right_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_front_right_edge.gltf")
        self.cube_front_right_edge.reparentTo(self.static_cube)

        # Load back face cubes
        self.cube_back_right_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_back_right_edge.gltf")
        self.cube_back_right_edge.reparentTo(self.static_cube)

        self.cube_back_center = self.loader.loadModel(os.getcwd() + "/3dModels/center_cubes/cube_back_center.gltf")
        self.cube_back_center.reparentTo(self.static_cube)

        self.cube_back_left_edge = self.loader.loadModel(os.getcwd() + "/3dModels/edge_cubes/cube_back_left_edge.gltf")
        self.cube_back_left_edge.reparentTo(self.static_cube)

        # Load left face cube
        self.cube_left_center = self.loader.loadModel(os.getcwd() + "/3dModels/center_cubes/cube_left_center.gltf")
        self.cube_left_center.reparentTo(self.static_cube)

        # Load left face cube
        self.cube_right_center = self.loader.loadModel(os.getcwd() + "/3dModels/center_cubes/cube_right_center.gltf")
        self.cube_right_center.reparentTo(self.static_cube)

        self.downFace = np.array([
            [
                (self.cube_front_down_left_corner, 0, 0),
                (self.cube_front_down_edge, 0, 0),
                (self.cube_front_down_right_corner, 0, 0)
            ],
            [
                (self.cube_down_left_edge, 0, 0),
                (self.cube_down_center, 0, 0),
                (self.cube_down_right_edge, 0, 0)
            ],
            [
                (self.cube_back_down_left_corner, 0, 0),
                (self.cube_back_down_edge, 0, 0),
                (self.cube_back_down_right_corner, 0, 0)
            ]
        ])

        self.leftFace = np.array([
            [
                (self.cube_back_up_left_corner, 0, 0),
                (self.cube_up_left_edge, 0, 0),
                (self.cube_front_up_left_corner, 0, 0)
            ],
            [
                (self.cube_back_left_edge, 0, 0),
                (self.cube_left_center, 0, 0),
                (self.cube_front_left_edge, 0, 0)
            ],
            [
                (self.cube_back_down_left_corner, 0, 0),
                (self.cube_down_left_edge, 0, 0),
                (self.cube_front_down_left_corner, 0, 0)
            ]
        ])

        self.upFace = np.array([
            [
                (self.cube_back_up_left_corner, 0, 0),
                (self.cube_back_up_edge, 0, 0),
                (self.cube_back_up_right_corner, 0, 0)
            ],
            [
                (self.cube_up_left_edge, 0, 0),
                (self.cube_up_center, 0, 0),
                (self.cube_up_right_edge, 0, 0)
            ],
            [
                (self.cube_front_up_left_corner, 0, 0),
                (self.cube_front_up_edge, 0, 0),
                (self.cube_front_up_right_corner, 0, 0)
            ]
        ])

        self.frontFace = np.array([
            [
                (self.cube_front_up_left_corner, 0, 0),
                (self.cube_front_up_edge, 0, 0),
                (self.cube_front_up_right_corner, 0, 0)
            ],
            [
                (self.cube_front_left_edge, 0, 0),
                (self.cube_front_center, 0, 0),
                (self.cube_front_right_edge, 0, 0)
            ],
            [
                (self.cube_front_down_left_corner, 0, 0),
                (self.cube_front_down_edge, 0, 0),
                (self.cube_front_down_right_corner, 0, 0)
            ]
        ])

        self.backFace = np.array([
            [
                (self.cube_back_up_right_corner, 0, 0),
                (self.cube_back_up_edge, 0, 0),
                (self.cube_back_up_left_corner, 0, 0)
            ],
            [
                (self.cube_back_right_edge, 0, 0),
                (self.cube_back_center, 0, 0),
                (self.cube_back_left_edge, 0, 0)
            ],
            [
                (self.cube_back_down_right_corner, 0, 0),
                (self.cube_back_down_edge, 0, 0),
                (self.cube_back_down_left_corner, 0, 0)
            ]
        ])

        self.rightFace = np.array([
            [
                (self.cube_front_up_right_corner, 0, 0),
                (self.cube_up_right_edge, 0, 0),
                (self.cube_back_up_right_corner, 0, 0)
            ],
            [
                (self.cube_front_right_edge, 0, 0),
                (self.cube_right_center, 0, 0),
                (self.cube_back_right_edge, 0, 0)
            ],
            [
                (self.cube_front_down_right_corner, 0, 0),
                (self.cube_down_right_edge, 0, 0),
                (self.cube_back_down_right_corner, 0, 0)
            ]
        ])

def showcaseFdec(mix, solution):
    viewer = Viewer3d(mix, solution)
    viewer.run()