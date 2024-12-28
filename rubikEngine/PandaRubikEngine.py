#! /usr/bin/python

from rubikEngine.RubikEngine import RubikEngine
from panda3d.core import Vec3
import numpy as np
import time
import os

class PandaRubikEngine(RubikEngine):
    def __init__(self, position_x, position_y, position_z, viewer3D):

        self.viewer3D = viewer3D

        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z

        # Load central cubes        
        self.rotation_cube = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/central_cube.gltf")
        self.rotation_cube.setPos(position_x, position_y, position_z)
        self.rotation_cube.reparentTo(self.viewer3D.render)

        self.static_cube = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/central_cube.gltf")
        self.static_cube.setPos(position_x, position_y, position_z)
        self.static_cube.reparentTo(self.viewer3D.render)

        # Load down face cubes
        self.cube_front_down_left_corner = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/corner_cubes/cube_front_down_left_corner.gltf")
        self.cube_front_down_left_corner.reparentTo(self.static_cube)

        self.cube_front_down_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_front_down_edge.gltf")
        self.cube_front_down_edge.reparentTo(self.static_cube)

        self.cube_front_down_right_corner = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/corner_cubes/cube_front_down_right_corner.gltf")
        self.cube_front_down_right_corner.reparentTo(self.static_cube)
        
        self.cube_down_left_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_down_left_edge.gltf")
        self.cube_down_left_edge.reparentTo(self.static_cube)

        self.cube_down_center = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/center_cubes/cube_down_center.gltf")
        self.cube_down_center.reparentTo(self.static_cube)

        self.cube_down_right_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_down_right_edge.gltf")
        self.cube_down_right_edge.reparentTo(self.static_cube)

        self.cube_back_down_left_corner = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/corner_cubes/cube_back_down_left_corner.gltf")
        self.cube_back_down_left_corner.reparentTo(self.static_cube)

        self.cube_back_down_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_back_down_edge.gltf")
        self.cube_back_down_edge.reparentTo(self.static_cube)

        self.cube_back_down_right_corner = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/corner_cubes/cube_back_down_right_corner.gltf")
        self.cube_back_down_right_corner.reparentTo(self.static_cube)

        # Load up face cubes
        self.cube_front_up_left_corner = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/corner_cubes/cube_front_up_left_corner.gltf")
        self.cube_front_up_left_corner.reparentTo(self.static_cube)

        self.cube_front_up_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_front_up_edge.gltf")
        self.cube_front_up_edge.reparentTo(self.static_cube)

        self.cube_front_up_right_corner = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/corner_cubes/cube_front_up_right_corner.gltf")
        self.cube_front_up_right_corner.reparentTo(self.static_cube)
        
        self.cube_up_left_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_up_left_edge.gltf")
        self.cube_up_left_edge.reparentTo(self.static_cube)

        self.cube_up_center = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/center_cubes/cube_up_center.gltf")
        self.cube_up_center.reparentTo(self.static_cube)

        self.cube_up_right_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_up_right_edge.gltf")
        self.cube_up_right_edge.reparentTo(self.static_cube)

        self.cube_back_up_left_corner = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/corner_cubes/cube_back_up_left_corner.gltf")
        self.cube_back_up_left_corner.reparentTo(self.static_cube)

        self.cube_back_up_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_back_up_edge.gltf")
        self.cube_back_up_edge.reparentTo(self.static_cube)

        self.cube_back_up_right_corner = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/corner_cubes/cube_back_up_right_corner.gltf")
        self.cube_back_up_right_corner.reparentTo(self.static_cube)

        # Load front face cubes
        self.cube_front_left_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_front_left_edge.gltf")
        self.cube_front_left_edge.reparentTo(self.static_cube)

        self.cube_front_center = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/center_cubes/cube_front_center.gltf")
        self.cube_front_center.reparentTo(self.static_cube)

        self.cube_front_right_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_front_right_edge.gltf")
        self.cube_front_right_edge.reparentTo(self.static_cube)

        # Load back face cubes
        self.cube_back_right_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_back_right_edge.gltf")
        self.cube_back_right_edge.reparentTo(self.static_cube)

        self.cube_back_center = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/center_cubes/cube_back_center.gltf")
        self.cube_back_center.reparentTo(self.static_cube)

        self.cube_back_left_edge = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/edge_cubes/cube_back_left_edge.gltf")
        self.cube_back_left_edge.reparentTo(self.static_cube)

        # Load left face cube
        self.cube_left_center = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/center_cubes/cube_left_center.gltf")
        self.cube_left_center.reparentTo(self.static_cube)

        # Load left face cube
        self.cube_right_center = self.viewer3D.loader.loadModel(os.getcwd() + "/3DBlenderObjects/center_cubes/cube_right_center.gltf")
        self.cube_right_center.reparentTo(self.static_cube)

        downFace = np.array([
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

        leftFace = np.array([
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

        upFace = np.array([
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

        frontFace = np.array([
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

        backFace = np.array([
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

        rightFace = np.array([
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

        # Define rotation intervals
        self.z_axis_cw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(360, 0, 0))
        self.z_axis_ccw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(-360, 0, 0))
        self.x_axis_cw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(0, 360, 0))
        self.x_axis_ccw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(0, -360, 0))
        self.y_axis_cw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(0, 0, 360))
        self.y_axis_ccw_rot_interval = self.rotation_cube.hprInterval(1.0, Vec3(0, 0, -360))

        super().__init__(downFace, leftFace, upFace, frontFace, backFace, rightFace)

    def applyU(self) :
        super().applyU()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.upFace:
            for cube in line:
                self.reparentCube(cube, self.rotation_cube)
        self.y_axis_cw_rot_interval.start(0, 0.25)

    def applyPrimeU(self) :
        super().applyPrimeU()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.upFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.y_axis_ccw_rot_interval.start(0, 0.25)

    def applyD(self) :
        super().applyD()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.downFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.y_axis_ccw_rot_interval.start(0, 0.25)

    def applyPrimeD(self) :
        super().applyPrimeD()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.downFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.y_axis_cw_rot_interval.start(0, 0.25)

    def applyR(self) :
        super().applyR()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.rightFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.x_axis_cw_rot_interval.start(0, 0.25)

    def applyPrimeR(self) :
        super().applyPrimeR()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.rightFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.x_axis_ccw_rot_interval.start(0, 0.25)
        
    def applyL(self) :
        super().applyL()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.leftFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.x_axis_ccw_rot_interval.start(0, 0.25)

    def applyPrimeL(self) :
        super().applyPrimeL()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.leftFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.x_axis_cw_rot_interval.start(0, 0.25)

    def applyF(self) :
        super().applyF()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.frontFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.z_axis_ccw_rot_interval.start(0, 0.25)

    def applyPrimeF(self) :
        super().applyPrimeF()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.frontFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.z_axis_cw_rot_interval.start(0, 0.25)

    def applyB(self) :
        super().applyB()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.backFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.z_axis_cw_rot_interval.start(0, 0.25)

    def applyPrimeB(self) :
        super().applyPrimeB()

        self.reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        for line in self.backFace:
            for cube in line:
                cube[0].reparentTo(self.rotation_cube)
        self.z_axis_ccw_rot_interval.start(0, 0.25)

    def reparentCubie(self, cubie, parent):
        cubie[1] = cubie[0].getPos(self.viewer3D.scene)
        cubie[2] = cubie[0].getHpr(self.viewer3D.scene)
        cubie[0].reparentTo(parent)
        cubie[0].setHpr(self.viewer3D.scene, cubie[2])

    def reparentFace(self, face, parent):
        for line in face:
            for cubie in line:
                self.reparentCubie(cubie, parent)

    def reparentAll(self, parent):
        self.reparentFace(self.downFace, parent)
        self.reparentFace(self.upFace, parent)
        self.reparentFace(self.frontFace, parent)
        self.reparentFace(self.backFace, parent)
        self.reparentFace(self.rightFace, parent)
        self.reparentFace(self.leftFace, parent)