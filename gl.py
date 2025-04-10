from mafia import Game, Lobby, Vote
from abc import ABC, abstractmethod


class ObjStorage(ABC):  # *
    @abstractmethod
    def add(self, host_id, game: Game):
        pass

    @abstractmethod
    def delete(self, host_id):
        pass

    @abstractmethod
    def find_player(self, player_id):
        pass


class Games(ObjStorage):
    def __init__(self):
        self.games: dict[int, Game] = {}

    def add(self, host_id, game: Game):
        self.games[host_id] = game

    def delete(self, host_id):
        del self.games[host_id]

    def find_player(self, player_id):
        if self.games[player_id]:
            return True
        for game in self.games.values():
            if game.players[player_id]:
                return True
        return False


class Lobbies:
    def __init__(self):
        self.lobbies: dict[int, Lobby] = {}

    def add(self, host_id, lobby: Lobby):
        self.lobbies[host_id] = lobby

    def delete(self, host_id):
        del self.lobbies[host_id]

    def find_player(self, player_id):
        return any(player_id in lobby.players for lobby in self.lobbies.values())


class Votes(ObjStorage):
    def __init__(self):
        self.votes: dict[int, Vote] = {}

    def add(self, host_id, vote):
        self.votes[host_id] = vote

    def delete(self, host_id):
        del self.votes[host_id]

    def find_player(self, player_id):
        if self.votes[player_id]:
            return True
        for vote in self.votes.values():
            if player_id in vote.players:
                return True
        return False


current_votes = Votes()
current_games = Games()
current_lobbies = Lobbies()
