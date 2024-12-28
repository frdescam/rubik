#! /usr/bin/python

import numpy as np
from enum import Enum

class Moves(Enum) :
    F = "F"
    B = "B"
    U = "U"
    D = "D"
    R = "R"
    L = "L"

    PF = "PF"
    PB = "PB"
    PU = "PU"
    PD = "PD"
    PR = "PR"
    PL = "PL"

    TWOF = "TWOF"
    TWOB = "TWOB"
    TWOU = "TWOU"
    TWOD = "TWOD"
    TWOR = "TWOR"
    TWOL = "TWOL"

class RubikEngine :
    def __init__(self, downFace, leftFace, upFace, frontFace, backFace, rightFace) :
        
        self.downFace = downFace
        self.leftFace = leftFace
        self.upFace = upFace
        self.frontFace = frontFace
        self.backFace = backFace
        self.rightFace = rightFace

    def setState(self, other) :
        self.frontFace = other.frontFace
        self.backFace = other.backFace
        self.rightFace = other.rightFace
        self.leftFace = other.leftFace
        self.upFace = other.upFace
        self.downFace = other.downFace

    def getCopy(self) :
        copy = RubikState()
        copy.setState(self)
        return copy

    def __rotateFaceCW(self, oldFace) :
        newFace = np.array([[oldFace[2][0], oldFace[1][0], oldFace[0][0]], [oldFace[2][1], oldFace[1][1], oldFace[0][1]], [oldFace[2][2], oldFace[1][2], oldFace[0][2]]])
        return newFace

    def __rotateFaceCCW(self, oldFace) :
        newFace = np.array([[oldFace[0][2], oldFace[1][2], oldFace[2][2]], [oldFace[0][1], oldFace[1][1], oldFace[2][1]], [oldFace[0][0], oldFace[1][0], oldFace[2][0]]])
        return newFace

    def _applyU(self) :
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

    def _applyPrimeU(self) :
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

    def _applyTwoU(self) : 
        self._applyU()
        self._applyU()

    def _applyD(self) :
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

    def _applyPrimeD(self) :
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

    def _applyTwoD(self) : 
        self._applyD()
        self._applyD()

    def _applyR(self) :
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

    def _applyPrimeR(self) :
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

    def _applyTwoR(self) : 
        self._applyR()
        self._applyR()

    def _applyL(self) :
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

    def _applyPrimeL(self) :
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

    def _applyTwoL(self) : 
        self._applyL()
        self._applyL()

    def _applyF(self) :
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

    def _applyPrimeF(self) :
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

    def _applyTwoF(self) : 
        self._applyF()
        self._applyF()

    def _applyB(self) :
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


    def _applyPrimeB(self) :
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

    def _applyTwoB(self) : 
        self._applyB()
        self._applyB()

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
            case Moves.TWOF :
                self._applyTwoF()
            case Moves.TWOB :
                self._applyTwoB()
            case Moves.TWOU :
                self._applyTwoU()
            case Moves.TWOD :
                self._applyTwoD()
            case Moves.TWOR :
                self._applyTwoR()
            case Moves.TWOL :
                self._applyTwoL()

    def print(self):
        print()

        print("       " + self.upFace[0][0] + " " + self.upFace[0][1] + " " + self.upFace[0][2])
        print("       " + self.upFace[1][0] + " " + self.upFace[1][1] + " " + self.upFace[1][2])
        print("       " + self.upFace[2][0] + " " + self.upFace[2][1] + " " + self.upFace[2][2])

        print()

        print(self.leftFace[0][0] + " " + self.leftFace[0][1] + " " + self.leftFace[0][2] + "  " + self.frontFace[0][0] + " " + self.frontFace[0][1] + " " + self.frontFace[0][2] + "  " + self.rightFace[0][0] + " " + self.rightFace[0][1] + " " + self.rightFace[0][2] + "  " + self.backFace[0][0] + " " + self.backFace[0][1] + " " + self.backFace[0][2])
        print(self.leftFace[1][0] + " " + self.leftFace[1][1] + " " + self.leftFace[1][2] + "  " + self.frontFace[1][0] + " " + self.frontFace[1][1] + " " + self.frontFace[1][2] + "  " + self.rightFace[1][0] + " " + self.rightFace[1][1] + " " + self.rightFace[1][2] + "  " + self.backFace[1][0] + " " + self.backFace[1][1] + " " + self.backFace[1][2])
        print(self.leftFace[2][0] + " " + self.leftFace[2][1] + " " + self.leftFace[2][2] + "  " + self.frontFace[2][0] + " " + self.frontFace[2][1] + " " + self.frontFace[2][2] + "  " + self.rightFace[2][0] + " " + self.rightFace[2][1] + " " + self.rightFace[2][2] + "  " + self.backFace[2][0] + " " + self.backFace[2][1] + " " + self.backFace[2][2])

        print()

        print("       " + self.downFace[0][0] + " " + self.downFace[0][1] + " " + self.downFace[0][2])
        print("       " + self.downFace[1][0] + " " + self.downFace[1][1] + " " + self.downFace[1][2])
        print("       " + self.downFace[2][0] + " " + self.downFace[2][1] + " " + self.downFace[2][2])

        print()
        print()