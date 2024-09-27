from Models.tournament import Tournament
from Views.tournament_view import TournamentView
from prettytable import PrettyTable


class TournamentController:
    def __init__(self):
        self.tournament_view: TournamentView = TournamentView()

    def create_tournament(self) -> Tournament:
        tournament_informations: dict = (
            self.tournament_view.get_tournament_informations()
        )
        tournament = Tournament.dict_to_model(tournament_informations)
        nb_tours = self.tournament_view.get_nb_tours()
        tournament.change_nb_tours(nb_tours)
        return tournament

    def show_tournament(self, tournament) -> None:
        table = PrettyTable()
        column_names: list = [
            "name", "location", "start_tournament",
            "end_tournament", "actual_tour", "description",
            "id",
        ]
        table.field_names = column_names

        for t in tournament:
            table.add_row([
                t['name'],
                t['location'],
                t['start_tournament'],
                t['end_tournament'],
                t['actual_tour'],
                t['description'],
                t["id"],
            ])
        print(table)

    def show_tournament_report(self, tournament):
        table = PrettyTable()
        column_names: list = [
            "name", "location", "start_tournament",
            "end_tournament", "actual_tour", "description",
            "id",
        ]
        table.field_names = column_names

        table.add_row([
            tournament['name'],
            tournament['location'],
            tournament['start_tournament'],
            tournament['end_tournament'],
            tournament['actual_tour'],
            tournament['description'],
            tournament["id"],
        ])

        print(table)

    def get_tournament(self, id, tournament):
        for t in tournament:
            if id == t["id"]:
                return t
