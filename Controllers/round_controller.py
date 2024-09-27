from Models.match import Match
from Models.round import Round
from random import shuffle


class RoundController:
    def generate_first_pair(self, players, tournament):
        """
            Generate the first pair of the first round based of a shuffle list of players
        """
        shuffle(players)
        first_round = Round(name="Round 1")
        for i in range(0, len(players), 2):
            player1 = players[i]
            player2 = players[i + 1]
            player1.player_allready_played.append(player2.national_id)
            player2.player_allready_played.append(player1.national_id)
            match = Match(player1, player2)
            first_round.adding_match(match)
        tournament.rounds.append(first_round)
        first_round.present_match()
        first_round.update_score(first_round)
        first_round.set_finish_round()
        tournament.actual_tour += 1

    def generate_pair(self, players, tournament):
        """
            Generate a list of match based of the score of the players
            the player cannot played against a other player allready
        """
        players = sorted(players, key=lambda x: x.score, reverse=True)
        pairings = []
        players_with_pair = set()  # Suivi des joueurs déjà appariés

        num_players = len(players)
        if num_players < 2:
            raise ValueError("At least 2 players are required to generate pairings.")

        # D'abord, essayer de faire des paires avec des joueurs qui n'ont jamais joué ensemble
        for player in players:
            if player in players_with_pair:
                continue  # Ce joueur est déjà apparié, on passe au suivant
            for opponent in players:
                if opponent == player or opponent in players_with_pair:
                    continue  # Ne pas s'auto-apparier ou apparier un joueur déjà apparié

                # Vérifier si ces joueurs ont déjà joué ensemble
                if (opponent.national_id not in player.player_allready_played and player.national_id not in opponent.player_allready_played):
                    # Créer le match et mettre à jour les listes
                    match = Match(player, opponent)
                    pairings.append(match)
                    player.player_allready_played.append(opponent.national_id)
                    opponent.player_allready_played.append(player.national_id)
                    players_with_pair.add(player)
                    players_with_pair.add(opponent)
                    break  # On a trouvé un appariement pour ce joueur, on passe au suivant

        # Ensuite, si certains joueurs ne sont pas encore appariés, on les apparie malgré les matchs passés
        for player in players:
            if player in players_with_pair:
                continue  # Ce joueur est déjà apparié

            for opponent in players:
                if opponent == player or opponent in players_with_pair:
                    continue  # Ne pas s'auto-apparier ou apparier un joueur déjà apparié

                # Créer un match, même si les joueurs ont déjà joué ensemble
                match = Match(player, opponent)
                pairings.append(match)
                players_with_pair.add(player)
                players_with_pair.add(opponent)
                break  # On a trouvé un appariement pour ce joueur, on passe au suivant

        # Si le nombre de matches est inférieur à la moitié des joueurs, lever une exception
        if len(pairings) < (len(players) / 2):
            raise Exception("Not enough pairings could be generated.")

        return pairings
