from tinydb import TinyDB, Query
from typing import Dict, Any, List


class Player:
    """
        Model of the Player
        A player have a name (first and last)
        A date of birth,
        a national ID,
        a score,
        and a list of the players allready play against
    """
    def __init__(
        self, last_name: str, first_name: str, date_of_birth: str,
        national_id: str
    ):
        self.last_name = last_name
        self.first_name = first_name
        self.full_name = f"{last_name} {first_name}"
        self.date_of_birth = date_of_birth
        self.national_id = national_id
        self.score: float = 0.0
        self.player_allready_played: list = []
        self.tournament_score = 0.0

        self.player_db = TinyDB("database/players.json")

    # def update(self, score: float) -> None:
    #     # Update the score of the player
    #     self.score += score

    def save_player_db(self, player_informations: dict) -> None:
        players_db = self.player_db
        self.p_id = players_db.insert(player_informations)
        players_db.update({"id": self.p_id}, doc_ids=[self.p_id])

    @staticmethod
    def load_player_db() -> list:
        # Load the player in the database (json)
        players_db = TinyDB("database/players.json")
        players_db.all()
        players = []
        for item in players_db:
            players.append(item)

        return players

    @staticmethod
    def national_id_is_valid(national_id: str) -> bool:
        players_db = TinyDB("database/players.json")
        players_db.all()
        for player in players_db:
            if player["national_id"] == national_id:
                print("Player already exist")
                return False
        return True

    @classmethod
    def dict_to_model(cls, player: dict) -> "Player":
        # return a Player model based of the dictionnary
        player_model = cls(
            player["first_name"],
            player["last_name"],
            player["date_of_birth"],
            player["national_id"]
        )
        if "score" in player:
            player_model.score = player["score"]

        if "player_allready_played" in player:
            player_model.player_allready_played = (
                player["player_allready_played"]
            )
        player_model.tournament_score = player["tournament_score"]
        return player_model

    def model_to_dict(self, player: "Player") -> dict:
        # Return a dictionnary based of the model
        player_model: dict = {
            "first_name": player.first_name,
            "last_name": player.last_name,
            "date_of_birth": player.date_of_birth,
            "national_id": player.national_id,
            "score": player.score,
            "player_allready_played": player.player_allready_played,
            "tournament_score": player.tournament_score,
        }

        return player_model

    def to_dictionary(self) -> Dict[str, Any]:
        dictionary: Dict[str, Any] = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "chess_national_id": self.national_id,
            "score": self.score,
        }
        if self.player_allready_played:
            dictionary["player_allready_played"] = (
                self.players_to_dict(self.player_allready_played)
            )
        if self.tournament_score:
            dictionary["tournament_score"] = self.tournament_score
        return dictionary

    @classmethod
    def players_to_dict(cls, players: List["Player"]) -> List[Dict[str, Any]]:
        # Return a list of dictionnary of the players
        players_list = []
        for player in players:
            dictionary = {
                "first_name": player.first_name,
                "last_name": player.last_name,
                "date_of_birth": player.date_of_birth,
                "chess_national_id": player.national_id,
                "score": player.score,
                "tournament_score": player.tournament_score,
            }
            players_list.append(dictionary)
        return players_list

    def update_player(self, player, player_informations):
        # Update the database by the player informations
        players_db = self.player_db
        Player = Query()
        players_db.update(player_informations,
                          Player.national_id == player["national_id"])

    @staticmethod
    def reset_list_played():
        # Load the player in the database (json)
        players_db = TinyDB("database/players.json")
        players_db.all()
        for player in players_db:
            player["player_allready_played"] = []
            player["tournament_score"] = 0.0
            players_db.update(player, doc_ids=[player.doc_id])
