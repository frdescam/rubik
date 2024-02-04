import sys

from rubikState import RubikState, Moves

# check input
# transform enumeration

def getMix():
    while 1:
        print("How would you like to mix our rubicube?")
        try:
            mix = input()
            break
        except EOFError:
            sys.exit('EOF error')
        except:
            sys.exit('Input error')
    
    mixList = mix.split()

    moves = []

    for move in mixList:
        if (move == "F"):
            moves.append(Moves.F)
        elif (move == "R"):
            moves.append(Moves.R)
        elif (move == "U"):
            moves.append(Moves.U)
        elif (move == "B"):
            moves.append(Moves.B)
        elif (move == "L"):
            moves.append(Moves.L)
        elif (move == "D"):
            moves.append(Moves.D)

        elif (move == "F'"):
            moves.append(Moves.PF)
        elif (move == "P'"):
            moves.append(Moves.PR)
        elif (move == "P'"):
            moves.append(Moves.PU)
        elif (move == "P'"):
            moves.append(Moves.PB)
        elif (move == "P'"):
            moves.append(Moves.PL)
        elif (move == "P'"):
            moves.append(Moves.PD)

        elif (move == "F2"):
            moves.append(Moves.TWOF)
        elif (move == "R2"):
            moves.append(Moves.TWOR)
        elif (move == "U2"):
            moves.append(Moves.TWOU)
        elif (move == "B2"):
            moves.append(Moves.TWOB)
        elif (move == "L2"):
            moves.append(Moves.TWOL)
        elif (move == "D2"):
            moves.append(Moves.TWOD)

        else:
            sys.exit('Error in mix sequence notation, please go to http://www.francocube.com/notation.php to check your input')
            
    return (moves)

def main():
    getMix()

if __name__ == "__main__":
    main()
