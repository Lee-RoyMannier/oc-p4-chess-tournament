from Models.player import Player
from random import choice
from typing import Dict, Any


class Match:
    """
        Model of a Match:
        the match have 2 players against
        with a score beginning at 0
    """
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.white_player = choice([player1, player2])
        self.black_player = (
            player1 if self.white_player == player2 else player2
        )

    def to_dictionary(self) -> Dict[str, Any]:
        # Return a dictionnary of the model
        return {
            "player1": self.player1.model_to_dict(self.player1),
            "player2": self.player2.model_to_dict(self.player2),
            "white_player": self.white_player.model_to_dict(self.white_player),
            "black_player": self.black_player.model_to_dict(self.black_player),
        }

    @classmethod
    def load_from_dictionary(cls, data: Dict[str, Any]) -> 'Match':
        """
        Creates a match object from a dictionary.

        Args:
            data (dict): Dictionary containing the match data.

        Returns:
            Match: Match object created from the dictionary.
        """
        player1 = Player.dict_to_model(data["player1"])
        player2 = Player.dict_to_model(data["player2"])
        white_player = Player.dict_to_model(data["white_player"])
        black_player = Player.dict_to_model(data["black_player"])
        match = cls(player1, player2)
        match.white_player = white_player
        match.black_player = black_player

        return match
