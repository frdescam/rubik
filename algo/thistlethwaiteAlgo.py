from algo.cubiesMoves import cubiesMove
from collections import deque
from colors import ANSI_GREEN, ANSI_RED, ANSI_RESET
from Sequence import Sequence

import sys
import time

## CORNER - EDGE - POSITION - ORIENTATION

GOAL_EP = [i for i in range(0, 12)]    # edgePosition        (0-11)   (UF UR UB UL DF DR DB DL FR FL BR BL)	   {0, ..., 11}
GOAL_CP = [i for i in range(12, 20)]   # cornerPosition      (12-19)  (UFR URB UBL ULF DRF DFL DLB DBR)		   {0, ..., 7}
GOAL_EO = [0] * 12                     # edgeOrientation     (0-1)    (UF UR UB UL DF DR DB DL FR FL BR BL)     0 = good, 1 = bad
GOAL_CO = [0] * 8                      # cornerOrientation   (0-2)    (UFR URB UBL ULF DRF DFL DLB DBR)         0 = good, 1 = twisted clockwise, 2 = twisted anti-clockwise

CUBE_EP = GOAL_EP[:]
CUBE_CP = GOAL_CP[:]
CUBE_EO = GOAL_EO[:]
CUBE_CO = GOAL_CO[:]

## BIDIRECTIONALITY

FORWARD = 0
BACKWARD = 1

## THISTHLEWAITE PHASES

PHASE_MOVES =   [["F","B","L","R","U","D","F'","B'","L'","R'","U'","D'","F2","B2","L2","R2","U2","D2"], # G0 -> G1 : all moves allowed
                ["L","R","U","D","L'","R'","U'","D'","F2","B2","L2","R2","U2","D2"], # G1 -> G2 : 1/4 turns Front and Back forbidden
                ["U","D","U'","D'","F2","B2","L2","R2","U2","D2"], # G2 -> G3 : 1/4 turns allowed only for Up and Down
                ["F2","B2","L2","R2","U2","D2"]] # G3 -> G4 : no 1/4 turns at all

## KOCIEMBA PHASES --> not possible because "pruning tables" (ie number of nodes to explore) are too huge
# PHASE_MOVES =   [["F","B","L","R","U","D","F'","B'","L'","R'","U'","D'","F2","B2","L2","R2","U2","D2"], # G0 -> G1 : all moves
#                 ["U","D","R2","L2","F2","B2"]] # G1 -> G2

## HASHING FUNCTION

def get_id(eP, cP, eO, cO, phase):
    if phase == 0:
        return tuple(eO[:]) # edge orientations only
    elif phase == 1:
        result = [1 if x > 7 and x < 12 else 0 for x in eP]
        result.extend(cO[:])
        return tuple(result) # edges positions from 8-11 + corners orientations
    elif phase == 2:
        result = cP[:]
        result.append(1 if eP[0] in {0, 2, 4, 6} else 0)
        result.append(1 if eP[2] in {0, 2, 4, 6} else 0)
        result.append(1 if eP[4] in {0, 2, 4, 6} else 0)
        result.append(1 if eP[6] in {0, 2, 4, 6} else 0)
        result.extend([1 if x in {1, 3, 5, 7} else 0 for x in eP[0:8]])
        result.extend([1 if x in {8, 11} else 0 for x in eP[8:12]])
        result.extend([1 if x in {9, 10} else 0 for x in eP[8:10]])
        return tuple(result) # corners good position + edges on M or S slices + edges E slice good placement or half turned
    else:
        result = eP[:] + cP[:] + eO[:] + cO[:]
        return tuple(result) # full state

# KOCIEMBA TESTS

# def get_id(eP, cP, eO, cO, phase):
#     if phase == 0:
#         result = eO[:] + cO[:] + eP[8:12]
#         return tuple(result)
#     else:
#         result = eP[:] + cP[:] + eO[:] + cO[:]
#     return tuple(result) # full state

# UTILS

