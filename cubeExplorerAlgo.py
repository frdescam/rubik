# compute pruning table : which heuristics?
# add transition table --> index

# using IDA (Iterative Deepening Algorithm): depth first searching




# PHASE 1 : find a cube in G1
# G1 = <U, D, R2, L2, F2, B2>
# max = 12 moves




# PHASE 2 : solve whole cube
# max = 18 moves



# So: first solution should be 30 moves
# (but more research should lead to a 20 moves solutions)



# Note for optimization:
# any R, R2, or R' move should not be followed by R, R2, or R' because otherwise the search checks many positions several times. 
# since RL=LR we can also assume that R (or R2, R') never follows L (or L2, L'). 
# symmetry reduction
# One important subtlety is that phase 1 should end on a move that does not occur in the move set of phase 2 (i.e. F, F', B, B', R, R', L, or L'). 
# If you do not do this, then all the same move sequences will be searched again after the phase 1 length is increased.
# Do not use facelet level but cubie level (instead of 57 facelets, use 12 edges and 8 corners)
# Cubies can be in their home-positions, but with wrong orientations (corners twisted, edges flipped).

# Ressources :
# - http://kociemba.org/cube.htm
# - https://www.jaapsch.net/puzzles/compcube.htm
