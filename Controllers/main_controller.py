from Controllers.tournament_controller import TournamentController
from Controllers.player_controller import Playercontroller
from Controllers.round_controller import RoundController
from Models.player import Player
from Models.tournament import Tournament
from Models.round import Round
from Views.menu_views import MainView
from Controllers.view_controller import ViewController


class MainController:
    def __init__(self):
        self.APP_RUNNING = True

    def run(self):
        menu_view = MainView()
        self.player_c = Playercontroller()

        while self.APP_RUNNING:
            self.tournament_controller = TournamentController()
            user_choice = menu_view.get_choice_menu()
            print(user_choice)
            if user_choice == "1":
                # CREATE A TOURNAMENT
                print("Create a tournament")
                tournament = self.tournament_controller.create_tournament()
                tournament.update_id_tournament()

                user_input = self.player_c.get_player_menu_choice()
                if user_input == "1":
                    loading_player = 0
                    # BEGIN TO LOAD PLAYERS FOR THE NEW TOURNAMENT
                    players = self.player_c.load_players()
                    players_aloaded = True
                    while players_aloaded:
                        nb_players = (input("How many players do you want to add to the tournament?\n"))
                        if not nb_players.isdigit() or int(nb_players) < 4:
                            print("Please enter a number between 4 and 8")
                        else:
                            players_aloaded = False
                    nb_players = int(nb_players)
                    while loading_player < nb_players:
                        self.player_c.display_players(players)
                        id_choice = int(input(f"Player{loading_player}/{nb_players} - Please enter ID\n"))
                        player = self.player_c.get_player(id_choice, players)
                        tournament.players.append(player)
                        players = self.player_c.refresh_players(id_choice,
                                                                players)
                        loading_player += 1
                    tournament_informations = (
                        tournament.model_to_dict(tournament)
                    )
                    tournament.save_tournament_db(tournament_informations)
                    tournament.update_tournament_field("id_tournament", tournament.id_tournament)
                else:
                    self.run()

            elif user_choice == "2":
                # LOAD A TOURNAMENT
                print("Load a tournament")
                tournament = Tournament.load_tournament_db()
                self.tournament_controller.show_tournament(tournament)
                id_tournament = (
                    int(input("Please enter the ID of the Tournament"))
                )
                load_tournament = self.tournament_controller.get_tournament(
                    id_tournament, tournament
                )
                load_tournament = dict(load_tournament)  # type: ignore

                actual_tournament = Tournament.dict_to_model(load_tournament)
                players = [
                    Player.dict_to_model(player) for
                    player in actual_tournament.players]  # type: ignore
                round_c = RoundController()
                print(actual_tournament.NB_TOURS)
                # CHECK IF THE TOURNAMENT IS END OR NOT
                if actual_tournament.start_tournament == actual_tournament.end_tournament:
                    for i in range(len(actual_tournament.rounds)):
                        actual_tournament.rounds[i] = Round.load_from_dictionary(actual_tournament.rounds[i])
                    # GERNERATE THE FIRST ROUND
                    if actual_tournament.actual_tour == 0:
                        round_c.generate_first_pair(players, actual_tournament)
                        _ = actual_tournament.update_players(actual_tournament)
                        actual_tournament.update_tournament_db(actual_tournament)
                    contine_round = True
                    # GENERATE ROUND BASED OF THE SCORE
                    while actual_tournament.actual_tour < actual_tournament.NB_TOURS and contine_round:
                        # actual_tournament.update_tournament_db()
                        players = [
                            Player.dict_to_model(player) for
                            player in actual_tournament.players]
                        pairing = round_c.generate_pair(players, actual_tournament)
                        actual_tournament.actual_tour += 1
                        new_r = Round(f"Rounds {actual_tournament.actual_tour}")
                        new_r.matches = pairing
                        actual_tournament.rounds.append(new_r)
                        new_r.present_match()

                        if user_choice := input("Continue round or quit ?\n") == "quit":
                            contine_round = False
                        else:
                            new_r.set_finish_round()
                            _ = actual_tournament.update_players(actual_tournament)
                            new_r.update_score(new_r)
                            actual_tournament.update_tournament_db(actual_tournament)
                    Player.reset_list_played()
                    actual_tournament.set_end_tournament()
                else:
                    print("Tournament ended \n")
                menu_view.display_score(actual_tournament)
                actual_tournament.update_tournament_db(actual_tournament)
            elif user_choice == "3":
                # DISPLAY REPORT
                print("Display reports")
                self.view_c = ViewController()
                self.view_c.report()
                self.view_c.report()

            elif user_choice == "4":
                # ADD PLAYER
                print("Add new player")
                player_adding = True
                while player_adding:
                    self.player_c.create_player()
                    user_choice = input("Continue to create player? y/n")

                    if user_choice == "n":
                        player_adding = False
            else:
                # QUIT APPLICATION
                print("Thanks you")
                self.APP_RUNNING = False
