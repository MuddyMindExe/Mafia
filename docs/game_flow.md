# game flow

## Life-cycle

- Lobby is created by Host
- Players join Lobby
- Host starts game

---

### Transition: Lobby → Game

Condition:
- Host starts game
- All requirements are satisfied

Result:
- Lobby is destroyed
- Game is created

## 2. Game Rules

### Start Requirements

- Minimum players: 3
- Minimum mafia: 1

### Invariants

- Game always has a Host
- Game always has at least 3 players (after start)

___

## 3. State Machine

Lobby → Game →Finished Game

Allowed transitions:
- Lobby → Game

Forbidden:
- Game → Lobby

___

## 4. Implementation Notes (optional section)

This section describes current code behaviour.

- Lobby stored in mafia.game.gl.LobbyStorage.lobbies (dict)
- Game stored in mafia.game.gl.GameStorage.games (dict)
- Keys: host_id (int)

Lobby removal:
- Happens during Game creation
- Happens if Host left the game (not implemented)

Game removal:
- Happens after game logical end
- Happens if Host left the game (not implemented)
