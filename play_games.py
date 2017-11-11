# This script is for playing my own games.
from isolation import isolation
from sample_players import GreedyPlayer, RandomPlayer


def set_up_game():
    """ Set up a game and plays steps manually"""
    p1 = GreedyPlayer()
    p2 = RandomPlayer()

    # hash to reference
    players = {p1: 1, p2: 2}
    game = isolation.Board(p1, p2)

    moves = game.get_legal_moves(p1)



def play_random_greedy_game():
    """ a game for me to understand"""

    p1 = GreedyPlayer()
    p2 = RandomPlayer()

    #hash to reference
    players = {p1: 1, p2: 2}
    game = isolation.Board(p1,p2)
    winner, history, outcome = game.play()

    print('The game starts\n')

    player1_moves = [history[i] for i in range(0,len(history), 2)]
    player2_moves = [history[i] for i in range(1,len(history), 2)]
    max_moves = max([len(player1_moves),len(player2_moves)])

    for i in range(max_moves):
        if i ==0:
            p1_current = player1_moves[0]
            p2_current = player2_moves[0]

            print('Player 1 starts at space (%i,%i).'%(p1_current[0], p1_current[1]))
            print('Player 1 starts at space (%i,%i).' %(p2_current[0], p2_current[1]))
        else:
            if i<=len(player1_moves)-1:
                p1_previous = p2_current
                p1_current = player1_moves[i]

                print('Player 1 moves from space (%i,%i) to space (%i,%i).' % (p1_previous[0], p1_previous[1],
                                                                               p1_current[0], p1_current[1]))
            if i<= len(player2_moves)-1:
                p2_previous = p2_current
                p1_current = player2_moves[i]

                print('Player 2 moves from space (%i,%i) to space (%i,%i).' % (p2_previous[0], p2_previous[1],
                                                                               p2_current[0], p2_current[1]))


    print('\nPlayer %i won because of %s.'%(players[winner], outcome))



if __name__=='__main__':

    play_random_greedy_game()








