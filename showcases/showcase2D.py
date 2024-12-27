#! /usr/bin/python

from cubeModel.TextRubikState import TextRubikState

def showcase2D(mix, solution):
    cube = TextRubikState()

    for move in mix:
        cube.applyMove(move)

    print("Initial state :")

    cube.print()

    for move in solution:
        cube.applyMove(move)

    print("Final state :")

    cube.print()