from errors import PlayerErrors, VotingErrors


class VotersStorage:
    """Tracks voting status for each player"""

    def __init__(self, players: list[int]):
        self.players = {player_id: False for player_id in players}

    def set_voter_status(self, voter_id: int, status: bool):
        """Update a player's voting status.

        Args:
            voter_id: Player identifier
            status: True if voted, False if not

        Raises:
            PlayerErrors.PlayerNotFoundError: If player isn't a part of vote
        """
        if self.players[voter_id]:
            self.players[voter_id] = status
        else:
            raise PlayerErrors.PlayerNotFoundError()


class VotesStorage:
    """Stores and manages votes"""

    def __init__(self, players: list[int]):
        self.votes = {player_id: [] for player_id in players}

    def add_vote(self, inter_id, target_id):
        """Register a vote between players.

        Args:
            inter_id: Voter's ID
            target_id: Vote target ID

        Raises:
            VotingErrors.VotingPermissionError: If voter can't vote
            PlayerErrors.PlayerNotFoundError: If target isn't a part of vote
            VotingErrors.AlreadyVotedError: If duplicate vote
        """
        if not self.votes.get(inter_id):
            raise VotingErrors.VotingPermissionError()
        if not self.votes.get(target_id):
            raise PlayerErrors.PlayerNotFoundError()
        if inter_id in self.votes.get(target_id):
            raise VotingErrors.AlreadyVotedError()
        self.votes[target_id].append(inter_id)

    def remove_vote(self, inter_id):
        """Remove a vote if it exists.

        Args:
            inter_id: Voter's ID
            target_id: Vote target ID
        """
        for voters_list in self.votes.values():
            if inter_id in voters_list:
                voters_list.remove(inter_id)

    def get_votes(self):
        return self.votes

    def calculate_votes(self, votes: dict[int, list[int]]):
        return max(votes, key=lambda k: len(votes[k]))


class VotesManager:
    def __init__(self, players: list[int]):
        self.voters = VotersStorage(players)
        self.votes = VotesStorage(players)

    def add_vote(self, inter_id: int, target_id: int):
        self.votes.add_vote(inter_id, target_id)
        self.voters.set_voter_status(inter_id, True)

    def remove_vote(self, inter_id: int):
        self.votes.remove_vote(inter_id)
        self.voters.set_voter_status(inter_id, False)

    def vote_result(self):
        return self.votes.calculate_votes(self.votes.votes)
