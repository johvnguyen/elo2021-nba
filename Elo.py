import numpy as np
import pandas as pd
import Team

def winprob(t1, t2):
    """Calculate win probability of each t1 and t2 against each other"""

    prob1 = 1/(1 + (10 ** ((t2.elo - t1.elo)/400)))
    prob2 = 1/(1 + (10 ** ((t1.elo - t2.elo)/400)))
    
    return prob1, prob2

def update_elo(win, lose, wprob, lprob, date):
    """Update the elo rating of winnning and losing team"""

    # k is a hyperparameter
    k = 15

    welo =  win.elo + (k * (1 - wprob))
    lelo =  lose.elo + (k * (0 - lprob))

    win.update_elo(welo, date)
    lose.update_elo(lelo, date)

    return


