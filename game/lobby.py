from game.game import Game, GameCreator, Mafia, Sherif, Doc, Citizen
import random
from errors import GameErrors


class Lobby:
    """
    Represents a game lobby where players can join before the game starts.

    Attributes:
        host_id (int): The ID of the host player.
        time (int): Game start's at day (True) or night (False).
        players (set): A set of player IDs who joined the lobby.
        mafia_amt (int): Number of mafia roles to assign.
        sherif_amt (int): Number of sherif roles to assign.
        doc_amt (int): Number of doctor roles to assign.
        game (Game): A GameCreator instance to build the game.
        min_players_amt (int): Minimum required number of players to start the game.
    """
    def __init__(self, host_id, time, mafia_amt, doc_amt, sherif_amt):
        self.host_id    = host_id
        self.time       = time
        self.players    = set()
        self.mafia_amt  = mafia_amt
        self.sherif_amt = sherif_amt
        self.doc_amt    = doc_amt
        self.game       = GameCreator().set_host(self.host_id).set_time(self.time)
        self.min_players_amt = self.mafia_amt + self.sherif_amt + self.doc_amt + 2

    def add_player(self, player_id: int):
        """
        Adds a player's ID to the set of players.

        Args:
            player_id (int): The ID of the player to add.

        Returns:
            Lobby: The current instance to allow method chaining.
        """
        self.players.add(player_id)
        return self

    def remove_player(self, player_id: int):
        """
        Removes a player's ID from the set of players.

        Args:
            player_id (int): The ID of the player to remove.

        Returns:
            Lobby: The current instance to allow method chaining.
        """
        self.players.discard(player_id)
        return self

    def create_game(self) -> Game:
        """
        Converts the current Lobby instance into a Game instance and starts the game.
        If the number of players is sufficient, assigns roles and starts the game.

        Raises:
            NotEnoughPlayersError: If the number of players is less than the required minimum.

        Returns:
            Game: An instance representing the running game session.
        """
        if len(self.players) < self.min_players_amt:
            raise GameErrors.NotEnoughPlayersError()
        players = self.role_assignment()
        self.game.set_players(players).build()
        return self.game

    def role_assignment(self) -> dict:
        """
        Assigns roles to all players based on the configured amounts.

        Returns:
            dict of players with roles
        """
        available = list(self.players)
        mafia   = {key: Mafia()   for key in Lobby.__role_assign(available, self.mafia_amt)}
        sherif  = {key: Sherif()  for key in Lobby.__role_assign(available, self.sherif_amt)}
        doc     = {key: Doc()     for key in Lobby.__role_assign(available, self.doc_amt)}
        citizen = {key: Citizen() for key in available}
        return mafia | sherif | doc | citizen

    @staticmethod
    def __role_assign(players: list[int], amt: int) -> list:
        """
        Selects and removes a given number of random player IDs from the list.

        Args:
            players (list[int]): List of available player IDs to choose from.
            amt (int): Number of players to select.

        Returns:
            list[int]: A list of selected player IDs.
        """
        chosen = random.sample(players, amt)
        for el in chosen:
            players.remove(el)
        return chosen

    def __repr__(self):
        return (f"host_id: {self.host_id}, "
                f"time: {self.time}, "
                f"players: {self.players}, "
                f"mafia_amt: {self.mafia_amt}, "
                f"doc_amt: {self.doc_amt}, "
                f"sherif_amt: {self.sherif_amt}")
