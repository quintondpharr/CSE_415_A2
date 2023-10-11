'''Farmer_Fox.py
by Quinton Pharr
UWNetID: qpharr@uw.edu
Student number: 2264513

Assignment 2, in CSE 415, Autumn 2023.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in 
# the format shown.

#<METADATA>
SOLUTION_VERSION = "1.0"
PROBLEM_NAME = "Farmer, Fox, Chicken, and Grain"
PROBLEM_VERSION = "1.0"
PROBLEM_AUTHORS = ['Q. Pharr']
PROBLEM_CREATION_DATE = "10-OCT-2023"

PROBLEM_DESC=\
'''The <b>"Farmer, Fox, Chicken, and Grain"</b> problem is a classic puzzle
in which the player starts off with a farmer, a fox, a chicken, and a bag
of grain on the left bank of a river. The object is to execute a sequence
of legal moves that transfers them all to the right bank of the river.
The problem is that the boat can only carry the farmer and one other item
at a time. If the fox is left alone with the chicken, the fox will eat the
chicken. If the chicken is left alone with the grain, the chicken will eat
the grain.'''

#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>
F = 0  # array index to access farmer counts
f = 1  # same idea for fox
C = 2  # same idea for chicken
G = 3  # same idea for grain
LEFT = 0  # same idea for left side of river
RIGHT = 1  # etc.

class State():

    def __init__(self, d=None):
        if d == None:
            d = {'agents': [[1, 1, 1, 1], [0, 0, 0, 0]],
                 'boat': LEFT}
        self.d = d

    def __eq__(self, s2):
        for prop in ['agents', 'boat']:
            if self.d[prop] != s2.d[prop]: return False
        return True
    
    def __str__(self):
    # produces a textual description of a state
        p = self.d['agents']
        txt = "\n Farmer on left:" + str(p[LEFT][F]) + "\n"
        txt += " Fox on left:" + str(p[LEFT][f]) + "\n"
        txt += " Chicken on left:" + str(p[LEFT][C]) + "\n"
        txt += " Grain on left:" + str(p[LEFT][G]) + "\n"
        txt += "   Farmer on right:" + str(p[RIGHT][F]) + "\n"
        txt += "   Fox on right:" + str(p[RIGHT][f]) + "\n"
        txt += "   Chicken on right:" + str(p[RIGHT][C]) + "\n"
        txt += "   Grain on right:" + str(p[RIGHT][G]) + "\n"
        side = 'left'
        if self.d['boat'] == 1: side = 'right'
        txt += " boat is on the " + side + ".\n"
        return txt

    
    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State({})
        news.d['agents'] = [[self.d['agents'][side][A_or_a] for A_or_a in [F, f, C, G]] for side in [LEFT, RIGHT]]
        news.d['boat'] = self.d['boat']
        return news

    
    def can_move(self, Farmer, Fox, Chicken, Grain):
        '''Tests whether it's legal to move the boat and take 
        F Farmer, f Fox, C Chicken, and G Grain.'''
        side = self.d['boat']  # Where the boat is.
        p = self.d['agents']

        # Checks for moving Farmer alone or with only one item
        if Farmer + Fox + Chicken + Grain > 2: 
            return False

        # Check for fox and chicken left together
        if Fox == 0 and Chicken == 0 and p[side][f] == 1 and p[side][C] == 1:
            return False

        # Check for chicken and grain left together
        if Chicken == 0 and Grain == 0 and p[side][C] == 1 and p[side][G] == 1:
            return False

        return True

    
    def move(self, Farmer, Fox, Chicken, Grain):
        '''Assuming it's legal to make the move, this computes
        the new state resulting from moving the boat carrying
        Farmer, Fox, Chicken, and Grain.'''
        news = self.copy() # start with a deep copy.
        side = self.d['boat'] # where the boat is.
        p = news.d['agents'] # get the array of arrays of agents.
        p[side][F] = 0
        p[side][f] = 0 if Fox == 1 else p[side][f]
        p[side][C] = 0 if Chicken == 1 else p[side][C]
        p[side][G] = 0 if Grain == 1 else p[side][G]

        p[1-side][F] = 1
        p[1-side][f] = 1 if Fox == 1 else p[1-side][f]
        p[1-side][C] = 1 if Chicken == 1 else p[1-side][C]
        p[1-side][G] = 1 if Grain == 1 else p[1-side][G]
        news.d['boat'] = 1-side # Move the boat itself.
        return news

    
    def goal_test(s):
        '''if the farmer, fox, chicken, and grain are on the right side of the river,
        the goal is reached'''
        p = s.d['agents']
        return (p[F][RIGHT] == 1 and p[f][RIGHT] == 1 and p[C][RIGHT] == 1 and p[G][RIGHT] == 1)
    
    def goal_message(s):
        return '''Congratulations on successfully guiding the farmer, fox, chicken,
        and grain across the river!'''
    
    class Operator:
        def __init__(self, name, precond, state_transf):
            self.name = name
            self.precond = precond
            self.state_transf = state_transf

        def is_applicable(self, s):
            return self.precond(s)
        
        def apply(self, s):
            return self.state_transf(s)
#</COMMON_CODE>

#<INITIAL_STATE>
INITIAL_DICT = {'agents': [[1, 1, 1, 1], [0, 0, 0, 0]], 'boat': LEFT}
CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT)
#</INITIAL_STATE>

#<OPERATORS>
FfCG_combinations = [(1, 0, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1), (1, 1, 0, 0)]

OPERATORS = [State.Operator( 
    "Cross the river with farmer and " + ["", "a fox", "a chicken", "some grain"][Fox + 2*Chicken + 3*Grain],
    lambda s, Farmer1=Farmer, Fox1=Fox, Chicken1=Chicken, Grain1=Grain: s.can_move(Farmer1, Fox1, Chicken1, Grain1),
    lambda s, Farmer1=Farmer, Fox1=Fox, Chicken1=Chicken, Grain1=Grain: s.move(Farmer1, Fox1, Chicken1, Grain1))
    for (Farmer, Fox, Chicken, Grain) in FfCG_combinations]


#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: State.goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: State.goal_message(s)
#</GOAL_MESSAGE_FUNCTION>