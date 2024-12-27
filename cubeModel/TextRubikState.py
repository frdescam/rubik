#! /usr/bin/python

from cubeModel.RubikState import RubikState
from thistlethwaiteAlgo import ANSI_BLUE, ANSI_BROWN, ANSI_CYAN, ANSI_GREEN, ANSI_PURPLE, ANSI_RED, ANSI_RESET, ANSI_WHITE, ANSI_YELLOW
import numpy as np

class TextRubikState(RubikState):
    def __init__(self):
        # red
        downFace = np.array([[ANSI_RED + "0" + ANSI_RESET, ANSI_RED + "1" + ANSI_RESET, ANSI_RED + "2" + ANSI_RESET], [ANSI_RED + "3" + ANSI_RESET, ANSI_RED + "4" + ANSI_RESET, ANSI_RED + "5" + ANSI_RESET], [ANSI_RED + "6" + ANSI_RESET, ANSI_RED + "7" + ANSI_RESET, ANSI_RED + "8" + ANSI_RESET]])
        # green
        leftFace = np.array([[ANSI_GREEN + "0" + ANSI_RESET, ANSI_GREEN + "1" + ANSI_RESET, ANSI_GREEN + "2" + ANSI_RESET], [ANSI_GREEN + "3" + ANSI_RESET, ANSI_GREEN + "4" + ANSI_RESET, ANSI_GREEN + "5" + ANSI_RESET], [ANSI_GREEN + "6" + ANSI_RESET, ANSI_GREEN + "7" + ANSI_RESET, ANSI_GREEN + "8" + ANSI_RESET]])
        # purple (=orange in 3D modelization and original rubik)
        upFace = np.array([[ANSI_PURPLE + "0" + ANSI_RESET, ANSI_PURPLE + "1" + ANSI_RESET, ANSI_PURPLE + "2" + ANSI_RESET], [ANSI_PURPLE + "3" + ANSI_RESET, ANSI_PURPLE + "4" + ANSI_RESET, ANSI_PURPLE + "5" + ANSI_RESET], [ANSI_PURPLE + "6" + ANSI_RESET, ANSI_PURPLE + "7" + ANSI_RESET, ANSI_PURPLE + "8" + ANSI_RESET]])
        # white
        frontFace = np.array([[ANSI_WHITE + "0" + ANSI_RESET, ANSI_WHITE + "1" + ANSI_RESET, ANSI_WHITE + "2" + ANSI_RESET], [ANSI_WHITE + "3" + ANSI_RESET, ANSI_WHITE + "4" + ANSI_RESET, ANSI_WHITE + "5" + ANSI_RESET], [ANSI_WHITE + "6" + ANSI_RESET, ANSI_WHITE + "7" + ANSI_RESET, ANSI_WHITE + "8" + ANSI_RESET]])
        # yellow
        backFace = np.array([[ANSI_YELLOW + "0" + ANSI_RESET, ANSI_YELLOW + "1" + ANSI_RESET, ANSI_YELLOW + "2" + ANSI_RESET], [ANSI_YELLOW + "3" + ANSI_RESET, ANSI_YELLOW + "4" + ANSI_RESET, ANSI_YELLOW + "5" + ANSI_RESET], [ANSI_YELLOW + "6" + ANSI_RESET, ANSI_YELLOW + "7" + ANSI_RESET, ANSI_YELLOW + "8" + ANSI_RESET]])
        # blue
        rightFace = np.array([[ANSI_BLUE + "0" + ANSI_RESET, ANSI_BLUE + "1" + ANSI_RESET, ANSI_BLUE + "2" + ANSI_RESET], [ANSI_BLUE + "3" + ANSI_RESET, ANSI_BLUE + "4" + ANSI_RESET, ANSI_BLUE + "5" + ANSI_RESET], [ANSI_BLUE + "6" + ANSI_RESET, ANSI_BLUE + "7" + ANSI_RESET, ANSI_BLUE + "8" + ANSI_RESET]])
        
        super().__init__(downFace, leftFace, upFace, frontFace, backFace, rightFace)