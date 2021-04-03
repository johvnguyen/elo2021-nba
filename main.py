import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import Team
import Elo

figdir = './figures'
datadir = './data'

# Load team list
tnames = pd.read_csv(f"{datadir}/teams.csv")
tnames = tnames['Franchise'].values
teamdict = {tnames[i] : i for i in range(len(tnames))}

# Load game data
games = pd.read_csv(f"{datadir}/games2021.csv")
dates = games['Date'].values
games = games[['Date', 'Visitor/Neutral', 'PTS', 'Home/Neutral', 'PTS.1']]
games.columns = ['Date', 'Visitor', 'VPTS', 'Home', 'HPTS']

# Want list of unqiue game days while preserving order
dates = list(dict.fromkeys(dates))
dates = np.insert(dates, 0, 'Init', axis = 0)
ndays = len(dates)
datesdict = {dates[i] : i for i in range(ndays)}

# Make team structures
teams = []
for name in tnames:
    newteam = Team.Team(name, datesdict)
    teams.append(newteam)

# Calculate Elo based on game results
for i in range(len(games)):
    curr_game = games.iloc[i]

    date = curr_game['Date']
    home_team = curr_game['Home']
    visit_team = curr_game['Visitor']

    hpts = int(curr_game['HPTS'])
    vpts = int(curr_game['VPTS'])

    hindex = teamdict[home_team]
    vindex = teamdict[visit_team]

    hteam = teams[hindex]
    vteam = teams[vindex]

    hprob, vprob = Elo.winprob(hteam, vteam)

    if hpts < vpts:
        Elo.update_elo(vteam, hteam, vprob, hprob, date)
    
    if vpts < hpts:
        Elo.update_elo(hteam, vteam, hprob, vprob, date)

# Prepare the elo rating data to be put into array
for team in teams:
    team.finalize()

# Set up divisions
atl = ['Brooklyn Nets', 'Philadelphia 76ers', 'New York Knicks', 'Boston Celtics', 'Toronto Raptors']
cen = ['Milwaukee Bucks', 'Indiana Pacers', 'Chicago Bulls', 'Cleveland Cavaliers', 'Detroit Pistons']
sea = ['Charlotte Hornets', 'Miami Heat', 'Atlanta Hawks', 'Washington Wizards', 'Orlando Magic']
nwe = ['Utah Jazz', 'Denver Nuggets', 'Portland Trail Blazers', 'Oklahoma City Thunder', 'Minnesota Timberwolves']
pac = ['Phoenix Suns', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Golden State Warriors', 'Sacramento Kings']
swe = ['Dallas Mavericks', 'San Antonio Spurs', 'Memphis Grizzlies', 'New Orleans Pelicans', 'Houston Rockets']
div_names = ['ATL', 'CEN', 'SEA', 'NWE', 'PAC', 'SWE']

divisions = [atl, cen, sea, nwe, pac, swe]

# Only have start and middle of month on x-axis
axdates = []
for date in dates:
    if ' 1 ' in date or ' 15 ' in date:
        axdates.append(date)
    else:
        axdates.append('')

# Plotting begins here
d = 0
for div in divisions:
    fig, ax = plt.subplots(figsize=(25, 12.5))

    for team in div:
        i = teamdict[team]
        
        ax.scatter(dates, teams[i].elo_change, label = team)
        ax.plot(dates, teams[i].elo_hist)
        
    ax.legend(bbox_to_anchor=(1,1))

    ax.set_xlabel('Dates')
    ax.set_xticks(axdates)

    ax.set_ylabel('Elo Rating')

    figname = f'{figdir}/elo_{div_names[d]}.png'
    fig.savefig(figname)

    d += 1


fig, ax = plt.subplots(figsize=(25, 12.5))
for team in tnames:
    i = teamdict[team]

    ax.scatter(dates, teams[i].elo_change, label = team)
    ax.plot(dates, teams[i].elo_hist)

ax.legend(bbox_to_anchor=(1,1))

ax.set_xlabel('Dates')
ax.set_xticks(axdates)

ax.set_ylabel('Elo Rating')

figname = f'{figdir}/nba_elo.png'
fig.savefig(figname)