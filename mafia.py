import random
import threading
from player import Mafia, Sherif, Doc, Citizen
from errors import *
from datahandler import DataHandler


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

    def day(self):  # В боте идет проверка на отсутствие голосования
        if self.time:
            return
        self.mafia_act.clear()
        self.sherif_act.clear()
        self.doc_act.clear()
        self.time = True
        self.start_vote()

    def night(self):  # В боте идет проверка на отсутствие голосования
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
        self.players.discard(player_id)
        return self

    def create_game(self):
        if len(self.players) < self.min_players_amt:
            return False
        players = self.role_assignment()
        self.game.set_players(players).build()
        return self.game

    def role_assignment(self) -> dict:
        mafia = {key: Mafia() for key in self.__role_assign(self.mafia_amt)}
        sherif = {key: Sherif() for key in self.__role_assign(self.sherif_amt)}
        doc = {key: Doc() for key in self.__role_assign(self.doc_amt)}
        citizen = {key: Citizen() for key in self.players}
        return mafia | sherif | doc | citizen

    def __role_assign(self, amt: int) -> list:
        chosen = random.sample(list(self.players), amt)
        for el in chosen:
            self.players.remove(el)
        return chosen
