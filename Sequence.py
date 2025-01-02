from RubikMoves import Moves

class Sequence():
    def __init__(self, stringSeq):
        self.stringSeq = stringSeq.split()
        self.moveSeq = self.__stringSeq2MoveSeq(stringSeq)
        self.limitedMoveSeq = self.__moveSeq2LimitedMoveSeq(self.moveSeq)

        self.stringSeqIndex = 0
        self.moveSeqIndex = 0
        self.limitedMoveSeqIndex = 0
        
        self.currentSeq = self.moveSeq

    def __stringSeq2MoveSeq(self, stringSeq):
        stringSeqList = stringSeq.split()

        move_mapping = {
        "F": Moves.F, "R": Moves.R, "U": Moves.U, "B": Moves.B, "L": Moves.L, "D": Moves.D,
        "F'": Moves.PF, "R'": Moves.PR, "U'": Moves.PU, "B'": Moves.PB, "L'": Moves.PL, "D'": Moves.PD,
        "F2": Moves.TWOF, "R2": Moves.TWOR, "U2": Moves.TWOU, "B2": Moves.TWOB, "L2": Moves.TWOL, "D2": Moves.TWOD
        }

        moveSeq = []

        for stringMove in stringSeqList:
            if stringMove not in move_mapping:
                sys.exit('Error in mix sequence notation, please go to http://www.francocube.com/notation.php to check your input')
            moveSeq.append(move_mapping[stringMove])

        return moveSeq

    def __moveSeq2LimitedMoveSeq(self, moveSeq):
        limitedMoveSeq = []
        for move in moveSeq:
            match move:
                case Moves.TWOF :
                    limitedMoveSeq.append(Moves.F)
                    limitedMoveSeq.append(Moves.F)
                case Moves.TWOB :
                    limitedMoveSeq.append(Moves.B)
                    limitedMoveSeq.append(Moves.B)
                case Moves.TWOU :
                    limitedMoveSeq.append(Moves.U)
                    limitedMoveSeq.append(Moves.U)
                case Moves.TWOD :
                    limitedMoveSeq.append(Moves.D)
                    limitedMoveSeq.append(Moves.D)
                case Moves.TWOR :
                    limitedMoveSeq.append(Moves.R)
                    limitedMoveSeq.append(Moves.R)
                case Moves.TWOL :
                    limitedMoveSeq.append(Moves.L)
                    limitedMoveSeq.append(Moves.L)
                case _ :
                    limitedMoveSeq.append(move)
        return(limitedMoveSeq)

    def asString(self):
        self.currentSeq = self.stringSeq
        return self

    def asMoves(self):
        self.currentSeq = self.moveSeq
        return self

    def asLimitedMoves(self):
        self.currentSeq = self.limitedMoveSeq
        return self

    def __iter__(self):
        return self

    def __moveSeq_next(self):
        if self.moveSeqIndex >= len(self.moveSeq):
            self.moveSeqIndex = 0
            raise StopIteration
        nextMove = self.moveSeq[self.moveSeqIndex]
        self.moveSeqIndex += 1
        return nextMove

    def __limitedMoveSeq_next(self):
        if self.limitedMoveSeqIndex >= len(self.limitedMoveSeq):
            self.limitedMoveSeqIndex = 0
            raise StopIteration
        nextMove = self.limitedMoveSeq[self.limitedMoveSeqIndex]
        self.limitedMoveSeqIndex += 1
        return nextMove

    def __stringSeq_next(self):
        if self.stringSeqIndex >= len(self.stringSeq):
            self.stringSeqIndex = 0
            raise StopIteration
        nextMove = self.stringSeq[self.stringSeqIndex]
        self.stringSeqIndex += 1
        return nextMove

    def __next__(self):
        if (self.currentSeq is self.moveSeq):
            return self.__moveSeq_next()
        elif (self.currentSeq is self.limitedMoveSeq):
            return self.__limitedMoveSeq_next()
        else :
            return self.__stringSeq_next()