import asyncio
from game.lobby import *
from game.game import *
from gl import current_games, current_lobbies, current_votes
from errors import *


class AsyncLobbyInteraction:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def start(self, host_id: int, time: bool, mafia_amt: int, doc_amt: int, sheriff_amt: int) -> bool:
        """
        Creates a Lobby object and adds it to storage

        Args:
            host_id (int): unique ID of a host, which is used as a key to get game objects
            time (bool): time the game starts with:
            True means the game starts during the day; False means it starts at night
            mafia_amt (int): the amount of players with mafia role
            doc_amt (int): the amount of players with doctor role
            sheriff_amt (int): the amount of players with sherif role
        Returns:
            True: if lobby was successfully created
            False: if chosen host is already a part of another game/lobby
        """
        async with self._lock:
            if AsyncLobbyInteraction.find_player(host_id):
                return False
            lobby = Lobby(host_id, time, mafia_amt, doc_amt, sheriff_amt)
            current_lobbies.add(host_id, lobby)
            return True

    async def delete(self, host_id: int) -> bool:
        """
        Deletes a Lobby from storage

        Args:
            host_id (int): unique ID of a host, which is used as a key to get game objects

        Returns:
             bool: True if the lobby was successfully removed

        Raises:
            GeneralErrors.ObjNotExists: occurs when user tries to delete a non-existent Lobby
        """
        async with self._lock:
            res = current_lobbies.delete(host_id)
            if not current_lobbies:
                raise GeneralErrors.ObjNotExists
            return True

    async def add_player(self, host_id: int, target_id: int) -> bool:
        """
        Adds player to a list of players in Lobby

        Args:
            host_id (int): unique ID of a host, which is used as a key to get a Lobby object
            inter_id (int): unique ID of a player, who wants to join a lobby

        Returns:
            True: if player was successfully added to the storage
            False: if player already parrticipates a Lobby or a Game
        """
        async with self._lock:
            if not any(find_player_in_game(target_id), find_player_in_lobby(target_id)):
                return False
            lobby = current_lobbies.lobbies.get(host_id)
            lobby.add_player(target_id)
            return True

    async def remove_player(self, host_id: int, inter_id: int) -> None:
        """
        Removes a player from a list of players in Lobby

        Args:
            host_id (int): unique ID of a host, which is used as a key to get a Lobby object
            inter_id (int): unique ID of a player, who wants to join a lobby
        """
        async with self._lock:
            lobby = current_lobbies.lobbies.get(host_id)
            lobby.remove_player(inter_id)


class AsyncGameInteraction:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def start(self, host_id: int) -> dict[int, Mafia | Sherif | Doc | Citizen]:
        lobby = current_lobbies.lobbies.get()
        if not lobby:
            raise LobbyErrors.LobbyNotFoundError()
        game, players = lobby.create_game()
        async with self._lock:
            current_games.add(host_id, game)
            current_lobbies.delete(host_id)
            return players

    async def delete(self, host_id: int):
        async with self._lock:
            current_games.delete(host_id)

    async def day(self, host_id: int):
        async with self._lock:
            game = current_games.games.get(host_id)
            game.day()

    async def night(self, host_id: int):
        async with self._lock:
            game = current_games.games.get(host_id)
            game.night()

    async def move(self, inter_id: int, target_id: int, role_type):
        async with self._lock:
            host_id = find_player_in_game(inter_id)
            if not host_id:
                raise PlayerErrors.PlayerNotFoundError
            game = current_games.games.get(host_id)
            game.move(inter_id, target_id, Mafia)


class AsyncVoteInteraction:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def add_vote(self, host_id, inter_id, target_id):
        vote_session = current_votes.votes.get(host_id)
        if not vote_session:
            raise GeneralErrors.ObjNotExists()
        async with self._lock:
            vote_session.votes.add_vote(inter_id, target_id)

    async def remove_vote(self, host_id, inter_id):
        vote_session = current_votes.votes.get(host_id)
        if not vote_session:
            raise GeneralErrors.ObjNotExists()
        async with self._lock:
            vote_session.remove_vote(inter_id)


async def find_player_in_lobby(target_id: int) -> bool | int:
    return await asyncio.to_thread(current_lobbies.find_player, target_id)


async def find_player_in_game(target_id: int) -> bool | int:
    return await asyncio.to_thread(current_games.find_player, target_id)
