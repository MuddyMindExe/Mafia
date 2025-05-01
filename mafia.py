import asyncio
from game.lobby import Lobby
from gl import current_games, current_lobbies, current_votes


class AsyncLobbyInteraction:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def start(self, host_id, time, mafia_amt, doc_amt, sherif_amt):
        lobby = Lobby(host_id, time, mafia_amt, doc_amt, sherif_amt)
        async with self._lock:
            current_lobbies.add(host_id, lobby)

    async def delete(self, host_id):
        async with self._lock:
            current_lobbies.delete(host_id)

    @staticmethod
    async def find_player(target_id):
        await asyncio.to_thread(current_lobbies.find_player, target_id)


class AsyncGameInteraction:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def start(self):
        pass
