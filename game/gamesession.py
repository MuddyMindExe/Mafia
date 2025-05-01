import asyncio
from player import Mafia, Sherif, Doc
from game.game import Game
from errors import GameErrors
from abc import ABC, abstractmethod


class AsyncGameSession(ABC):
    @abstractmethod
    async def mafia_move(self, inter_id, target_id):
        pass

    @abstractmethod
    async def doc_move(self, inter_id, target_id):
        pass

    @abstractmethod
    async def sherif_move(self, inter_id, target_id):
        pass

    @abstractmethod
    async def day(self):
        pass

    @abstractmethod
    async def night(self):
        pass


class GameSession(AsyncGameSession):
    def __init__(self, game_obj: Game):
        self.game_obj = game_obj
        self.mafia_event = asyncio.Event()
        self.doc_event = asyncio.Event()
        self.sherif_event = asyncio.Event()
        self.exe_queue = asyncio.Queue()

    async def mafia_move(self, inter_id, target_id):
        if self.game_obj.time:
            raise GameErrors.TimeError()
        if self.doc_event.is_set():
            await asyncio.to_thread(self.game_obj.move, inter_id, target_id, Mafia)
            self.mafia_event.set()
        else:
            await self.exe_queue.put(self.game_obj.move(inter_id, target_id, Mafia))

    async def doc_move(self, inter_id, target_id):
        await asyncio.to_thread(self.game_obj.move(inter_id, target_id, Doc))

    async def sherif_move(self, inter_id, target_id):
        return self.game_obj.move(inter_id, target_id, Sherif)

    async def day(self):
        if all([self.mafia_event.is_set(), self.doc_event.is_set()]):
            await asyncio.to_thread(self.game_obj.day())
        else:
            raise GameErrors.NotReadyError

    async def night(self):
        await asyncio.to_thread(self.game_obj.night())
        self.mafia_event.clear()
        self.doc_event.clear()
        self.sherif_event.clear()
