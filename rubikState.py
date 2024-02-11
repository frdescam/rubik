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

class RubikState :
    def __init__(self) :
        # Xface[x][y]
        self.frontFace = np.array([["\033[0;31m0\033[0m", "\033[0;31m1\033[0m", "\033[0;31m2\033[0m"], ["\033[0;31m3\033[0m", "\033[0;31m4\033[0m", "\033[0;31m5\033[0m"], ["\033[0;31m6\033[0m", "\033[0;31m7\033[0m", "\033[0;31m8\033[0m"]])
        self.backFace = np.array([["\033[0;32m0\033[0m", "\033[0;32m1\033[0m", "\033[0;32m2\033[0m"], ["\033[0;32m3\033[0m", "\033[0;32m4\033[0m", "\033[0;32m5\033[0m"], ["\033[0;32m6\033[0m", "\033[0;32m7\033[0m", "\033[0;32m8\033[0m"]])
        self.rightFace = np.array([["\033[0;35m0\033[0m", "\033[0;35m1\033[0m", "\033[0;35m2\033[0m"], ["\033[0;35m3\033[0m", "\033[0;35m4\033[0m", "\033[0;35m5\033[0m"], ["\033[0;35m6\033[0m", "\033[0;35m7\033[0m", "\033[0;35m8\033[0m"]])
        self.leftFace = np.array([["\033[0;37m0\033[0m", "\033[0;37m1\033[0m", "\033[0;37m2\033[0m"], ["\033[0;37m3\033[0m", "\033[0;37m4\033[0m", "\033[0;37m5\033[0m"], ["\033[0;37m6\033[0m", "\033[0;37m7\033[0m", "\033[0;37m8\033[0m"]])
        self.upFace = np.array([["\033[0;33m0\033[0m", "\033[0;33m1\033[0m", "\033[0;33m2\033[0m"], ["\033[0;33m3\033[0m", "\033[0;33m4\033[0m", "\033[0;33m5\033[0m"], ["\033[0;33m6\033[0m", "\033[0;33m7\033[0m", "\033[0;33m8\033[0m"]])
        self.downFace = np.array([["\033[0;34m0\033[0m", "\033[0;34m1\033[0m", "\033[0;34m2\033[0m"], ["\033[0;34m3\033[0m", "\033[0;34m4\033[0m", "\033[0;34m5\033[0m"], ["\033[0;34m6\033[0m", "\033[0;34m7\033[0m", "\033[0;34m8\033[0m"]])

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

    def applyU(self) :
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
            case Moves.F :
                self.applyF()
            case Moves.B :
                self.applyB()
            case Moves.U :
                self.applyU()
            case Moves.D :
                self.applyD()
            case Moves.R :
                self.applyR()
            case Moves.L :
                self.applyL()
            case Moves.PF :
                self.applyPrimeF()
            case Moves.PB :
                self.applyPrimeB()
            case Moves.PU :
                self.applyPrimeU()
            case Moves.PD :
                self.applyPrimeD()
            case Moves.PR :
                self.applyPrimeR()
            case Moves.PL :
                self.applyPrimeL()
            case Moves.TWOF :
                self.applyTwoF()
            case Moves.TWOB :
                self.applyTwoB()
            case Moves.TWOU :
                self.applyTwoU()
            case Moves.TWOD :
                self.applyTwoD()
            case Moves.TWOR :
                self.applyTwoR()
            case Moves.TWOL :
                self.applyTwoL()


    def printCube(self) :
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