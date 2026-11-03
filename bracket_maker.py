# === Stage 1: Каркас модуля ===
# Project: BracketMaker
bracketmaker_tournament.py

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class TournamentFormat(str, Enum):
    SINGLE_ELIMINATION = "single_elimination"
    DOUBLE_ELIMINATION = "double_elimination"
    ROUND_ROBIN = "round_robin"


class TournamentStatus(str, Enum):
    DRAFTING = "drafting"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


@dataclass(frozen=True)
class Tournament:
    title: str
    format: TournamentFormat
    participants: tuple[str, ...] = ()
    status: TournamentStatus = TournamentStatus.DRAFTING

    def with_participants(self, participants: Iterable[str]) -> "Tournament":
        return Tournament(
            title=self.title,
            format=self.format,
            participants=tuple(participants),
            status=self.status,
        )


def demo_tournaments() -> List[Tournament]:
    return [
        Tournament(
            title="Open Cup 2024",
            format=TournamentFormat.SINGLE_ELIMINATION,
            participants=("Alice", "Bob", "Carol", "Dave"),
            status=TournamentStatus.IN_PROGRESS,
        ),
        Tournament(
            title="Weekend Blitz",
            format=TournamentFormat.ROUND_ROBIN,
            participants=("Eve", "Frank"),
            status=TournamentStatus.DRAFTING,
        ),
    ]


def main() -> None:
    for tournament in demo_tournaments():
        print(tournament.title)
        print(tournament.format.value)
        print(tournament.status.value)
        print(tournament.participants)


if __name__ == "__main__":
    main()
