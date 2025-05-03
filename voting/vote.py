from abc import ABC, abstractmethod
from votestorage import VotesManager


class Vote(ABC):
    """Abstract base class for voting systems"""

    def __init__(self, host_id: int, votes_manager: VotesManager):
        self.host_id = host_id
        self.votes_manager = votes_manager

    @abstractmethod
    def add_vote(self, inter_id, target_id) -> None: ...

    @abstractmethod
    def remove_vote(self, inter_id) -> None: ...

    @abstractmethod
    def vote_result(self) -> list[int]: ...


class VoteKick(Vote):
    """Implementation for kick voting system"""

    def __init__(self, host_id: int, votes_manager: VotesManager):
        super().__init__(host_id, votes_manager)

    def add_vote(self, inter_id: int, target_id: int):
        self.votes_manager.add_vote(inter_id, target_id)

    def remove_vote(self, inter_id: int):
        self.votes_manager.remove_vote(inter_id)

    def vote_result(self):
        return self.votes_manager.vote_result()


class VoteCreator:
    """Vote constructor"""

    def __init__(self, host_id, players: list):
        self.host_id = host_id
        self.votes_manager = VotesManager(players)

    def create(self) -> VoteKick:
        return VoteKick(self.host_id, self.votes_manager)
