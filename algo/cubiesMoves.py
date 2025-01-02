from RubikMoves import Moves
import sys

## MOVES AT CEPO LEVEL
## ie CORNER - EDGE - POSITION - ORIENTATION

def moveU(eP, cP, eO, cO):
    eP[0], eP[1], eP[2], eP[3] = eP[1], eP[2], eP[3], eP[0]
    cP[0], cP[1], cP[2], cP[3] = cP[1], cP[2], cP[3], cP[0]
    eO[0], eO[1], eO[2], eO[3] = eO[1], eO[2], eO[3], eO[0]
    cO[0], cO[1], cO[2], cO[3] = cO[1], cO[2], cO[3], cO[0]
def moveD(eP, cP, eO, cO):
    eP[4], eP[5], eP[6], eP[7] = eP[7], eP[4], eP[5], eP[6]
    cP[4], cP[5], cP[6], cP[7] = cP[5], cP[6], cP[7], cP[4]
    eO[4], eO[5], eO[6], eO[7] = eO[7], eO[4], eO[5], eO[6]
    cO[4], cO[5], cO[6], cO[7] = cO[5], cO[6], cO[7], cO[4]
def moveF(eP, cP, eO, cO):
    eP[0], eP[4], eP[8], eP[9] = eP[9], eP[8], eP[0], eP[4]
    cP[0], cP[3], cP[4], cP[5] = cP[3], cP[5], cP[0], cP[4]
    eO[0], eO[4], eO[8], eO[9] = (eO[9] + 1) % 2, (eO[8] + 1) % 2, (eO[0] + 1) % 2, (eO[4] + 1) % 2
    cO[0], cO[3], cO[4], cO[5] = (cO[3] + 2) % 3, (cO[5] + 1) % 3, (cO[0] + 1) % 3, (cO[4] + 2) % 3
def moveB(eP, cP, eO, cO):
    eP[2], eP[6], eP[10], eP[11] = eP[10], eP[11], eP[6], eP[2]
    cP[1], cP[2], cP[6], cP[7] = cP[7], cP[1], cP[2], cP[6]
    eO[2], eO[6], eO[10], eO[11] = (eO[10] + 1) % 2, (eO[11] + 1) % 2, (eO[6] + 1) % 2, (eO[2] + 1) % 2
    cO[1], cO[2], cO[6], cO[7] = (cO[7] + 1) % 3, (cO[1] + 2) % 3, (cO[2] + 1) % 3, (cO[6] + 2) % 3
def moveL(eP, cP, eO, cO):
    eP[3], eP[7], eP[9], eP[11] = eP[11], eP[9], eP[3], eP[7]
    cP[2], cP[3], cP[5], cP[6] = cP[6], cP[2], cP[3], cP[5]
    eO[3], eO[7], eO[9], eO[11] = eO[11], eO[9], eO[3], eO[7]
    cO[2], cO[3], cO[5], cO[6] = (cO[6] + 1) % 3, (cO[2] + 2) % 3, (cO[3] + 1) % 3, (cO[5] + 2) % 3
def moveR(eP, cP, eO, cO):
    eP[1], eP[5], eP[8], eP[10] = eP[8], eP[10], eP[5], eP[1]
    cP[0], cP[1], cP[4], cP[7] = cP[4], cP[0], cP[7], cP[1]
    eO[1], eO[5], eO[8], eO[10] = eO[8], eO[10], eO[5], eO[1]
    cO[0], cO[1], cO[4], cO[7] = (cO[4] + 1) % 3, (cO[0] + 2) % 3, (cO[7] + 2) % 3, (cO[1] + 1) % 3

## ALL MOVES
def cubiesMove(one_move, eP, cP, eO, cO):
    match one_move:
        case "U":
            moveU(eP, cP, eO, cO)
        case "U'":
            moveU(eP, cP, eO, cO)
            moveU(eP, cP, eO, cO)
            moveU(eP, cP, eO, cO)
        case "U2":
            moveU(eP, cP, eO, cO)
            moveU(eP, cP, eO, cO)
        case "D":
            moveD(eP, cP, eO, cO)
        case "D'":
            moveD(eP, cP, eO, cO)
            moveD(eP, cP, eO, cO)
            moveD(eP, cP, eO, cO)
        case "D2":
            moveD(eP, cP, eO, cO)
            moveD(eP, cP, eO, cO)
        case "R":
            moveR(eP, cP, eO, cO)
        case "R'":
            moveR(eP, cP, eO, cO)
            moveR(eP, cP, eO, cO)
            moveR(eP, cP, eO, cO)
        case "R2":
            moveR(eP, cP, eO, cO)
            moveR(eP, cP, eO, cO)
        case "L":
            moveL(eP, cP, eO, cO)
        case "L'":
            moveL(eP, cP, eO, cO)
            moveL(eP, cP, eO, cO)
            moveL(eP, cP, eO, cO)
        case "L2":
            moveL(eP, cP, eO, cO)
            moveL(eP, cP, eO, cO)
        case "F":
            moveF(eP, cP, eO, cO)
        case "F'":
            moveF(eP, cP, eO, cO)
            moveF(eP, cP, eO, cO)
            moveF(eP, cP, eO, cO)
        case "F2":
            moveF(eP, cP, eO, cO)
            moveF(eP, cP, eO, cO)
        case "B":
            moveB(eP, cP, eO, cO)
        case "B'":
            moveB(eP, cP, eO, cO)
            moveB(eP, cP, eO, cO)
            moveB(eP, cP, eO, cO)
        case "B2":
            moveB(eP, cP, eO, cO)
            moveB(eP, cP, eO, cO)
        case _:
            sys.exit("bad input:" + str(one_move))
