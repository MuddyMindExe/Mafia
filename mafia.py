from player import Mafia, Sherif, Doc, Citizen
from errors import *


class Game:
    def __init__(self, host: int, time: bool, players: dict):
        self.host = host
        self.time = time
        self.players: dict[int, Mafia | Sherif | Doc | Citizen] = players

    def move(self, inter_id: int, target_id: int, role_type):  # *
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

    def day(self):  # В боте идет проверка на отсутствие голосования
        if self.time:
            return
        self.time = True

    def night(self):  # В боте идет проверка на отсутствие голосования
        if not self.time:
            return


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
