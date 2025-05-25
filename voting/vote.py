from abc import ABC, abstractmethod
from dataclasses import dataclass
from voting.votestorage import VotesManager
import asyncio


class Vote(ABC):
    """Abstract base class for voting systems"""

    def __init__(self, host_id: int, votes_manager: VotesManager):
        self.host_id = host_id
        self.votes_manager = votes_manager

    @abstractmethod
    async def add_vote(self, inter_id, target_id) -> None: ...

    @abstractmethod
    async def remove_vote(self, inter_id) -> None: ...

    @abstractmethod
    async def vote_result(self) -> list[int]: ...


@dataclass
class VoteKick(Vote):
    """Implementation for kick voting system"""

    host_id: int
    votes_manager: VotesManager

    async def add_vote(self, inter_id: int, target_id: int) -> None:
        self.votes_manager.add_vote(inter_id, target_id)

    async def remove_vote(self, inter_id: int) -> None:
        self.votes_manager.remove_vote(inter_id)

    async def vote_result(self) -> list[int]:
        return self.votes_manager.vote_result()


class VoteCreator:
    """Vote instances factory"""

    def __init__(self, host_id: int, players: list[int]):
        self.host_id = host_id
        self.votes_manager = VotesManager(players)

    def create(self) -> VoteKick:
        return VoteKick(self.host_id, self.votes_manager)
