from rubikState import RubikState, Moves
from thistlethwaiteAlgo import solver
from cubiesMoves import cubiesMove
from mixParsing import getMix

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

if __name__ == "__main__":
    cProfile.run('main()')
