################################# 
###### Simple markov chains #####
#################################

import numpy as numpy
import random as random

states = ["c", "t", "a", "g"]

transition_name = [
#to    c     t     a     g  from:
    ["cc", "ct", "ca", "cg"], #c
    ["tc", "tt", "ta", "tg"], #t
    ["ac", "at", "aa", "ag"], #a
    ["gc", "gt", "ga", "gg"]  #g
                   ]

transition_matrix = [
#to    c     t     a     g  from:
    [0.25, 0.25, 0.25, 0.25], #c
    [0.25, 0.25, 0.25, 0.25], #t
    [0.25, 0.25, 0.25, 0.25], #a
    [0.25, 0.25, 0.25, 0.25]  #g
                   ]

# Check that transition matrix rows sum up to 1
for row in range(0, len(transition_matrix)):
    totalprob = sum(transition_matrix[row])
    if totalprob != 1:
        print(f"Row {row + 1} in the transition matrix sums up to {totalprob} instead of 1:")
        print(transition_matrix[row])

def forecast(Gen):

    # Initialisations
    base_now = "c"
    print("The starting base is: " + base_now)
    i = 0
    prob = 1

    # Keep track of what is going on over generations
    GenTrack = [base_now]

    # Off we go with our Markov chain
    while i != Gen:
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        if base_now == "c":                   
            change = numpy.random.choice(
                transition_name[0],          # pick one out of ['cc', 'ct', 'ca', 'cg']
                replace = True,
                p = transition_matrix[0]     # first row of matrix describes changes from c
                )
            # if the choice is to stay the same
            if change == "cc":
                prob = prob * 0.25
                GenTrack.append("c")
                pass            
            # if the choice is to change
            elif change == "ct":
                prob = prob * 0.25
                base_now = "t"
                GenTrack.append("t")
            elif change == "ca":
                prob = prob * 0.25
                base_now = "a"
                GenTrack.append("a")
            else:
                prob = prob * 0.25
                base_now = "g"
                GenTrack.append("g")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        elif base_now == "t":                   
            change = numpy.random.choice(
                transition_name[1],          # pick one out of ['tc', 'tt', 'ta', 'tg']
                replace = True,
                p = transition_matrix[1]     # second row of matrix describes changes from t
                )
            # if the choice is to stay the same
            if change == "tt":
                prob = prob * 0.25
                GenTrack.append("t")
                pass            
            # if the choice is to change
            elif change == "tc":
                prob = prob * 0.25
                base_now = "c"
                GenTrack.append("c")
            elif change == "ta":
                prob = prob * 0.25
                base_now = "a"
                GenTrack.append("a")
            else:
                prob = prob * 0.25
                base_now = "g"
                GenTrack.append("g")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        elif base_now == "a":                   
            change = numpy.random.choice(
                transition_name[2],          # pick one out of ['ac', 'at', 'aa', 'ag']
                replace = True,
                p = transition_matrix[2]     # third row of matrix describes changes from a
                )
            # if the choice is to stay the same
            if change == "aa":
                prob = prob * 0.25
                GenTrack.append("a")
                pass            
            # if the choice is to change
            elif change == "ac":
                prob = prob * 0.25
                base_now = "c"
                GenTrack.append("c")
            elif change == "at":
                prob = prob * 0.25
                base_now = "t"
                GenTrack.append("t")
            else:
                prob = prob * 0.25
                base_now = "g"
                GenTrack.append("g")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        elif base_now == "g":                   
            change = numpy.random.choice(
                transition_name[3],          # pick one out of ['gc', 'gt', 'ga', 'gg']
                replace = True,
                p = transition_matrix[3]     # fourth row of matrix describes changes from g
                )
            # if the choice is to stay the same
            if change == "gg":
                prob = prob * 0.25
                GenTrack.append("g")
                pass            
            # if the choice is to change
            elif change == "gc":
                prob = prob * 0.25
                base_now = "c"
                GenTrack.append("c")
            elif change == "gt":
                prob = prob * 0.25
                base_now = "t"
                GenTrack.append("t")
            else:
                prob = prob * 0.25
                base_now = "a"
                GenTrack.append("a")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        i = i + 1
        # This is the end of the markov chain, when i = Gen the while loop ends

    # This is the output of calling forecast(Gen)
    print(f"Base-states: {GenTrack}")
    print(f"End state after {Gen} unit of time: {base_now}")
    print(f"Probability of seeing base {base_now} after {Gen} unit of time is {prob}.")
