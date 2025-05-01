from player import Mafia, Sherif, Doc, Citizen
from errors import *


class Game:
    def __init__(self, host: int, time: bool, mafia, doc, sherif, citizen):
        self.host = host
        self.time = time
        self.mafia = mafia
        self.doc = doc
        self.sherif = sherif
        self.citizen = citizen
        self.union: dict = self.mafia | self.doc | self.sherif | self.citizen

    def move(self, inter_id: int, target_id: int, role_type):  # *
        if self.time:
            raise GameErrors.TimeError()
        player = self.get_player(inter_id)
        target = self.get_player(target_id)
        if player is None:
            raise PlayerErrors.PlayerNotFoundError()
        if target is None:
            raise PlayerErrors.TargetNotFoundError()
        if not isinstance(player, role_type):
            raise PlayerErrors.ActionPermissionError()
        player.action(self.union, target)

    # def finish_ready(self):
    #     if
    #     if not any(isinstance(obj, Mafia) for obj in self.players.values()):
    #         return True

    def day(self):
        if self.time:
            raise GameErrors.TimeError()
        self.time = True

    def night(self):
        if not self.time:
            raise GameErrors.TimeError()
        self.time = False

    def get_player(self, target_id):
        return self.union.get(target_id)


class GameCreator:
    def __init__(self):
        self.host = None
        self.time = True
        self.mafia = None
        self.doc = None
        self.sherif = None
        self.citizen = None

    def set_time(self, time: bool):
        self.time = time
        return self

    def set_host(self, host: int):
        self.host = host
        return self

    def set_players(self, mafia: dict, doc: dict, sherif: dict, citizen: dict):
        self.mafia = mafia
        self.doc = doc
        self.sherif = sherif
        self.citizen = citizen
        return self

    def build(self) -> Game:
        if not all([self.host, self.time, self.mafia, self.doc, self.sherif, self.citizen]):
            raise ValueError("Missing required fields")
        return Game(self.host, self.time, self.mafia, self.doc, self.sherif, self.citizen)
