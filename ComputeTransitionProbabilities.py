"""
 ComputeTransitionProbabilities.py

 Python function template to compute the transition probability matrix.

 Dynamic Programming and Optimal Control
 Fall 2024
 Programming Exercise

 Contact: Antonio Terpin aterpin@ethz.ch

 Authors: Maximilian Stralz, Philip Pawlowsky, Antonio Terpin

 --
 ETH Zurich
 Institute for Dynamic Systems and Control
 --
"""

import numpy as np
from utils import *

def compute_matrix_Piju(Constants):
    # pre allocate
    P = np.zeros((Constants.K, Constants.K,Constants.L)) 
    #initial position as an index
    map_start = state2idx(Constants.START_POS[0],Constants.START_POS[1],Constants)
    # set of static drone positions  (Use a set for quick lookups)
    static_drones = set(tuple(pos) for pos in Constants.DRONE_POS)  
    for i in range(Constants.N):# iterate over all x
        for j in range(Constants.M): # iterate over all y
            for i_swan in range(Constants.N): # iterate over all x for the swan 
                for j_swan in range(Constants.M): # iterate over all y for the swan
                    for l in range(Constants.L): # iterate over all input
                        # current state as index
                        map_i = state2idx(i,j,i_swan, j_swan, Constants) 
                        #----- no current applied ----------
                        #check where you'd end up WITHOUTH current
                        no_current_i, no_current_j = compute_state_with_input(i,j,l, Constants)
                        #check where the drone ends up if it moves
                        moved_swan_x, moved_swan_y = (i_swan, j_swan) + drone_position_numpy(i_swan,j_swan,i,j)
                        #check if you end un inside the map
                        if 0 <= no_current_i < Constants.N and 0 <= no_current_j < Constants.M:
                            #get the state you'd end up WITHOUTH current as an index
                            #map_j = state2idx(no_current_i,no_current_j,i_swan, j_swan, Constants)
                            #chek for static collision
                            if not tuple([no_current_i, no_current_j]) in static_drones:
                                #if not hitted, check for swan collision

                                #if the swan is moving and is not going to hit the drone
                                if moved_swan_x != no_current_i and moved_swan_y != no_current_j:
                                    #if no problem arises, you go to the designated x with probability p_current
                                    P[map_i][state2idx(no_current_i,no_current_j,moved_swan_x, moved_swan_y, Constants)][l] = (1 - Constants.CURRENT_PROB[no_current_i][no_current_j]) * Constants.SWAN_PROB
                                #the swan is moving and hits the drone
                                else: 
                                    P[map_i][map_start][l] = (1 - Constants.CURRENT_PROB[no_current_i][no_current_j]) * Constants.SWAN_PROB
                                #if the swan is not moving and is not going to hit the drone
                                if i_swan != no_current_i and j_swan != no_current_j:
                                    P[map_i][state2idx(no_current_i,no_current_j,i_swan, j_swan, Constants)][l] = (1 - Constants.CURRENT_PROB[no_current_i][no_current_j]) * (1- Constants.SWAN_PROB)
                                #the swan is not moving and hits the drone
                                else:
                                    P[map_i][map_start][l] = (1 - Constants.CURRENT_PROB[no_current_i][no_current_j]) * (1- Constants.SWAN_PROB)
                            else:
                                #if no probelm arises: you go to the designated x with probability 1-p_current
                                P[map_i][map_start][l] = 1 - Constants.CURRENT_PROB[no_current_i][no_current_j]
                        else:
                            #if you are outside the map, you go home with probability 1-p_current
                            P[map_i][map_start][l] = 1 - Constants.CURRENT_PROB[no_current_i][no_current_j]
                            # TODO Il cigno deve respawnare ???
                        # ––––– apply current –-------
                        #check wherer you'd end up WITH current
                        current_i, current_j = compute_state_plus_currents(no_current_i,no_current_j, Constants)
                        # Genera la linea tra i punti di partenza e arrivo senza corrente
                        path = bresenham((i, j), (current_i, current_j))
                        #check if you end up outside the map
                        if 0 <= current_i < Constants.N and 0 <= current_j < Constants.M:
                            #check if collision with static drones
                            if not any(tuple(point) in static_drones for point in path):
                                #if the swan is moving and is not going to hit the drone
                                if all(point != (moved_swan_x, moved_swan_y) for point in path):
                                    #if no problem arises, you go to the designated x with probability p_current
                                    P[map_i][state2idx(current_i,current_j,moved_swan_x, moved_swan_y, Constants)][l] = (Constants.CURRENT_PROB[no_current_i][no_current_j]) * Constants.SWAN_PROB
                                #the swan is moving and hits the drone
                                else: 
                                    P[map_i][map_start][l] = (Constants.CURRENT_PROB[no_current_i][no_current_j]) * Constants.SWAN_PROB
                                #if the swan is not moving and is not going to hit the drone
                                if all(point != (i_swan, j_swan) for point in path):
                                    P[map_i][state2idx(current_i,current_j,i_swan, j_swan, Constants)][l] = (Constants.CURRENT_PROB[no_current_i][no_current_j]) * (1- Constants.SWAN_PROB)
                                #the swan is not moving and hits the drone
                                else:
                                    P[map_i][map_start][l] = (Constants.CURRENT_PROB[no_current_i][no_current_j]) * (1- Constants.SWAN_PROB)
                            else:
                                #if no, go j
                                P[map_i][map_start][l] = Constants.CURRENT_PROB[no_current_i][no_current_j]
                        # if you are outside the map you go home.
                        else:
                            P[map_i][map_start][l] = Constants.CURRENT_PROB[no_current_i][no_current_j]
                            # TODO Il cigno deve respawnare ???
    return P

def compute_transition_probabilities(Constants):
    """Computes the transition probability matrix P.

    It is of size (K,K,L) where:
        - K is the size of the state space;
        - L is the size of the input space; and
        - P[i,j,l] corresponds to the probability of transitioning
            from the state i to the state j when input l is applied.

    Args:
        Constants: The constants describing the problem instance.

    Returns:
        np.array: Transition probability matrix of shape (K,K,L).
    """
    P = compute_matrix_Piju(Constants)
    print()
    print("K ", Constants.K)
    print("L ", Constants.L)
    print("Result")
    print(P)
    # TODO fill the transition probability matrix P here

    return P
