#!/usr/bin/python

from colors import ANSI_YELLOW, ANSI_RESET
from Sequence import Sequence
from algo.thistlethwaiteAlgo import solver
from showcases.showcase2D import showcase2D
# from showcases.showcase3DOpenGL import showcase3DOpenGL
# from showcases.showcase3DBlender import showcase3DBlender

import sys
import random
import cProfile

ALL_MOVES = ["F","B","L","R","U","D","F'","B'","L'","R'","U'","D'","F2","B2","L2","R2","U2","D2"]

# PRINT

def printManual():
    print("\nShowcase manual:")
    print("Use 'arrows' to change orientation")
    print("Press 'm' to mix cube")
    print("Press 's' to perform solution")
    print("Press 'r' to reset")
    print("Press 'esc' to escape")

# TESTER

def testMix(mix):
    print("Mix: " + mix)
    solution = solver(mix.split())
    # check
    print("\n")

def launchTester():
    # 5 random spins
    print(ANSI_YELLOW + "\n5 RANDOM SPINS" + ANSI_RESET)
    mix=""
    for i in range(5):
        mix += ALL_MOVES[random.randint(0, 17)]
        mix += " "
    testMix(mix)

    # 20 random spins
    print(ANSI_YELLOW + "20 RANDOM SPINS" + ANSI_RESET)
    mix=""
    for i in range(20):
        mix += ALL_MOVES[random.randint(0, 17)]
        mix += " "
    testMix(mix)

    # 50 random spins
    print(ANSI_YELLOW + "50 RANDOM SPINS" + ANSI_RESET)
    mix=""
    for i in range(50):
        mix += ALL_MOVES[random.randint(0, 17)]
        mix += " "
    testMix(mix)

    # superflip

    print(ANSI_YELLOW + "SUPERFLIP" + ANSI_RESET)
    testMix("U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2")

    # distance 20 positions

    print(ANSI_YELLOW + "DISTANCE 20" + ANSI_RESET)
    testMix("B2 L B2 R' F' U' B' L D' F' L U L2 B2 L' D2 B2 D2 R2 B2")
    testMix("R U2 R D2 R2 B2 L' D' B' F U B' R' U2 L' D R2 F' U2 L2")
    testMix("D2 R2 F2 D2 F2 D2 R' F2 D' L2 R B L' F U R' B F2 R2 F'")
    testMix("D' F' U B2 R2 F R' U2 B' L D F R D2 R2 L2 D' R2 F2 D'")
    testMix("U2 R2 F2 D' U F2 U2 B U B' R U' F L B R' F L2 D' B")
    testMix("D B2 D' B2 R2 D' R2 U L R' D B' D R F' D2 R2 U' F' R")
    testMix("B D' L' F' L F B U' D2 F' R2 B' U F2 R' L U2 R2 F2 B2")
    testMix("U2 L' U2 F2 L' R D2 L2 B' D2 L F' R' U' L U2 F' D' R B")
    testMix("F' L B2 R U' B' L U2 D' F L' R2 U2 D2 B2 R2 D R2 L2 F2")
    testMix("U2 R2 D2 B U2 B' F D' B' R' D U2 B2 F2 R' D' B U' F' R2")

def main():

    if (len(sys.argv) != 2):
        sys.exit('Wrong number of arguments')

    input = sys.argv[1]

    if (input == "TEST"):
        launchTester()
    
    else:
        mix = Sequence(input)
    
        solution = solver(mix)

        showcase2D(mix, solution)
    
        # showcase3DOpenGL(mix, solution)
        # showcase3DBlender(mix, solution)

if __name__ == "__main__":
    # cProfile.run('main()')
    main()
