from errors import VotingErrors
from abc import ABC, abstractmethod
from votestorage import VotersStorage, VotesStorage


class Vote(ABC):
    def __init__(self, host_id: int, players):
        self.host_id = host_id
        self.voters = VotersStorage(players)
        self.votes = VotesStorage()

    @abstractmethod
    def add_vote(self, inter_id, target_id):
        pass

    @abstractmethod
    def remove_vote(self, inter_id):
        pass

    @abstractmethod
    def find_player(self, target_id):
        pass

    @abstractmethod
    def vote_result(self):
        pass


class VoteKick(Vote):
    def __init__(self, host_id: int, players):
        super().__init__(host_id, players)

    def add_vote(self, inter_id: int, target_id: int):
        self.votes.add_vote(inter_id, target_id)
        self.voters.add_voter(inter_id)

    def remove_vote(self, inter_id: int):
        self.votes.remove_vote(inter_id)
        self.voters.remove_voter(inter_id)

    def find_player(self, target_id):
        return any(target_id in group for group in [self.voters.voters, self.voters.players])

    def vote_result(self):
        return self.votes.calculate_votes()

    def finish_ready(self):
        return not self.voters.get_players()


class ValidatingVotes:
    def __init__(self, host_id):
        self.host_id = host_id

    def permission_validate(self, players, inter_id, target_id=None):
        if inter_id == self.host_id or inter_id not in players or inter_id == target_id:
            raise VotingErrors.VotingPermissionError()
