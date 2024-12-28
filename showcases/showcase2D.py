#! /usr/bin/python

from rubikEngine.TextRubikEngine import TextRubikEngine

def showcase2D(mix, solution):
    cube = TextRubikEngine()

    for move in mix:
        cube.applyMove(move)

    print("Initial state :")

    cube.print()

    for move in solution:
        cube.applyMove(move)

    print("Final state :")

    cube.print()