#!/usr/bin/python

from rubikState import RubikState, Moves

class Node :
    def __init__(self, state = None, move = None) :
        self.state = state
        self.move = move
        self.children = []

    def addChild(self, state, move) :
        newNode = Node(state, move)
        self.children.append(newNode)
        return newNode

    def getChildren(self) :
        return self.children

    def getState(self) :
        return self.state

    def getMove(self) :
        return self.move

def computeStates(root, depth = 0) :
    if depth ==  2:
        return
    for move in list(Moves) :
        tmpState = root.getState().getCopy()
        tmpState.applyMove(move)
        newNode = root.addChild(tmpState.getCopy(), move)
        computeStates(newNode, depth + 1)

def printStates(root) :
    if not root.getChildren :
        return

    if root.getMove() == None :
        print ("move : " + str(root.getMove()))
        root.getState().printCube()

    for child in root.getChildren() :
        print ("move : " + str(child.getMove()))
        child.getState().printCube()
        printStates(child)

def main():
    root = Node(RubikState())

    computeStates(root)

    printStates(root)

if __name__ == "__main__":
    main()
