from game.player import Mafia, Sherif, Doc, Citizen
from errors import *


class Game:
    def __init__(self, host_id: int, time: bool, players: dict[int, Mafia | Doc | Sherif | Citizen]):
        self.host_id = host_id
        self.time = time
        self.players = players

    @staticmethod
    def _move_validation(player, target, role_type):
        if player is None:
            raise PlayerErrors.PlayerNotFoundError()
        if target is None:
            raise PlayerErrors.TargetNotFoundError()
        if not isinstance(player, role_type):
            raise PlayerErrors.ActionPermissionError()

    def move(self, inter_id: int, target_id: int, role_type):  # *
        if self.time:
            raise GameErrors.TimeError()
        player = self.get_player(inter_id)
        target = self.get_player(target_id)
        Game._move_validation(player, target, role_type)
        player.action(self.players, target)

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

    def remove_player(self, target_id):
        pass


class GameCreator:
    def __init__(self):
        self.host_id = None
        self.time = True
        self.players = None

    def set_time(self, time: bool):
        self.time = time
        return self

    def set_host_id(self, host_id: int):
        self.host_id = host_id
        return self

    def set_players(self, players: dict[int, Mafia | Doc | Sherif | Citizen]):
        self.players = players
        return self

    def build(self) -> Game:
        if not all([self.host_id, self.time, self.players]):
            raise ValueError("Missing required fields")
        return Game(self.host_id, self.time, self.players)
