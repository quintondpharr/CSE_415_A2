#!/usr/bin/python3
""" ItrBFS.py
Iterative Breadth-First Search of a problem space.
 Version 1.0, Oct 10th, 2023.
 Quinton Pharr, Univ. of Washington

This is just the exact same code as itrDFS, but with steps 4 and 5 combined
into one step, since BFS is just DFS with a queue instead of a stack. I.E.
the only difference is that we add to the end of the queue instead of the
beginning.
"""

import sys
import importlib


class ItrBFS:
    """
    Class that implements Iterative BFS for any problem space (provided in the required format)
    """

    def __init__(self, problem):
        """ Initializing the ItrBFS class."""
        self.Problem = importlib.import_module(problem)
        self.COUNT = None  # Number of nodes expanded
        self.MAX_OPEN_LENGTH = None  # Maximum length of the open list
        self.PATH = None  # Solution path
        self.PATH_LENGTH = None  # Length of the solution path
        self.BACKLINKS = None  # Predecessor links, used to recover the path
        print("\nWelcome to ItrBFS")

    def runBFS(self):
        """This is an encapsulation of some setup before running
        BFS, plus running it and then printing some stats."""
        initial_state = self.Problem.CREATE_INITIAL_STATE()
        print("Initial State:")
        print(initial_state)

        self.COUNT = 0
        self.MAX_OPEN_LENGTH = 0
        self.BACKLINKS = {}

        self.IterativeBFS(initial_state)
        print(f"Number of states expanded: {self.COUNT}")
        print(f"Maximum length of the open list: {self.MAX_OPEN_LENGTH}")

    def IterativeBFS(self, initial_state):
        """This is the actual algorithm"""
        # STEP 1. Put the start state on a list OPEN
        OPEN = [initial_state]
        CLOSED = []
        self.BACKLINKS[initial_state] = None

        # STEP 2. If OPEN is empty, output “DONE” and stop.
        while OPEN != []:
            report(OPEN, CLOSED, self.COUNT)
            if len(OPEN) > self.MAX_OPEN_LENGTH:
                self.MAX_OPEN_LENGTH = len(OPEN)

            # STEP 3. Select the first state on OPEN and call it S.
            #         Delete S from OPEN.
            #         Put S on CLOSED.
            #         If S is a goal state, output its description
            S = OPEN.pop(0)
            CLOSED.append(S)

            if self.Problem.GOAL_TEST(S):
                print(self.Problem.GOAL_MESSAGE_FUNCTION(S))
                self.PATH = [str(state) for state in self.backtrace(S)]
                self.PATH_LENGTH = len(self.PATH) - 1
                print(f"Length of solution path found: {self.PATH_LENGTH} edges")
                return
            self.COUNT += 1

            # STEP 4. Generate the list L of successors of S and delete
            #         from L those states already appearing on CLOSED.
            L = []
            for op in self.Problem.OPERATORS:
                if op.is_applicable(S):
                    new_state = op.apply(S)
                    if not (new_state in CLOSED or new_state in OPEN):
                        L.append(new_state)
                        self.BACKLINKS[new_state] = S

            OPEN.extend(L)  # Add L to the END of OPEN (instead of start like in dfs)

            print_state_list("OPEN", OPEN)

    # STEP 6. Go to Step 2.

    def backtrace(self, S):
        path = []
        while S:
            path.append(S)
            S = self.BACKLINKS[S]
        path.reverse()
        print("Solution path: ")
        for s in path:
            print(s)
        return path


def print_state_list(lst_name, lst):
    """
    Prints the states in lst with name lst_name
    """
    print(f"{lst_name} is now: ", end='')
    for s in lst[:-1]:
        print(str(s), end=', ')
    print(str(lst[-1]))


def report(opn, closed, count):
    """
    Reports the current statistics:
    Length of open list
    Length of closed list
    Number of states expanded
    """
    print(f"len(OPEN)= {len(opn)}", end='; ')
    print(f"len(CLOSED)= {len(closed)}", end='; ')
    print(f"COUNT = {count}")


if __name__ == '__main__':
    if sys.argv == [''] or len(sys.argv) < 2:
        Problem = "TowersOfHanoi"
    else:
        Problem = sys.argv[1]
    BFS = ItrBFS(Problem)
    BFS.runBFS()
