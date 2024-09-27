from datetime import datetime
from Models.match import Match
from typing import List, Dict, Any
from prettytable import PrettyTable


class Round:
    """
        Model of a Round:
        a round have a name,
        a list of matches,
        a starting date and a finish date
    """
    def __init__(self, name: str):
        self.name = name
        self.matches: List[Match] = []
        self.start_datetime = str(datetime.now())
        self.end_datetime = None
        self.finished = False

    def adding_match(self, match: Match):
        self.matches.append(match)

    def is_finished(self) -> bool:
        return self.finished

    def set_finish_round(self) -> None:
        self.finished = True
        self.end_datetime = str(datetime.now())

    def to_dictionary(self) -> Dict[str, Any]:
        dictionary = {
            "name": self.name,
            "start_datetime": self.start_datetime,
            "finished": str(self.finished),
            "matches": [match.to_dictionary() for match in self.matches]
        }

        if self.end_datetime is not None:
            dictionary["end_datetime"] = self.end_datetime
        return dictionary

    @classmethod
    def load_from_dictionary(cls, data: Dict[str, Any]) -> 'Round':
        """
        Creates a round object from a dictionary.

        Args:
            data (dict): Dictionary containing the round data.

        Returns:
            Round: Round object created from the dictionary.
        """
        round = cls(data["name"])
        round.start_datetime = data["start_datetime"]
        if data["finished"] == "True":
            round.set_finish_round()
        for data_match in data["matches"]:
            match = Match.load_from_dictionary(data_match)
            round.adding_match(match)
        return round

    def present_match(self):
        # Attribute point
        # If the player win, the score is update by 1
        # If its a Draw, The two players's scores are updated by 0.5
        print(f"---- {self.name}: ---- \n")
        for match in self.matches:
            print("How win : Black or White or Draw or quit")
            self.display_final(match)
            winner = input("Enter your color : \n").lower()

            if winner == "black":
                # match.black_player.score += 1
                match.black_player.tournament_score += 1

            elif winner == "white":
                # match.white_player.score += 1
                match.white_player.tournament_score += 1
            elif winner == "draw":
                # match.black_player.score += 0.5
                # match.white_player.score += 0.5
                match.black_player.tournament_score += 0.5
                match.white_player.tournament_score += 0.5
            elif winner == "quit":
                exit()
            else:
                # match.black_player.score += 0.5
                # match.white_player.score += 0.5
                match.black_player.tournament_score += 0.5
                match.white_player.tournament_score += 0.5

            # if match.black_player.national_id == match.player1.national_id:
            #     match.player1.tournament_score = match.black_player.tournament_score
            #     match.player2.tournament_score = match.white_player.tournament_score
            # else:
            #     match.player2.tournament_score = match.black_player.tournament_score
            #     match.player1.tournament_score = match.white_player.tournament_score

    def display_final(self, match):
        # Display the actual match
        table = PrettyTable()
        table.field_names = ["white", "black"]

        table.add_row([
            match.white_player.full_name,
            match.black_player.full_name,
        ])
        print(table)

    def update_score(self, round):
        # Update the score of the 2 players
        for match in round.matches:
            pp1 = match.player1.model_to_dict(match.player1)
            pp2 = match.player2.model_to_dict(match.player2)
            p1 = match.white_player.model_to_dict(match.white_player)
            p2 = match.black_player.model_to_dict(match.black_player)
            # pp1["score"] = p1["score"]
            # pp2["score"] = p2["score"]
            # pp1["tournament_score"] += p1["tournament_score"]
            # pp2["tournament_score"] = p2["tournament_score"]
            pp1["score"] += pp1["tournament_score"]
            pp2["score"] += pp2["tournament_score"]

            print(pp1["tournament_score"])
            print(pp2["tournament_score"])
            print(p1["tournament_score"])
            print(p2["tournament_score"])
            match.player1.update_player(pp1, pp1)
            match.player2.update_player(pp2, pp2)
