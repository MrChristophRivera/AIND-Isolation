import numpy as np
import pandas as pd
from os import getcwd, listdir
from os.path import split, join
import sys
from tqdm import tqdm_notebook as pbar

# set the base path
base_path = split(getcwd())[0]
sys.path.append(base_path)

from tournament import *
from custom_builders import (exponent_score_builder,
                             improved_weighted_center_score_builder,
                             improved_weighted_score_builder)

NUM_MATCHES = 5  # number of matches against each opponent
TIME_LIMIT = 10  # number of milliseconds before timeout
Agent = namedtuple("Agent", ["player", "name"])

# Define a collection of agents to compete against the test agents
cpu_agents = [
    Agent(RandomPlayer(), "Random"),
    Agent(MinimaxPlayer(score_fn=open_move_score), "MM_Open"),
    Agent(MinimaxPlayer(score_fn=center_score), "MM_Center"),
    Agent(MinimaxPlayer(score_fn=improved_score), "MM_Improved"),
    Agent(AlphaBetaPlayer(score_fn=open_move_score), "AB_Open"),
    Agent(AlphaBetaPlayer(score_fn=center_score), "AB_Center"),
    Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
]


def play_game_set(test_agent, cpu_agent, win_records, time_limit):
    """plays a single game set between player_agent and cpu_agent"""

    for _ in range(2):
        games = [Board(test_agent.player, cpu_agent.player), Board(cpu_agent.player, test_agent.player)]

    # play a rando move for the first player
    move = random.choice(games[0].get_legal_moves())
    for game in games:
        game.apply_move(move)

    for game in games:
        winner, _, termination = game.play(time_limit=time_limit)
        if winner == test_agent.player:
            win_records[test_agent.name][cpu_agent.name] += 1


def create_win_records(test_agents, cpu_agents):
    """ creates a dict for the holding records"""
    return {agent.name: {agent.name: 0 for agent in cpu_agents} for agent in test_agents}


def play_matches(test_agents, cpu_agents, num_matches, time_limit=150):
    """Plays a series of matches between the test agents and cpu agent
    """
    win_records = create_win_records(test_agents, cpu_agents)

    for ta in pbar(test_agents):
        for ca in pbar(cpu_agents):
            for _ in pbar(range(num_matches)):
                play_game_set(ta, ca, win_records, time_limit)
    return pd.DataFrame(win_records).T


def random_improved_weighted_agents(n, min_w=0, max_w=10):
    """generates a list of random weighted agents"""
    ws = np.random.uniform(min_w, max_w, n)
    agents = [Agent(AlphaBetaPlayer(score_fn=improved_weighted_score_builder(w)),
                    "AB_WeightedImproved (w:%f)" % w) for w in ws]
    description = pd.DataFrame({'Weight': ws})
    description['Agent Type'] = 'Improved Weighted'
    description['Lambda'] = 1
    description['K'] = 1

    return agents, description


def random_improved_weighted_center_agents(n, min_w=0, max_w=10):
    """generates a list of random weighted agents"""
    ws = np.random.uniform(min_w, max_w, n)
    ls = np.random.uniform(0, 1, n)
    agents = [Agent(AlphaBetaPlayer(score_fn=improved_weighted_center_score_builder(ws[i], ls[i])),
                    "AB_WeightedCenter (w:%f,lamba:%f)" % (ws[i], ls[i])) for i in range(n)]

    description = pd.DataFrame({'Weight': ws, 'Lambda': ls})
    description['Agent Type'] = 'Improved Weighted Centered'
    description['K'] = 1

    return agents, description


def random_exponential_agents(n, min_k=1.1, max_k=3):
    """generates a list of random weighted agents"""
    ks = np.random.uniform(min_k, max_k, n, )

    agents = [Agent(AlphaBetaPlayer(score_fn=exponent_score_builder(k)),
                    "AB_Exp (k:%f)" % (k)) for k in ks]

    description = pd.DataFrame({'K': ks})
    description['Agent Type'] = 'Exponential'
    description['Weight'] = 1
    description['Lambda'] = 1

    return agents, description


def create_random_test_agent_list(n=10, seed=123):
    """Creates a random test agent list to play games
    Args:
        n(int): the number of agents per custom type
    Returns:
        test_agents(list): a list of the agents
        test_agent_description(dataframe): a data frame of the players
    """
    np.random.seed(seed)

    agents = [Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")]
    desc = [pd.DataFrame({'Agent Type': "AB_Improved", 'K': 1, 'Lambda': 1, 'Weight': 1}, index=[1])]

    for f in [random_improved_weighted_agents, random_improved_weighted_center_agents]:  # , random_exponential_agents]:


        a, d = f(n)
        agents.extend(a)
        desc.append(d)
    return agents, pd.concat(desc).reset_index(drop=True)


def main(n=10, seed=123):
    # Define a collection of agents to compete against the test agents
    cpu_agents = [
        Agent(RandomPlayer(), "Random"),
        Agent(MinimaxPlayer(score_fn=open_move_score), "MM_Open"),
        Agent(MinimaxPlayer(score_fn=center_score), "MM_Center"),
        Agent(MinimaxPlayer(score_fn=improved_score), "MM_Improved"),
        Agent(AlphaBetaPlayer(score_fn=open_move_score), "AB_Open"),
        Agent(AlphaBetaPlayer(score_fn=center_score), "AB_Center"),
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
    ]

    test_agents, descriptions = create_random_test_agent_list(n, seed)
    print('Total games per test agent is %d.' % (2 * len(cpu_agents) * 10))
    print('The total number of games that will be played is %d' % (2 * len(cpu_agents) * len(test_agents) * 10))

    win_record = play_matches(test_agents, cpu_agents, num_matches=10, time_limit=150)

    return win_record, descriptions