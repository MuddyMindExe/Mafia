class GeneralErrors:
    class Error(Exception):
        pass

    class ObjNotExists(Error):
        pass


class VotingErrors:
    class VotingError(Exception):
        pass

    class VoteNotFoundError(VotingError):
        pass

    class VotingPermissionError(VotingError):
        pass

    class VotingCantBeFinishedError(VotingError):
        pass

    class AlreadyVotedError(VotingError):
        pass


class PlayerErrors:
    class PlayerError(Exception):
        pass

    class PlayerNotFoundError(PlayerError):
        pass

    class ActionPermissionError(PlayerError):
        pass

    class SelfActionError(PlayerError):
        pass

    class TargetNotFoundError(PlayerError):
        pass

    class UnacceptableTargetError(PlayerError):
        pass

    class ActionDoneError(PlayerError):
        pass


class GameErrors:
    class GameError(Exception):
        pass

    class NotEnoughPlayersError(GameError):
        pass

    class TimeError(GameError):
        pass

    class NotReadyError(GameError):
        pass


class LobbyErrors:
    class LobbyError(Exception):
        pass

    class LobbyNotFoundError(LobbyError):
        pass
