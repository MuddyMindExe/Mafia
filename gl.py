from game.game import Game
from game.lobby import Lobby
from voting.votesession import VoteSession
from abc import ABC, abstractmethod


class ObjStorage(ABC):
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

    def find_player(self, target_id: int) -> bool:
        if self.games.get(target_id):
            return target_id
        for game in self.games.values():
            if target_id in game.players:
                return game.host_id
        return False


class Lobbies:
    def __init__(self):
        self.lobbies: dict[int, Lobby] = {}

    def add(self, host_id: int, lobby: Lobby) -> bool:
        if host_id in self.lobbies:
            return False
        self.lobbies[host_id] = lobby
        return True

    def delete(self, host_id: int) -> int | None:
        return self.lobbies.pop(host_id, None)

    def find_player(self, target_id: int) -> bool:
        if self.lobbies.get(target_id):
            return target_id
        for lobby in self.lobbies.values():
            if target_id in lobby.players:
                return lobby.host_id
        return False


class Votes(ObjStorage):
    def __init__(self):
        self.votes: dict[int, VoteSession] = {}

    def add(self, host_id, vote):
        self.votes[host_id] = vote

    def delete(self, host_id):
        del self.votes[host_id]

    def find_player(self, player_id):
        if self.votes.get(player_id):
            return True
        vote_sessions = self.votes.values()
        for vote_session in vote_sessions:
            vote = vote_session.vote_obj
            players = vote.votes_manager.voters.players.keys()
            if player_id in players:
                return True
        return False


class Players(ObjStorage):
    def __init__(self):
        self.players: dict[int, int] = {}

    def add(self):
        pass


current_games = Games()
current_lobbies = Lobbies()
current_votes = Votes()
