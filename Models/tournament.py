from datetime import datetime
from tinydb import TinyDB, Query


class Tournament:
    """
        Model of a tournament:
        a tournament have a name,
        a start and finish date,
        the players in this tournament,
        a list of rounds,
        a description
    """

    def __init__(self, name: str, location: str, description: str):
        self.NB_TOURS: int = 4
        self.name = name
        self.location = location
        self.start_tournament = str(datetime.now().date())
        self.end_tournament = str(datetime.now().date())
        self.actual_tour: int = 0
        self.players: list = []
        self.rounds: list = []
        self.description = description
        self.id_tournament = 0
        self.tour_db = TinyDB("database/tournaments.json")

    def update_id_tournament(self):
        tmp = self.tour_db.all()
        if tmp:  # Vérifier si la base de données n'est pas vide
            print(tmp[-1]["id"])
            self.id_tournament = tmp[-1]["id"]
        else:
            self.id_tournament = 1  # Initialiser à 1 si la base est vide

    def update_tournament_field(self, field_name: str, new_value):
        """
        Met à jour un champ spécifique du tournoi dans la base de données.

        :param field_name: Le nom du champ à mettre à jour (par exemple, 'name', 'location').
        :param new_value: La nouvelle valeur à attribuer au champ.
        """
        TournamentQuery = Query()
        # Rechercher le tournoi dans la base de données avec l'id_tournament
        tournament = self.tour_db.get(TournamentQuery.id_tournament == self.id_tournament)

        if tournament:
            # Mettre à jour le champ spécifique
            self.tour_db.update({field_name: new_value}, TournamentQuery.id_tournament == self.id_tournament)
            # Mettre à jour l'attribut localement aussi si nécessaire
            setattr(self, field_name, new_value)
            print(f"Le champ '{field_name}' a été mis à jour avec succès.")
        else:
            print(f"Tournoi avec id {self.id_tournament} non trouvé.")

    def set_end_tournament(self):
        self.end_tournament = str(datetime.now())

    def model_to_dict(self, tournament: "Tournament") -> dict:
        tournament_info: dict = {
            "name": self.name,
            "location": self.location,
            "start_tournament": self.start_tournament,
            "end_tournament": self.end_tournament,
            "actual_tour": self.actual_tour,
            "players": self.players,
            "rounds": [self.rounds[i].to_dictionary() for i in range(len(self.rounds))],
            "description": self.description,
            "NB_TOURS": self.NB_TOURS,
            "id_tournament": self.id_tournament,
        }

        return tournament_info

    def change_nb_tours(self, nb_tours: int):
        self.NB_TOURS = nb_tours

    @classmethod
    def dict_to_model(cls, informations: dict) -> "Tournament":
        name = informations["name"]
        location = informations["location"]
        description = informations["description"]

        tournament = cls(name, location, description)

        if "start_tournament" in informations:
            tournament.start_tournament = informations["start_tournament"]

        if "end_tournament" in informations:
            tournament.end_tournament = informations["end_tournament"]

        tournament.actual_tour = informations.get("actual_tour", 0)
        tournament.players = informations.get("players", [])
        tournament.rounds = informations.get("rounds", [])
        tournament.NB_TOURS = informations.get("NB_TOURS", [])
        tournament.id_tournament = informations.get("id_tournament", 0)
        return tournament

    def save_tournament_db(self, tournament: dict):
        db = self.tour_db
        self.t_id = db.insert(tournament)
        db.update({"id": self.t_id}, doc_ids=[self.t_id])

    @staticmethod
    def load_tournament_db():
        db = TinyDB("database/tournaments.json")
        db.all()
        tournaments_list = []
        for item in db:
            tournaments_list.append(item)

        return tournaments_list

    def update_tournament_db(self, tournament_data):
        """Update tournament info (after each round) in database"""
        db = self.tour_db  # Chargement de la base de données
        TournamentQuery = Query()

        # Accès direct à l'attribut id_tournament depuis self
        tournament = db.get(TournamentQuery.id_tournament == self.id_tournament)

        if tournament:
            # Mise à jour des rounds
            db.update({"rounds": [round.to_dictionary() for round in self.rounds]}, TournamentQuery.id_tournament == self.id_tournament)
            # Mise à jour des joueurs
            db.update({"players": self.players}, TournamentQuery.id_tournament == self.id_tournament)
            # Mise à jour du tour actuel
            db.update({"actual_tour": self.actual_tour}, TournamentQuery.id_tournament == self.id_tournament)
        else:
            print(f"Tournoi avec id {self.id_tournament} non trouvé.")

    def update_players(self, tournament_dataa):
        tournament_data = self.model_to_dict(tournament_dataa)
        players = tournament_data["players"]
        rounds = tournament_data["rounds"]
        player_dict = {player["national_id"]: player for player in players}
        for round_data in rounds:
            # Parcourir chaque match dans le round
            for match in round_data["matches"]:
                # Récupérer les IDs des deux joueurs
                player1_id = match["player1"]["national_id"]
                player2_id = match["player2"]["national_id"]
            # Mettre à jour les scores des joueurs en fonction du match
                player_dict[player1_id]["score"] = match["player1"]["score"]
                player_dict[player2_id]["score"] = match["player2"]["score"]
                player_dict[player1_id]["tournament_score"] = match["player1"]["tournament_score"]
                player_dict[player2_id]["tournament_score"] = match["player2"]["tournament_score"]
        tournament_data["players"] = list(player_dict.values())
        return tournament_data
