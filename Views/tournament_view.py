class TournamentView:

    def get_tournament_informations(self) -> dict:
        # Get the tournament informations
        labels_tournament: list = ["name", "location", "description"]
        Tournament_informations: dict = {}
        for label in labels_tournament:
            is_valid = False
            while not is_valid:
                Tournament_informations[label] = input(
                    f"{label}: please enter a {label}: \n"
                )
                if Tournament_informations[label] != "":
                    is_valid = True
                else:
                    print("Please enter a valid information.")
        return Tournament_informations

    def get_nb_tours(self) -> int:
        # Get the number of tours
        nb_tour = input("Please enter the number of tours: (4 default)\n")
        if nb_tour == "":
            nb_tour = 4
        return int(nb_tour)
