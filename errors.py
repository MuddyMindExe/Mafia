class VotingErrors:
    class VotingError(Exception):
        pass

    class AlreadyVotedError(VotingError):
        pass

    class HostVotingError(VotingError):
        pass

    class SelfVotingError(VotingError):
        pass


class ActionErrors:
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

    class TimeError(GameError):
        pass
