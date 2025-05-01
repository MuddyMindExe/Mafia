import asyncio
from vote import Vote
from abc import ABC, abstractmethod


class AsyncVoteSession(ABC):
    @abstractmethod
    def add_vote(self, inter_id, target_id):
        raise NotImplementedError

    @abstractmethod
    def remove_vote(self, inter_id):
        raise NotImplementedError


class VoteSession(AsyncVoteSession):
    def __init__(self, vote_obj: Vote):
        self.vote_obj = vote_obj
        self.voters = self.vote_obj.voters
        self.votes = self.vote_obj.votes
        self._lock = asyncio.Lock()

    async def add_vote(self, inter_id, target_id):
        async with self._lock:
            await asyncio.to_thread(self.vote_obj.add_vote, inter_id, target_id)

    async def remove_vote(self, inter_id):
        async with self._lock:
            await asyncio.to_thread(self.vote_obj.remove_vote, inter_id)
