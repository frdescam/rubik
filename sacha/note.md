Most useful resource to optimize algo: https://www.jaapsch.net/puzzles/compcube.htm

Notes on Kociemba :
- One important subtlety is that phase 1 should end on a move that does not occur in the move set of phase 2 (i.e. F, F', B, B', R, R', L, or L'). If you do not do this, then all the same move sequences will be searched again after the phase 1 length is increased.

TO DO:

[X] implement Kociemba algo --> too huge number of nodes to explore
[] create testeur + scramble
[] implement human style FMC challenge algo --> Roux / CFOP
[X] 3D representation

- scop + use arrows
- test parsing
- trimming function
- thistlewaite but continue searching after first solution found to compare other solutions
