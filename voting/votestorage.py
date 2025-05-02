from datahandler import DataHandler
from errors import PlayerErrors, VotingErrors


class VotersStorage:
    def __init__(self, players: list):
        self.players = {player_id: False for player_id in players}

    def set_voter_status(self, voter_id: int, status: bool):
        if self.players[voter_id]:
            self.players[voter_id] = status
        else:
            raise PlayerErrors.PlayerNotFoundError()


class VotesStorage:
    def __init__(self, player_ids: list[int]):
        self.votes = {player_id: [] for player_id in player_ids}

    def add_vote(self, inter_id, target_id):
        if not self.votes.get(inter_id):
            raise VotingErrors.VotingPermissionError()
        if not self.votes.get(target_id):
            raise PlayerErrors.PlayerNotFoundError()
        if inter_id in self.votes.get(target_id):
            raise VotingErrors.AlreadyVotedError()
        self.votes[target_id].append(inter_id)

    def remove_vote(self, inter_id):
        for votes_list in self.votes.values():
            if inter_id in votes_list:
                votes_list.remove(inter_id)

    def get_votes(self):
        return self.votes

    def calculate_votes(self):
        return DataHandler.calculate_keys(self.votes)
