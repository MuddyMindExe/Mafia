import random
import threading
from player import Mafia, Sherif, Doc, Citizen
from errors import *


class Vote:
    def __init__(self, host: int, players: list[int]):
        self.host = host
        self.players = players
        self.votes: dict[int, list] = {player_id: [] for player_id in self.players}
        self.voters = []

    def add_vote(self, inter_id, target_id):
        if inter_id == self.host:
            raise VotingErrors.HostVotingError()
        if inter_id == target_id:
            raise VotingErrors.SelfVotingError()
        if inter_id in self.voters:
            raise VotingErrors.AlreadyVotedError()
        target_votes: list = self.votes[target_id]
        self.__add_player(target_votes, inter_id)
        self.__add_player(self.voters, inter_id)
        self.__remove_player(self.players, inter_id)

    def remove_vote(self, inter_id):
        if inter_id == self.host:
            raise VotingErrors.HostVotingError
        if inter_id not in self.voters:
            raise VotingErrors.SelfVotingError
        voters = self.votes.values()
        for voter_list in voters:
            if inter_id in voter_list:
                self.__remove_player(voter_list, inter_id)

    def __add_player(self, arr: list, player: int):
        if player not in arr:
            arr.append(player)

    def __remove_player(self, l: list, player: int):
        if player in l:
            l.remove(player)


class Game:
    def __init__(self, host: int, time: bool, players: dict):
        self.host = host
        self.time = time
        self.players: dict[int, Mafia | Sherif | Doc | Citizen] = players
        self.mafia_act = threading.Event()
        self.doc_act = threading.Event()
        self.sherif_act = threading.Event()
        self.voting = threading.Event()

    def move(self, inter_id: int, target_id: int, role_type, event: threading.Event):  # *
        if self.time:
            raise GameErrors.TimeError()
        player = self.players.get(inter_id)
        target = self.players.get(target_id)
        if player is None:
            raise ActionErrors.PlayerNotFoundError()
        if target is None:
            raise ActionErrors.TargetNotFoundError()
        if not isinstance(player, role_type):
            raise ActionErrors.ActionPermissionError()
        player.action(self.players, target)
        event.set()

    def start_vote(self):
        return Vote(self.host, list(self.players.keys()))

    def day(self):
        if self.time:
            return
        self.mafia_act.clear()
        self.sherif_act.clear()
        self.doc_act.clear()
        self.time = True

    def night(self):
        if not self.time:
            return
        self.time = False
        self.mafia_act.wait()
        self.sherif_act.wait()
        self.doc_act.wait()


class GameCreator:
    def __init__(self):
        self.host = None
        self.time = True
        self.players = None

    def set_time(self, time: bool):
        self.time = time
        return self

    def set_host(self, host: int):
        self.host = host
        return self

    def set_players(self, players: dict):
        self.players = players
        return self

    def build(self) -> Game:
        if not all([self.host, self.time, self.players]):
            raise ValueError("Missing required fields")
        return Game(self.host, self.time, self.players)


class Lobby:
    def __init__(self, host, time, mafia_amt, sherif_amt, doc_amt):
        self.host = host
        self.time = time
        self.players = set()
        self.mafia_amt = mafia_amt
        self.sherif_amt = sherif_amt
        self.doc_amt = doc_amt
        self.min_players_amt = self.mafia_amt + self.sherif_amt + self.doc_amt + 2
        self.game = GameCreator().set_host(self.host).set_time(self.time)

    def add_player(self, player_id):
        self.players.add(player_id)
        return self

    def remove_player(self, player_id):
        self.players.remove(player_id)
        return self

    def create_game(self):
        if not len(self.players) >= self.min_players_amt:
            return False
        players = self.role_assignment()
        self.game.set_players(players).build()
        return self.game

    def role_assignment(self) -> dict:
        mafia = {key: Mafia() for key in self.__role_assign(self.mafia_amt)}
        sherif = {key: Sherif() for key in self.__role_assign(self.sherif_amt)}
        doc = {key: Doc() for key in self.__role_assign(self.doc_amt)}
        citizen = {key: Mafia() for key in self.players}
        return mafia | sherif | doc | citizen

    def __role_assign(self, amt: int) -> list:
        chosen = random.sample(self.players, amt)
        for el in chosen:
            self.players.remove(el)
        return chosen
