from vote import Vote
from errors import VotingErrors


class VoteValidator:
    def __init__(self, vote: Vote):
        self.vote = vote

    def add_vote(self, inter_id: int, target_id: int):
        self.vote.add_vote(inter_id, target_id)

    def remove_vote(self, inter_id: int):
        self.vote.remove_vote(inter_id)

    def wait_and_finish(self):
        return self.vote.vote_result()
sadaadsa