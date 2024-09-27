REPORT_CHOICE: dict = {
    "1": "● liste de tous les joueurs par ordre alphabétique",
    "2": "● liste de tous les tournois",
    "3": "● nom et dates d’un tournoi donné",
    "4": "● liste des joueurs du tournoi par ordre alphabétique",
    "5": "● liste de tous les tours du tournoi et de tous les matchs du tour",
    "6": "● exit",
}


class ViewReport:

    def get_user_input(self):
        return input("Please enter your choice: \n")

    def is_valid_input(self, user_choice):
        return user_choice in REPORT_CHOICE

    def get_user_choice(self):
        user_choice = self.get_user_input()

        if not self.is_valid_input(user_choice):
            print("Enter a valid choice \n")
            self.get_user_choice()
        return user_choice

    def display_report_menu(self):
        for key, value in REPORT_CHOICE.items():
            print(f"{key}: {value}")
