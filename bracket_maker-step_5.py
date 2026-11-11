# === Stage 5: Удаление и восстановление ===
# Project: BracketMaker
import uuid


class Tournament:
    def __init__(self, name, format, participants, status="active"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.format = format
        self.participants = participants
        self.status = status

    def __repr__(self):
        return f"Tournament(id={self.id}, name={self.name!r}, status={self.status!r})"


class SoftDeleteManager:
    def __init__(self):
        self.deleted = []
        self.active = []

    def add(self, tournament):
        self.active.append(tournament)

    def remove(self, tournament):
        if tournament not in self.active:
            return False
        self.active.remove(tournament)
        self.deleted.append(tournament)
        tournament.status = "deleted"
        return True

    def restore(self, tournament):
        if tournament not in self.deleted:
            return False
        self.deleted.remove(tournament)
        self.active.append(tournament)
        tournament.status = "active"
        return True

    def is_deleted(self, tournament):
        return tournament in self.deleted

    def is_active(self, tournament):
        return tournament in self.active
