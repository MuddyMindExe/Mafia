import asyncio
from vote import Vote
from abc import ABC, abstractmethod


class AsyncVoteSession(ABC):
    """Async voting interface with thread-safe implementations"""

    def __init__(self, vote_obj: Vote):
        self.vote_obj = vote_obj

    @abstractmethod
    async def add_vote(self, inter_id: int, target_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove_vote(self, inter_id: int) -> None:
        raise NotImplementedError


class VoteSession(AsyncVoteSession):
    """Thread-safe voting using asyncio locks"""

    def __init__(self, vote_obj: Vote):
        super().__init__(vote_obj)
        self._lock = asyncio.Lock()

    async def add_vote(self, inter_id, target_id):
        async with self._lock:
            await asyncio.to_thread(self.vote_obj.add_vote, inter_id, target_id)

    async def remove_vote(self, inter_id):
        async with self._lock:
            await asyncio.to_thread(self.vote_obj.remove_vote, inter_id)
