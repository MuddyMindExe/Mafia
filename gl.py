from game.game import Game
from game.lobby import Lobby
from voting.votesession import VoteSession
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
        if self.games.get(player_id):
            return True
        for game in self.games.values():
            if game.players.get(player_id):
                return True
        return False


class Lobbies:
    def __init__(self):
        self.lobbies: dict[int, Lobby] = {}

    def add(self, host_id, lobby: Lobby):
        self.lobbies[host_id] = lobby

    def delete(self, host_id):
        self.lobbies.pop(host_id, None)

    def find_player(self, target_id):
        if self.lobbies.get(target_id):
            return True
        return any(target_id in lobby.players for lobby in self.lobbies.values())


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


current_games = Games()
current_lobbies = Lobbies()
current_votes = Votes()
