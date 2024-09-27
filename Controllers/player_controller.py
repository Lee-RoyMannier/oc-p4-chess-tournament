from Models.player import Player
from Views.player_view import PlayerView
from prettytable import PrettyTable


class Playercontroller:
    def __init__(self):
        self.player_view = PlayerView()

    def create_player(self):
        # CREATE A NEW PLAYER BASED OF INFORMATIONS GET IN THE VIEW
        player_informations = self.player_view.get_player_informations()
        player_model = Player.dict_to_model(player_informations)
        player_informations = player_model.model_to_dict(player_model)
        player_model.save_player_db(player_informations)

    def get_player_menu_choice(self):
        self.player_view.display_player_choice()
        user_choice = self.player_view.get_user_choice()

        return user_choice

    def display_players(self, players: list):
        table = PrettyTable()
        table.field_names = players[0].keys()

        for player in players:
            table.add_row([
                player['first_name'],
                player['last_name'],
                player['date_of_birth'],
                player['national_id'],
                player['score'],
                ", ".join(player['player_allready_played']),
                player["tournament_score"],
                player["id"],
            ])
        print(table)

    def load_players(self) -> list:
        players = Player.load_player_db()
        return players

    def get_player(self, id, players):
        for player in players:
            if player["id"] == id:
                return player

    def refresh_players(self, id, players):
        # REFRESH THE PLAYERS VIEW WHEN A PLAYE IS CHOSEN
        for player in players:
            if player["id"] == id:
                if len(players) > 1:
                    players.remove(player)

        return players
