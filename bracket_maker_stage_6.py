# === Stage 6: Связанная сущность ===
# Project: BracketMaker
from datetime import datetime

MATCH_STATUS = ("pending", "scheduled", "completed", "cancelled")


class Match:
    def __init__(self, tournament, round_name, seed_a, seed_b,
                 status="pending", winner=None, score=None,
                 scheduled_at=None):
        self.tournament = tournament
        self.round_name = round_name
        self.seed_a = seed_a
        self.seed_b = seed_b
        self.status = status
        self.winner = winner
        self.score = score
        self.scheduled_at = scheduled_at or datetime.now()

    def set_result(self, winner, score=None):
        if self.status in ("completed", "cancelled"):
            raise ValueError("нельзя менять результат завершённого матча")
        self.winner = winner
        self.score = score
        self.status = "completed"

    def cancel(self):
        if self.status == "completed":
            raise ValueError("нельзя отменить завершённый матч")
        self.status = "cancelled"

    def is_finished(self):
        return self.status in ("completed", "cancelled")

    def to_dict(self):
        return {
            "round": self.round_name,
            "seed_a": self.seed_a,
            "seed_b": self.seed_b,
            "status": self.status,
            "winner": self.winner,
            "score": self.score,
            "scheduled_at": self.scheduled_at.isoformat(),
        }


def add_match(tournament, round_name, seed_a, seed_b,
              status="pending", winner=None, score=None,
              scheduled_at=None):
    if status not in MATCH_STATUS:
        raise ValueError(f"недопустимый статус матча: {status}")
    if status == "completed" and winner is None:
        raise ValueError("для завершённого матча нужен победитель")
    if tournament is None:
        raise ValueError("нельзя добавить матч без турнира")
    if seed_a == seed_b:
        raise ValueError("нельзя поставить одного участника в обоих матчах")
    return Match(
        tournament, round_name, seed_a, seed_b,
        status=status, winner=winner, score=score,
        scheduled_at=scheduled_at,
    )


def get_match(tournament, round_name, seed_a, seed_b):
    return next(
        (m for m in tournament.matches
           if m.round_name == round_name
           and m.seed_a == seed_a and m.seed_b == seed_b),
        None,
    )


def update_match_result(match, winner, score=None):
    match.set_result(winner, score)
    return match


def cancel_match(match):
    match.cancel()
    return match


def list_matches(tournament):
    return [m.to_dict() for m in tournament.matches]
