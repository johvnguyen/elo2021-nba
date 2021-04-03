import numpy as np
import pandas as pd

class Team:
    """Wrapper object for an NBA team"""

    def __init__(self, name, datesdict, init_elo = 1500):
        """Create a team with given name, and number of game days"""

        self.name = name
        self.elo = 1500
        self.datesdict = datesdict
        self.elo_hist = [np.nan for i in range(len(datesdict))]
        self.elo_change = [np.nan for i in range(len(datesdict))]

        self.elo_hist[0] = self.elo
        self.elo_change[0] = self.elo
    
    def update_elo(self, newelo, date):
        """Update a team's elo rating"""

        idx = self.datesdict[date]

        self.elo = newelo
        self.elo_hist[idx] = self.elo
        self.elo_change[idx] = self.elo
    
    def finalize(self):
        """Prepares the elo rating to be put in a plot"""

        old_elo = self.elo_hist[0]

        for i in range(len(self.elo_hist)):
            if np.isnan(self.elo_hist[i]):
                self.elo_hist[i] = old_elo
            else:
                old_elo = self.elo_hist[i]

    
    def print(self):
        """Function for debugging"""
        
        print(f'\nName: {self.name}')
        print(f'Elo: {self.elo}\n')

    
