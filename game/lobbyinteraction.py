from gl import current_lobbies
from lobby import Lobby
import asyncio


class LobbyInteraction:
    @staticmethod
    def start(host_id, time, mafia_amt, doc_amt, sherif_amt):
        lobby = Lobby(host_id, time, mafia_amt, doc_amt, sherif_amt)
        current_lobbies.add(host_id, lobby)

    @staticmethod
    def delete(host_id):
        current_lobbies.delete(host_id)


class AsyncLobbyInteraction:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def start(self, host_id, time, mafia_amt, doc_amt, sherif_amt):
        async with self._lock:
            lobby = Lobby(host_id, time, mafia_amt, doc_amt, sherif_amt)
            current_lobbies.add(host_id, lobby)

    async def delete(self, host_id):
        async with self._lock:
            current_lobbies.delete(host_id)

    async def add_player(self, host_id, inter_id):
        async with self._lock:
            lobby = current_lobbies.lobbies.get(host_id)
            lobby.add_player(inter_id)

    async def remove_player(self, host_id, inter_id):
        lobby = current_lobbies.lobbies.get(host_id)
        async with self._lock:
            lobby.remove_player(inter_id)

    @staticmethod
    async def find_player(target_id):
        await asyncio.to_thread(current_lobbies.find_player, target_id)
