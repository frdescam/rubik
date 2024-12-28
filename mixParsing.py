from rubikEngine.RubikEngine import Moves

import sys

def getMix(mix):
    
    mixList = mix.split()

    moves = []

    move_mapping = {
    "F": Moves.F, "R": Moves.R, "U": Moves.U, "B": Moves.B, "L": Moves.L, "D": Moves.D,
    "F'": Moves.PF, "R'": Moves.PR, "U'": Moves.PU, "B'": Moves.PB, "L'": Moves.PL, "D'": Moves.PD,
    "F2": Moves.TWOF, "R2": Moves.TWOR, "U2": Moves.TWOU, "B2": Moves.TWOB, "L2": Moves.TWOL, "D2": Moves.TWOD
    }

    for one_move in mixList:
        if one_move not in move_mapping:
            sys.exit('Error in mix sequence notation, please go to http://www.francocube.com/notation.php to check your input')
        moves.append(move_mapping[one_move])

    return moves

def convert_for_3D(mix):
    result = []
    for m in mix:
        if len(m) == 2 and m[1] == '2':
            result.append(m[0])
            result.append(m[0])
        else:
            result.append(m)
    return(result)
