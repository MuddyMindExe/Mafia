from player import Mafia, Sherif, Doc, Citizen
from errors import *


class Game:
    def __init__(self, host: int, time: bool, players: dict[int, Mafia | Doc | Sherif | Citizen]):
        self.host = host
        self.time = time
        self.players = players

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
        player.action(self.players, target)

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
        return self.players.get(target_id)


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

    def set_players(self, players: dict[int, Mafia | Doc | Sherif | Citizen]):
        self.players = players
        return self

    def build(self) -> Game:
        if not all([self.host, self.time, self.players]):
            raise ValueError("Missing required fields")
        return Game(self.host, self.time, self.players)
