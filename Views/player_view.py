from datetime import datetime
from Models.player import Player
PLAYER_CHOICE: dict = {"1": "Load Players", "q": "back"}
OPTIONS_MESSAGE: str = "Please, make your selection: "
ERROR_MESSAGE: str = "Invalid answer, please try again."


class PlayerView:

    def display_player_choice(self) -> None:
        # Display the player choice menu when the app is launch
        for key, value in PLAYER_CHOICE.items():
            print(f"{key}: {value} ")

    def get_player_informations(self) -> dict:
        # Get a dict of player informations
        informations_needed: list = [
            "last_name", "first_name", "date_of_birth", "national_id"
        ]
        player: dict = {}

        for information in informations_needed:
            if information == "date_of_birth":
                is_valid_date = False
                # print("Please enter the date in the format DD/MM/YYYY")
                while not is_valid_date:
                    date_input = input(f"Please enter the information: {information} DD/MM/YYYY\n")
                    try:
                        datetime.strptime(date_input, "%d/%m/%Y")
                        is_valid_date = True
                    except ValueError:
                        print("Invalid date format. Please try again.")
                player[information] = date_input

            if information == "national_id":
                is_valid_national_id = False
                print(f"Please enter the information: {information} \n")
                print("Please enter the national id in the format AB12345")
                while not is_valid_national_id:
                    national_id_input = input()
                    if len(national_id_input) == 7 and national_id_input[0:2].  isalpha() and national_id_input[3:].isdigit() and Player.national_id_is_valid(national_id_input):
                        is_valid_national_id = True
                    else:
                        print("Invalid national id format. Please try again.")
                player[information] = national_id_input
            else:
                valid_info = False
                while not valid_info:
                    player[information] = input(
                        f"Please enter the information: {information} \n"
                    )
                    if player[information] != "":
                        valid_info = True
                    else:
                        print("Please enter a valid information.")
        player["tournament_score"] = 0.0
        return player

    def get_choice_input(self) -> str:
        return input(OPTIONS_MESSAGE)

    def is_valid_choice(self, input_user: str) -> bool:
        return input_user in PLAYER_CHOICE

    def get_user_choice(self) -> str:
        user_choice = self.get_choice_input()

        if not self.is_valid_choice(user_choice):
            print(ERROR_MESSAGE + "\n")
            self.get_user_choice()
        return user_choice
