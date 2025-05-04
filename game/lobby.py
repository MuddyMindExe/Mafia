from game.game import Game, GameCreator, Mafia, Sherif, Doc, Citizen
import random
from errors import GameErrors


class Lobby:
    def __init__(self, host_id, time, mafia_amt, doc_amt, sherif_amt):
        self.host_id       = host_id
        self.time       = time
        self.players    = set()
        self.mafia_amt  = mafia_amt
        self.sherif_amt = sherif_amt
        self.doc_amt    = doc_amt
        self.game       = GameCreator().set_host(self.host_id).set_time(self.time)
        self.min_players_amt = self.mafia_amt + self.sherif_amt + self.doc_amt + 2

    def add_player(self, player_id):
        self.players.add(player_id)
        return self

    def remove_player(self, player_id):
        self.players.discard(player_id)
        return self

    def create_game(self) -> Game:
        if len(self.players) < self.min_players_amt:
            raise GameErrors.NotEnoughPlayersError()
        players = self.role_assignment()
        self.game.set_players(players).build()
        return self.game

    def role_assignment(self) -> dict:
        mafia   = {key: Mafia()   for key in self.__role_assign(self.mafia_amt)}
        sherif  = {key: Sherif()  for key in self.__role_assign(self.sherif_amt)}
        doc     = {key: Doc()     for key in self.__role_assign(self.doc_amt)}
        citizen = {key: Citizen() for key in self.players}
        return mafia | sherif | doc | citizen

    def __role_assign(self, amt: int) -> list:  # **
        chosen = random.sample(list(self.players), amt)
        for el in chosen:
            self.players.remove(el)
        return chosen

    def __repr__(self):
        return f"\nhost_id: {self.host_id}\ntime: {self.time}\nplayers: {self.players}\n" \
               f"mafia_amt: {self.mafia_amt}\ndoc_amt: {self.doc_amt}\nsherif_amt: {self.sherif_amt}\n"
