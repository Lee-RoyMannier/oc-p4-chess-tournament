from Views.view_report import ViewReport
from Models.tournament import Tournament
from Controllers.player_controller import Playercontroller
from Controllers.tournament_controller import TournamentController


class ViewController:
    def __init__(self):
        self.view_c = ViewReport()

    def report(self):
        self.view_c.display_report_menu()
        user_choice = self.view_c.get_user_choice()

        if user_choice == "1":
            print("liste de tous les joueurs par ordre alphabétique")
            player_c = Playercontroller()
            players = player_c.load_players()
            player_c.display_players(players)

        elif user_choice == "2":
            print("liste de tous les tournois")
            tournament = Tournament.load_tournament_db()
            tournament_controller = TournamentController()
            tournament_controller.show_tournament(tournament)

        elif user_choice == "3":
            self.display_tournament()

        elif user_choice == "4":
            print("liste des joueurs du tournoi par ordre alphabétique")
            self.display_all_player()

        elif user_choice == "5":
            print("liste des tours du tournoi et de tous les matchs du tour")
            self.display_all_tournament()

        elif user_choice == "6":
            exit()

    def display_all_tournament(self):
        tournament_name = input("Enter the tournament name: ")
        tournaments = Tournament.load_tournament_db()
        for tournament in tournaments:
            for k in tournament:
                if tournament_name == tournament["name"]:
                    rounds = (tournament["rounds"])
                    break

        html_content = "<html><head><style>"
        html_content += "table {width: 100%; border-collapse: collapse; margin-bottom: 20px;}"
        html_content += "th, td {border: 1px solid black; padding: 8px; text-align: left;}"
        html_content += "th {background-color: #f2f2f2;}"
        html_content += "</style></head><body>"

        for round_data in rounds:
            html_content += f"<h2>{round_data['name']}</h2>"
            html_content += f"<p>Start: {round_data['start_datetime']} | End: {round_data['end_datetime'] if 'end_datetime' in round_data else 'Ongoing'}</p>"
            html_content += "<table>"
            html_content += "<tr><th>White Player</th><th>Black Player</th><th>Score</th></tr>"

            for match in round_data['matches']:
                white_player = f"{match['white_player']['first_name']} {match['white_player']['last_name']}"
                black_player = f"{match['black_player']['first_name']} {match['black_player']['last_name']}"
                score = f"{match['white_player']['tournament_score']} - {match['black_player']['tournament_score']}"
                html_content += f"<tr><td>{white_player}</td><td>{black_player}</td><td>{score}</td></tr>"

            html_content += "</table>"

        html_content += "</body></html>"
        with open("test2.html", "w") as f:
            f.write(html_content)

    def display_all_player(self):
        player_c = Playercontroller()
        tournois_name = input("Name of the tournament: ")
        tournaments = Tournament.load_tournament_db()
        for tournament in tournaments:
            for k in tournament:
                if tournois_name == tournament["name"]:
                    players = tournament["players"]
                    player_c.display_players(players)
                    break

    def display_tournament(self):
        print("nom et dates d’un tournoi donné")
        self.tournament_controller = TournamentController()
        name = input("Name of the tournament : ")
        date = input("date(s) of the tournament")
        tournaments = Tournament.load_tournament_db()
        for tournament in tournaments:
            for k in tournament:
                if name == tournament["name"] and date == tournament["start_tournament"]:
                    self.tournament_controller.show_tournament_report(tournament)
                    break
