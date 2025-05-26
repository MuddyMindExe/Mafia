from errors import PlayerErrors, VotingErrors
import asyncio


class VotersStorage:
    """Tracks voting status for each player"""

    def __init__(self, players: list[int]):
        self.players = {player_id: False for player_id in players}
        self.not_voted_amt = len(self.players.keys())

    def set_voter_status(self, inter_id: int, status: bool) -> None:
        """Update a player's voting status.

        Args:
            inter_id: Player identifier
            status: True if voted, False if not
        """
        self.players[inter_id] = status


class VotesStorage:
    """Stores and manages votes"""

    def __init__(self, players: list[int]):
        self.votes = {player_id: [] for player_id in players}

    def add_vote(self, inter_id, target_id) -> None:
        """Register a vote between players.

        Args:
            inter_id: Voter's ID
            target_id: Vote target ID
        """
        self.votes[target_id].append(inter_id)

    def remove_vote(self, inter_id) -> None:
        """Remove a vote if it exists.

        Args:
            inter_id: Voter's ID
        """
        for voters_list in self.votes.values():
            if inter_id in voters_list:
                voters_list.remove(inter_id)

    def get_votes(self) -> dict[int, list]:
        return self.votes

    def calculate_votes(self) -> int:
        return max(self.votes, key=lambda k: len(self.votes[k]))


class VotesValidator:
    def __init__(self, voters: VotersStorage, votes: VotesStorage):
        self.voters = voters
        self.votes = votes

    def _player_participate(self, player_id) -> bool:
        return player_id in self.voters.players

    def _player_voted(self, player_id) -> bool:
        return self.voters.players.get(player_id)

    def validate_vote_add(self, inter_id: int, target_id: int):
        """Validate add operation.

        Args:
            inter_id: Voter's ID
            target_id: Target's ID

        Raises:
            PlayerErrors.PlayerNotFoundError: Voter/Target doesn't participate selected vote session
            VotingErrors.VotingPermissionError: Player has already voted
            PlayerErrors.SelfActionError: Self-voting attempt
        """
        if not self._player_participate(inter_id) or not self._player_participate(target_id):
            raise PlayerErrors.PlayerNotFoundError()
        if self._player_voted(inter_id):
            raise VotingErrors.AlreadyVotedError()
        if inter_id == target_id:
            raise PlayerErrors.SelfActionError()

    def validate_vote_remove(self, inter_id: int):
        """Validate remove operation.

        Args:
            inter_id: Voter's ID

        Raises:
            PlayerErrors.PlayerNotFoundError: Player doesn't participate selected vote session
            VotingErrors.VotingPermissionError: Player has already voted
        """
        if not self._player_participate(inter_id):
            raise PlayerErrors.PlayerNotFoundError()
        if not self._player_voted(inter_id):
            raise VotingErrors.VotingPermissionError()


class VotesManager:
    def __init__(self, players: list[int]):
        self.voters = VotersStorage(players)
        self.votes = VotesStorage(players)
        self.validator = VotesValidator(self.voters, self.votes)
        self._lock = asyncio.Lock()

    async def add_vote(self, inter_id: int, target_id: int) -> None | int:
        async with self._lock:
            self.validator.validate_vote_add(inter_id, target_id)
            self.votes.add_vote(inter_id, target_id)
            self.voters.set_voter_status(inter_id, True)
            self.voters.not_voted_amt -= 1
            if self.voters.not_voted_amt == 0:
                return await self.vote_result()

    async def remove_vote(self, inter_id: int) -> None:
        async with self._lock:
            self.validator.validate_vote_remove(inter_id)
            self.votes.remove_vote(inter_id)
            self.voters.set_voter_status(inter_id, False)
            self.voters.not_voted_amt += 1

    async def vote_result(self) -> int:
        async with self._lock:
            return self.votes.calculate_votes()
