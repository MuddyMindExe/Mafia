import asyncio
from game.lobby import Lobby
from gl import current_games, current_lobbies, current_votes
from errors import GameErrors, LobbyErrors, VotingErrors, GeneralErrors


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

    async def add_player(self, host_id, inter_id):
        lobby = current_lobbies.lobbies.get(host_id)
        async with self._lock:
            lobby.add_player(inter_id)

    async def remove_player(self, host_id, inter_id):
        lobby = current_lobbies.lobbies.get(host_id)
        async with self._lock:
            lobby.remove_player(inter_id)

    @staticmethod
    async def find_player(target_id):
        await asyncio.to_thread(current_lobbies.find_player, target_id)


class AsyncGameInteraction:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def start(self, host_id):
        lobby = current_lobbies.lobbies.get()
        if not lobby:
            raise LobbyErrors.LobbyNotFoundError()
        game = lobby.create_game()
        async with self._lock:
            current_games.add(host_id, game)
            current_lobbies.delete(host_id)

    async def delete(self, host_id):
        async with self._lock:
            current_games.delete(host_id)


class AsyncVoteInteraction:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def add_vote(self, host_id, inter_id, target_id):
        vote = current_votes.votes.get(host_id)
        players = vote.voters.players
        if not vote:
            raise GeneralErrors.ObjNotExists()
        if inter_id not in players or target_id not in players:
            raise VotingErrors.VotingPermissionError()
        async with self._lock:
            vote.votes.add_vote(inter_id, target_id)

    async def remove_vote(self, host_id, inter_id, target_id):
        vote = current_votes.votes.get(host_id)
        voters = vote.voters.voters
        if not vote:
            raise GeneralErrors.ObjNotExists()
        if inter_id not in voters:
            raise VotingErrors.VotingPermissionError()
        if target_id not in voters.
        async with self._lock:
            vote.votes.add_vote(inter_id, target_id)


