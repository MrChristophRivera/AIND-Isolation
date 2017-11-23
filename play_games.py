# This script is for playing my own games.
from isolation import isolation
import timeit
import itertools
import random
import warnings

from collections import namedtuple

from isolation import Board

from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score, GreedyPlayer)
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score,
                        custom_score_2, custom_score_3)



def print_history(players, winner, history, outcome):
    print('The game starts\n')

    player1_moves = [history[i] for i in range(0, len(history), 2)]
    player2_moves = [history[i] for i in range(1, len(history), 2)]
    max_moves = max([len(player1_moves), len(player2_moves)])


    '''
    for i in range(max_moves):
        if i == 0:
            p1_current = player1_moves[0]
            p2_current = player2_moves[0]

            print('Player 1 starts at space (%i,%i).' % (p1_current[0], p1_current[1]))
            print('Player 1 starts at space (%i,%i).' % (p2_current[0], p2_current[1]))
        else:
            if i <= len(player1_moves) - 1:
                p1_previous = p1_current
                p1_current = player1_moves[i]

                print('Player 1 moves from space (%i,%i) to space (%i,%i).' % (p1_previous[0], p1_previous[1],
                                                                               p1_current[0], p1_current[1]))
            if i <= len(player2_moves) - 1:
                p2_previous = p2_current
                p2_current = player2_moves[i]

                print('Player 2 moves from space (%i,%i) to space (%i,%i).' % (p2_previous[0], p2_previous[1],
                                                                               p2_current[0], p2_current[1]))

    print('\nPlayer %i won because of %s.' % (players[winner], outcome))
    
    '''


def set_up_game():
    """ Set up a game and plays steps manually"""
    p1 = GreedyPlayer()
    p2 = GreedyPlayer()

    # hash to reference
    players = {p1: 1, p2: 2}
    game = isolation.Board(p1, p2)

    game.apply_move((3, 3))
    game.apply_move((0, 5))
    print(game.to_string())
    print(open_move_score(game,p1))
    print(open_move_score(game,p2))



    game.play()

    print(game.get_legal_moves())

   # print(game.to_string())
    #winner, history, outcome = game.play()

    #print_history(players, winner, history, outcome)


def test_time(limit=1):
    """ This is to understand the timing aspects of the game. """

    time_limit = limit
    # time in milliseconds
    time_millis = lambda:  1000*timeit.default_timer() # gets the time in milliseconds

    # start the time
    move_start = time_millis()
    time_left = lambda: time_limit - (time_millis() - move_start)   #this just allows one to get the current
    #time cool

    while time_left()>0:
        print(move_start)

    print('done')


def play_greedy_minimax_game():
    """ a game for me to understand"""

    p2 = GreedyPlayer()
    p1 = MinimaxPlayer(score_fn=open_move_score, search_depth=2)
    # hash to reference


    players = {p1: 1, p2: 2}
    game = isolation.Board(p1, p2)
    game.apply_move((3, 3))
    game.apply_move((0, 5))
    winner, history, outcome = game.play()
    print(outcome)
    print(winner)
    #print_history(players, winner, history, outcome)

def play_greedy_minimax_game():
    """ a game for me to understand"""

    p2 = GreedyPlayer()
    p1 = MinimaxPlayer(score_fn=open_move_score, search_depth=2)
    # hash to reference

    players = {p1: 1, p2: 2}
    game = isolation.Board(p1, p2)
    game.apply_move((3, 3))
    game.apply_move((0, 5))
    winner, history, outcome = game.play()
    print(outcome)
    print(winner)
    #print_history(players, winner, history, outcome)



if __name__ == '__main__':
    play_greedy_minimax_game()
