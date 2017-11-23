# This file builds custom scoring functions with import parameters to play in the tournament
import numpy as np


def exponent_score_builder(k=2):
    """ Constructs a scoring function that uses form sign(player_moves-opponent_moves)*(player_moves-opponent_moves)*k
    where k is an power greater than 0.
    Args:
        k(float): the exponent
    Returns:
        exponent_score(callable)
    """

    def exponent_score(game, player):
        """Calculate the heuristic value of a game state from the point of view
        of the given player.

        Note: this function should be called from within a Player instance as
        self.score()` -- you should not need to call this function directly.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to
            one of the player objects `game.__player_1__` or `game.__player_2__`.)
        exponent

        Returns
        -------
        float
            The heuristic value of the current game state to the specified player.
        """

        if game.is_loser(player):
            return float("-inf")

        if game.is_winner(player):
            return float("inf")

        own_moves = len(game.get_legal_moves(player))
        opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
        return float(own_moves - opp_moves) ** k * np.sign(own_moves - opp_moves)

    return exponent_score


def improved_weighted_score_builder(opp_weight):
    """ Constructs a scoring function that uses player_moves-opp_weight*opp_moves to control the aggressiveness of the
    player
        Args:
            opp_weight(float): the exponent
        Returns:
            improve_weighted_score(callable)
        """

    def improve_weighted_score(game, player):
        """Calculate the heuristic value of a game state from the point of view
        of the given player.

        This should be the best heuristic function for your project submission.

        Note: this function should be called from within a Player instance as
        `self.score()` -- you should not need to call this function directly.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to
            one of the player objects `game.__player_1__` or `game.__player_2__`.)

        Returns
        -------
        float
            The heuristic value of the current game state to the specified player.
        """
        if game.is_loser(player):
            return float("-inf")

        if game.is_winner(player):
            return float("inf")

        own_moves = len(game.get_legal_moves(player))
        opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
        return float(own_moves - opp_weight*opp_moves)

    return improve_weighted_score


def improved_weighted_center_score_builder(opp_weight, lambda_):
    """Constructs a scoring function of lambda_*player_move_delta + (1-lambda_)*distance from center
    Args:
        opp_weight(float): scalar that determines aggressiveness of player
        lambda_(float) mixing parameter between 0 to 1. 0 all center score, 1 all weighted player diff.
    Returns:
        callable
    """

    def improved_weighted_center_score_builder(game, player):
        """Calculate the heuristic value of a game state from the point of view
        of the given player.

        Note: this function should be called from within a Player instance as
        `self.score()` -- you should not need to call this function directly.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        player : object
            A player instance in the current game (i.e., an object corresponding to
            one of the player objects `game.__player_1__` or `game.__player_2__`.)

        opp_weight: float

        Returns
        -------
        float
            The heuristic value of the current game state to the specified player.
        """
        if game.is_loser(player):
            return float("-inf")

        if game.is_winner(player):
            return float("inf")

        own_moves = len(game.get_legal_moves(player))
        opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

        score_diff = (own_moves - opp_weight*opp_moves)

        w, h = game.width / 2., game.height / 2.
        y, x = game.get_player_location(player)

        dist_score = float((h - y) ** 2 + (w - x) ** 2)

        return lambda_*score_diff+(1-lambda_) * dist_score

    return improved_weighted_center_score_builder