def inverse_move(move):
    if len(move) == 2 and move[1] == '2':
        return move
    return move[0] if len(move) == 2 else move + "'"


def useless_move(first, second):
    opposite_moves = {('R', 'L'), ('U', 'D'), ('F', 'B')}  # because for example RL = LR
    if first == second or (first, second) in opposite_moves: # also for exemple U + U = U2 etc
        return True
    return False

# BIDIRECTIONAL BREADTH-FIRST SEARCH ALGORITHM

def bidir_bfs(phase, start_id, goal_id):
    nodes_dict = { start_id:[FORWARD, "Z", None, CUBE_EP, CUBE_CP, CUBE_EO, CUBE_CO], goal_id:[BACKWARD, "Z", None, GOAL_EP, GOAL_CP, GOAL_EO, GOAL_CO]} # nodes_dict[id] = [direction, move, parent, state]
    queue = deque([nodes_dict[start_id], nodes_dict[goal_id]]) # queue of nodes to explore (first in first out)

    while queue: # stops if queue empty and no solution found
        current_node = queue.popleft()
        for move in PHASE_MOVES[phase]:
            if (useless_move(move[0], current_node[1][0])): # check the utility of move compared to last move
                continue
            new_ep = current_node[3][:]
            new_cp = current_node[4][:]
            new_eo = current_node[5][:]
            new_co = current_node[6][:]
            cubiesMove(move, new_ep, new_cp, new_eo, new_co)
            new_id = get_id(new_ep, new_cp, new_eo, new_co, phase)
            new_node = nodes_dict.get(new_id)
            if new_node != None and new_node[0] != current_node[0]: # solution found
                if current_node[0] == BACKWARD: # swap current and new nodes
                    current_node, new_node = new_node, current_node
                    move = inverse_move(move)
                moves = [move]
                while list(nodes_dict.keys())[list(nodes_dict.values()).index(current_node)] != start_id: # from current node to beginning state
                    moves.insert(0, current_node[1])
                    current_node = current_node[2]
                while list(nodes_dict.keys())[list(nodes_dict.values()).index(new_node)] != goal_id: # from current node to goal state
                    moves.append(inverse_move(new_node[1])) # going backward so need to inverse all moves
                    new_node = new_node[2]
                return moves
            elif new_node is None: # create new node, add it to queue and continue searching 
                nodes_dict[new_id] = [current_node[0], move, current_node, new_ep, new_cp, new_eo, new_co]
                queue.append(nodes_dict[new_id])
    return None

# CHECK

def checkSolution():
    if GOAL_EP == CUBE_EP and GOAL_CP == CUBE_CP and GOAL_EO == CUBE_EO and GOAL_CO == CUBE_CO:
        return True
    return False

def solver(mix):
    for one_move in mix.asString():
        cubiesMove(one_move, CUBE_EP, CUBE_CP, CUBE_EO, CUBE_CO)
    start_time = time.time()
    wc = 0
    moves_log = ""
    for phase in range(4):
        start_id = get_id(CUBE_EP, CUBE_CP, CUBE_EO, CUBE_CO, phase)
        goal_id = get_id(GOAL_EP, GOAL_CP, GOAL_EO, GOAL_CO, phase)
        if start_id == goal_id:
            continue
        moves = bidir_bfs(phase, start_id, goal_id)
        tmp = ""
        for m in moves:
            cubiesMove(m, CUBE_EP, CUBE_CP, CUBE_EO, CUBE_CO)
            wc += 1
            tmp += m + ' '
        moves_log += tmp
    end_time = time.time()
    print('Solution: ' + moves_log)
    print('Duration: {:.2f} seconds'.format(end_time - start_time))
    print('Total number of moves: ' + str(wc))
    if (checkSolution()):
        print('Solved? ' + ANSI_GREEN + "OK" + ANSI_RESET )
    else:
        print('Solved? ' + ANSI_RED + "KO" + ANSI_RESET)
    return(Sequence(moves_log))
