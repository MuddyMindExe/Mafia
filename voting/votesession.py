import asyncio
from vote import Vote


class VoteSession:
    def add_vote(self, inter_id, target_id):
        raise NotImplementedError

    def remove_vote(self, inter_id):
        raise NotImplementedError


class AsyncVoteSession(VoteSession):
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

    async def find_player(self, target_id):
        await asyncio.to_thread(self.vote_obj.find_player(target_id))
