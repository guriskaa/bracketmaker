# === Stage 3: Хранилище в памяти ===
# Project: BracketMaker
import uuid


class TournamentStore:
    def __init__(self):
        self._tournaments = {}

    def add(self, tournament):
        if tournament.id is None:
            tournament.id = uuid.uuid4().hex
        self._tournaments[tournament.id] = tournament
        return tournament

    def get(self, tournament_id):
        return self._tournaments.get(tournament_id)

    def list(self):
        return list(self._tournaments.values())


class Tournament:
    def __init__(self, name, format, participants, status):
        self.id = None
        self.name = name
        self.format = format
        self.participants = participants
        self.status = status


if __name__ == "__main__":
    store = TournamentStore()
    t1 = Tournament("Чемпионат", "single", 8, "drafting")
    store.add(t1)
    t2 = Tournament("Открытый", "double", 16, "open")
    store.add(t2)
    print(store.get(t1.id).name)
    print(len(store.list()))
