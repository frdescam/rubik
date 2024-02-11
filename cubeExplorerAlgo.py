import time
from pruningTables import Tables

# IMPLEMENTATION OF KOCIEMBA ALGORITHM aka CUBE EXPLORER
# http://kociemba.org/cube.htm
# https://www.jaapsch.net/puzzles/compcube.htm 


class CubeExplorer:

    def __init__(self, facelets):
        self.pruningTables = Tables() # TO DO

    def solve(self, max_length=50, timeout=float("inf")): # timeout shall be set to 3 seconds, for now it's infinite to test algorithm capacity

        # prepare for phase 1
        self.max_length = max_length
        self.timeout = timeout
        self.phase_1_initialise(max_length)

        # do phase 1
        for depth in range(self.max_length):
            n = self.phase_1_search(0, depth)
            if n >= 0:
                # solution found
                return self.solution_to_string(n) # transform solution found in annotation mandatory in the subject (URFDLB)
            elif n == -2:
                # timeout
                return -2

        # no solution found
        return -1


## PHASE 1
    
    # max depth: should be up to 12
    # from G0 to G1 = <U, D, R2, L2, F2, B2>

    def phase_1_initialise(self, max_length):
        # axis: index of face being turned
        # power: number of clockwise quarter turns
        self.axis = [0] * max_length
        self.power = [0] * max_length

        # twist, flip and udslice: phase 1 coordinates after n moves
        self.twist = [0] * max_length
        self.flip = [0] * max_length
        self.udslice = [0] * max_length

        # corner, edge4, edge8: phase 2 coordinates after n moves
        self.corner = [0] * max_length
        self.edge4 = [0] * max_length
        self.edge8 = [0] * max_length

        # min dist 1: minimum number of moves required to reach phase 2 after n moves
        # min dist 2: minimum number of moves required to reach a solution after n moves
        # Note: Estimations come from pruning tables. 
        # Pruning tables DO NOT show the solution, yet are used to EXCLUDE branches in the search tree.
        self.min_dist_1 = [0] * max_length
        self.min_dist_2 = [0] * max_length

        # initialise the arrays from the input
        self.cubiecubes = self.facelets_to_cubiecubes() # transforms facelets into cubiecube 
        self.twist[0] = self.twist
        self.flip[0] = self.flip
        self.udslice[0] = self.udslice
        self.corner[0] = self.corner
        self.edge4[0] = self.edge4
        self.edge8[0] = self.edge8
        self.min_dist_1[0] = self.phase_1_cost(0)

    def phase_1_search(self, n, depth):
        # timeout
        if time.time() > self._timeout:
            return -2
        # if phase 1 finished, do phase 2
        elif self.min_dist_1[n] == 0:
            return self.phase_2_initialise(n)
        # phase 1 of Iterative Deepening Algorithm (IDA)
        elif self.min_dist_1[n] <= depth:
            for i in range(6):
                if n > 0 and self.axis[n - 1] in (i, i + 3):
                    # Note: don't turn the same face on consecutive moves
                    # also for opposite faces, e.g. U and D, UD = DU, so we can
                    # impose that the lower index happens first.
                    continue
                for j in range(1, 4):
                    self.axis[n] = i
                    self.power[n] = j
                    mv = 3 * i + j - 1

                    # update coordinates
                    self.twist[n + 1] = self.tables.twist_move[self.twist[n]][
                        mv
                    ]
                    self.flip[n + 1] = self.tables.flip_move[self.flip[n]][mv]
                    self.udslice[n + 1] = self.tables.udslice_move[
                        self.udslice[n]
                    ][mv]
                    self.min_dist_1[n + 1] = self.phase_1_cost(n + 1)

                    # start search from next node
                    m = self.phase_1_search(n + 1, depth - 1)
                    if m >= 0:
                        return m
                    # timeout
                    if m == -2:
                        return -2
        # no solution found at current depth 
        return -1

# Note: continue searching after the first solution is found. As was noted with Thistlethwaite's algorithm, 
# a different phase 1 solution may well have a better possible phase 2 solution. 
# After one solution is found, other phase 1 solutions are tried to see if these give a better phase 2 
# and hence a better overall solution.

# Note: Phase 1 should end on a move that does not occur in the move set of phase 2 
# (i.e. F, F', B, B', R, R', L, or L'). If you do not do this, then all the same move sequences 
# will be searched again after the phase 1 length is increased.


## PHASE 2

    # max depth: should be up to 18
    # from G1 to I

    def phase_2_initialise(self, n):
        # timeout
        if time.time() > self.timeout:
            return -2
        # initialise phase 2 search from the phase 1 solution
        cc = self.facelets_to_cubiecubes()
        for i in range(n):
            for j in range(self.power[i]):
                cc.move(self.axis[i])
        self.edge4[n] = cc.edge4
        self.edge8[n] = cc.edge8
        self.corner[n] = cc.corner
        self.min_dist_2[n] = self.phase_2_cost(n)
        # launch phase 2
        for depth in range(self.max_length - n):
            m = self.phase_2_search(n, depth)
            if m >= 0:
                return m
        # no solution found at this depth
        return -1

    def phase_2_search(self, n, depth):
        if self.min_dist_2[n] == 0:
            return n
        elif self.min_dist_2[n] <= depth:
            for i in range(6):
                if n > 0 and self.axis[n - 1] in (i, i + 3):
                    continue
                for j in range(1, 4):
                    if i in [1, 2, 4, 5] and j != 2:
                        # Note: in phase 2 we only allow half turns of the faces
                        # R, F, L, B
                        continue
                    self.axis[n] = i
                    self.power[n] = j
                    mv = 3 * i + j - 1

                    # update coordinates following the move mv
                    self.edge4[n + 1] = self.tables.edge4_move[self.edge4[n]][
                        mv
                    ]
                    self.edge8[n + 1] = self.tables.edge8_move[self.edge8[n]][
                        mv
                    ]
                    self.corner[n + 1] = self.tables.corner_move[
                        self.corner[n]
                    ][mv]
                    self.min_dist_2[n + 1] = self._phase_2_cost(n + 1)

                    # start search from new node
                    m = self.phase_2_search(n + 1, depth - 1)
                    if m >= 0:
                        return m
        # if no solution found at current depth, return -1
        return -1


# COMPUTE COSTS WITH PRUNING TABLES

    def phase_1_cost(self, n):
        return max(
            self.tables.udslice_twist_prune[self.udslice[n], self.twist[n]],
            self.tables.udslice_flip_prune[self.udslice[n], self.flip[n]],
        )

    def phase_2_cost(self, n):
        return max(
            self.tables.edge4_corner_prune[self.edge4[n], self.corner[n]],
            self.tables.edge4_edge8_prune[self.edge4[n], self.edge8[n]],
        )

# UTILS

    def solution_to_string(self, length):
    
    def facelets_to_cubiecubes():

