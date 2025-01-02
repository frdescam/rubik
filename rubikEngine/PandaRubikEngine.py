#! /usr/bin/python

from rubikEngine.RubikEngine import RubikEngine
from RubikMoves import Moves
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
                self.cube_front_down_left_corner,
                self.cube_front_down_edge,
                self.cube_front_down_right_corner
            ],
            [
                self.cube_down_left_edge,
                self.cube_down_center,
                self.cube_down_right_edge
            ],
            [
                self.cube_back_down_left_corner,
                self.cube_back_down_edge,
                self.cube_back_down_right_corner
            ]
        ])

        leftFace = np.array([
            [
                self.cube_back_up_left_corner,
                self.cube_up_left_edge,
                self.cube_front_up_left_corner
            ],
            [
                self.cube_back_left_edge,
                self.cube_left_center,
                self.cube_front_left_edge
            ],
            [
                self.cube_back_down_left_corner,
                self.cube_down_left_edge,
                self.cube_front_down_left_corner
            ]
        ])

        upFace = np.array([
            [
                self.cube_back_up_left_corner,
                self.cube_back_up_edge,
                self.cube_back_up_right_corner
            ],
            [
                self.cube_up_left_edge,
                self.cube_up_center,
                self.cube_up_right_edge
            ],
            [
                self.cube_front_up_left_corner,
                self.cube_front_up_edge,
                self.cube_front_up_right_corner
            ]
        ])

        frontFace = np.array([
            [
                self.cube_front_up_left_corner,
                self.cube_front_up_edge,
                self.cube_front_up_right_corner
            ],
            [
                self.cube_front_left_edge,
                self.cube_front_center,
                self.cube_front_right_edge
            ],
            [
                self.cube_front_down_left_corner,
                self.cube_front_down_edge,
                self.cube_front_down_right_corner
            ]
        ])

        backFace = np.array([
            [
                self.cube_back_up_right_corner,
                self.cube_back_up_edge,
                self.cube_back_up_left_corner
            ],
            [
                self.cube_back_right_edge,
                self.cube_back_center,
                self.cube_back_left_edge
            ],
            [
                self.cube_back_down_right_corner,
                self.cube_back_down_edge,
                self.cube_back_down_left_corner
            ]
        ])

        rightFace = np.array([
            [
                self.cube_front_up_right_corner,
                self.cube_up_right_edge,
                self.cube_back_up_right_corner
            ],
            [
                self.cube_front_right_edge,
                self.cube_right_center,
                self.cube_back_right_edge
            ],
            [
                self.cube_front_down_right_corner,
                self.cube_down_right_edge,
                self.cube_back_down_right_corner
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

    def _applyU(self) :
        super()._applyU()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.upFace, self.rotation_cube)
        self.y_axis_cw_rot_interval.start(0, 0.25)

    def _applyPrimeU(self) :
        super()._applyPrimeU()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.upFace, self.rotation_cube)
        self.y_axis_ccw_rot_interval.start(0, 0.25)

    def _applyD(self) :
        super()._applyD()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.downFace, self.rotation_cube)
        self.y_axis_ccw_rot_interval.start(0, 0.25)

    def _applyPrimeD(self) :
        super()._applyPrimeD()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.downFace, self.rotation_cube)
        self.y_axis_cw_rot_interval.start(0, 0.25)

    def _applyR(self) :
        super()._applyR()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.rightFace, self.rotation_cube)
        self.x_axis_cw_rot_interval.start(0, 0.25)

    def _applyPrimeR(self) :
        super()._applyPrimeR()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.rightFace, self.rotation_cube)
        self.x_axis_ccw_rot_interval.start(0, 0.25)
        
    def _applyL(self) :
        super()._applyL()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.leftFace, self.rotation_cube)
        self.x_axis_ccw_rot_interval.start(0, 0.25)

    def _applyPrimeL(self) :
        super()._applyPrimeL()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.leftFace, self.rotation_cube)
        self.x_axis_cw_rot_interval.start(0, 0.25)

    def _applyF(self) :
        super()._applyF()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.frontFace, self.rotation_cube)
        self.z_axis_ccw_rot_interval.start(0, 0.25)

    def _applyPrimeF(self) :
        super()._applyPrimeF()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.frontFace, self.rotation_cube)
        self.z_axis_cw_rot_interval.start(0, 0.25)

    def _applyB(self) :
        super()._applyB()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.backFace, self.rotation_cube)
        self.z_axis_cw_rot_interval.start(0, 0.25)

    def _applyPrimeB(self) :
        super()._applyPrimeB()

        self._reparentAll(self.static_cube)
        self.rotation_cube.setHpr(0, 0, 0)
        self._reparentFace(self.backFace, self.rotation_cube)
        self.z_axis_ccw_rot_interval.start(0, 0.25)

    def applyMove(self, move) :
        match move:
            case Moves.F :
                self._applyF()
            case Moves.B :
                self._applyB()
            case Moves.U :
                self._applyU()
            case Moves.D :
                self._applyD()
            case Moves.R :
                self._applyR()
            case Moves.L :
                self._applyL()
            case Moves.PF :
                self._applyPrimeF()
            case Moves.PB :
                self._applyPrimeB()
            case Moves.PU :
                self._applyPrimeU()
            case Moves.PD :
                self._applyPrimeD()
            case Moves.PR :
                self._applyPrimeR()
            case Moves.PL :
                self._applyPrimeL()
            case _ :
                raise ValueError

    def _reparentCubie(self, cubie, parent):
        cubieHpr = cubie.getHpr(self.viewer3D.scene)
        cubie.reparentTo(parent)
        cubie.setHpr(self.viewer3D.scene, cubieHpr)

    def _reparentFace(self, face, parent):
        for line in face:
            for cubie in line:
                self._reparentCubie(cubie, parent)

    def _reparentAll(self, parent):
        self._reparentFace(self.downFace, parent)
        self._reparentFace(self.upFace, parent)
        self._reparentFace(self.frontFace, parent)
        self._reparentFace(self.backFace, parent)
        self._reparentFace(self.rightFace, parent)
        self._reparentFace(self.leftFace, parent)