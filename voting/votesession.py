import asyncio
from voting.vote import Vote
from abc import ABC, abstractmethod


class AsyncVoteSession(ABC):
    @abstractmethod
    async def add_vote(self, inter_id: int, target_id: int) -> None: ...

    @abstractmethod
    async def remove_vote(self, inter_id: int) -> None: ...


class VoteSession(AsyncVoteSession):
    def __init__(self, vote_obj: Vote):
        self.vote_obj = vote_obj

    async def add_vote(self, inter_id, target_id):
        await asyncio.to_thread(self.vote_obj.add_vote, inter_id, target_id)

    async def remove_vote(self, inter_id):
        await asyncio.to_thread(self.vote_obj.remove_vote, inter_id)
