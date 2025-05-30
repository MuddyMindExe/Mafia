from abc import ABC, abstractmethod
from errors import *


class Player(ABC):
    def __init__(self):
        self.life = True
        self.choice = False

    def kill(self):
        self.life = False

    def revive(self):
        self.life = True

    def action(self, players: dict, target):
        if self.choice:
            raise PlayerErrors.ActionDoneError()
        self._action(players, target)
        self.choice = True

    @abstractmethod
    def _action(self, players: dict, target):
        pass


class Citizen(Player):
    def _action(self, players: dict, target: Player):
        pass


class Mafia(Citizen):
    def _action(self, players: dict, target: Player):
        if not target.life or isinstance(target, Mafia):
            raise PlayerErrors.UnacceptableTargetError()
        target.kill()
        return True


class Sherif(Citizen):
    def _action(self, players: dict, target: Player):
        if target == self:
            raise PlayerErrors.UnacceptableTargetError()
        return target.__class__.__name__


class Doc(Citizen):
    def _action(self, players: dict, target: Player):
        target.revive()
        return True
