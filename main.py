#!/usr/bin/python

from rubikState import RubikState, Moves
from thistlethwaiteAlgo import solver
from cubiesMoves import cubiesMove
from mixParsing import getMix, convert_for_3D
from showcase3D import showcase

import sys
import cProfile

def main():

    if (len(sys.argv) != 2):
        sys.exit('Wrong number of arguments')

    input = sys.argv[1]
    faceletsMix = getMix(input)
    cubiesMix = input.split()

    rubik = RubikState()

    for one_move in faceletsMix:
        rubik.applyMove(one_move)
    
    print("Initial state :")
    rubik.printCube()

    solution = solver(cubiesMix)

    check = getMix(solution)

    for move in check:
        rubik.applyMove(move)

    print('\nFinal state:')
    rubik.printCube()

    print("\nShowcase manual:")
    print("Use 'arrows' to change orientation")
    print("Press 'm' to mix cube")
    print("Press 's' to perform solution")
    print("Press 'r' to reset")

    showcase(convert_for_3D(cubiesMix), convert_for_3D(solution.split()))

if __name__ == "__main__":
    # cProfile.run('main()')
    main()
