from prettytable import PrettyTable


OPTION_MENU: dict = {
    "1": "Create new tournament.",
    "2": "Load tournament",
    "3": "Display reports.",
    "4": "Add new player.",
    "q": "Quit app",
}
WELCOME_MESSAGE: str = "Welcome, please choose one the following options:"
OPTIONS_MESSAGE: str = "Please, make your selection: "
ERROR_MESSAGE: str = "Invalid answer, please try again."


class MainView:
    def display_welcomming_message(self):
        # Display the main message when the app is launch
        print(WELCOME_MESSAGE)

    def display_menu(self) -> None:
        # Display a list of option for the user
        for key, value in OPTION_MENU.items():
            print(f"{key}: {value}")

    def get_user_input(self) -> str:
        # Get the input of the user
        return input(OPTIONS_MESSAGE)

    def is_valid_input(self, user_input) -> bool:
        # Check if the input of the user is valid
        if user_input not in OPTION_MENU.keys():
            return False
        return True

    def get_choice_menu(self) -> str:
        # The program get the user choice
        self.display_welcomming_message()
        self.display_menu()
        user_choice = self.get_user_input()

        if not self.is_valid_input(user_choice):
            print(ERROR_MESSAGE + "\n")
            self.get_choice_menu()
        return user_choice

    def display_score(self, tournament):
        # Display the score of 2 players
        table = PrettyTable()
        player_scores = {}
        for r in tournament.rounds[-1].matches:
            p1 = r.player1
            p2 = r.player2
            if p1.full_name not in player_scores:
                player_scores[p1.full_name] = p1.tournament_score
            if p2.full_name not in player_scores:
                player_scores[p2.full_name] = p2.tournament_score
        player_scores = dict(sorted(player_scores.items(), key=lambda x: x[1], reverse=True))
        table.field_names = ["Player_name", "Score"]
        for player, score in player_scores.items():
            table.add_row([
                player, score
            ])
        print(table)
