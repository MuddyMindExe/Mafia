from datahandler import DataHandler


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

    def get_players(self):
        return self.players

    def get_voters(self):
        return self.voters


class VotesStorage:
    def __init__(self):
        self.votes: dict[int, list[int]] = {}

    def add_vote(self, inter_id, target_id):
        if not self.votes.get(target_id):
            self.votes[target_id] = [inter_id]
        else:
            self.votes[target_id].append(inter_id)

    def remove_vote(self, inter_id):
        for votes_list in self.votes.values():
            if inter_id in votes_list:
                votes_list.remove(inter_id)

    def get_votes(self):
        return self.votes

    def calculate_votes(self):
        return DataHandler.calculate_keys(self.votes)
