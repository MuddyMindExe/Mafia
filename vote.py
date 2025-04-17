import threading
from datahandler import DataHandler
from errors import VotingErrors


class Vote:
    def __init__(self, host_id: int, players: list[int]):
        self.host_id = host_id
        self.voters_storage = VotersStorage(players)
        self.votes = Votes()
        self.validator = ValidatingVotes(self.host_id)
        self.vote_finish = threading.Event()

    def add_vote(self, inter_id: int, target_id: int):
        try:
            self.validator.permission_validate(self.voters_storage.players, inter_id, target_id)
            self.votes.add_vote(inter_id, target_id)
            self.voters_storage.add_voter(inter_id)
            return True
        except VotingErrors.VotingPermissionError:
            return False

    def remove_vote(self, inter_id: int):
        try:
            self.validator.permission_validate(self.voters_storage.voters, inter_id)
            self.votes.remove_vote(inter_id)
            self.voters_storage.remove_voter(inter_id)
            return True
        except VotingErrors.VotingPermissionError:
            return False

    def finish_vote(self):
        self.vote_finish.wait()
        target = self.votes.calculate_votes()
        return target
    

class VotersStorage:
    def __init__(self, players: list):
        self.players = players
        self.voters = []

    def add_voter(self, voter_id):
        self.voters.append(voter_id)
        self.players.remove(voter_id)

    def remove_voter(self, voter_id):
        self.voters.remove(voter_id)
        self.players.append(voter_id)


class ValidatingVotes:
    def __init__(self, host_id):
        self.host_id = host_id

    def permission_validate(self, players, inter_id, target_id=None):
        if inter_id == self.host_id or inter_id not in players or inter_id == target_id:
            raise VotingErrors.VotingPermissionError()

    def is_finish_ready_validate(self, players, event: threading.Event):
        if not players:
            event.set()


class Votes:
    def __init__(self):
        self.votes: dict[int, list] = {}

    def add_vote(self, inter_id, target_id):
        if not self.votes.get(target_id):
            self.votes[target_id] = [inter_id]
        else:
            self.votes[target_id].append(inter_id)

    def remove_vote(self, inter_id):
        for votes_list in self.votes.values():
            if inter_id in votes_list:
                votes_list.remove(inter_id)

    def calculate_votes(self):
        return DataHandler.calculate_keys(self.votes)
