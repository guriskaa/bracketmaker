# === Stage 12: Массовое обновление ===
# Project: BracketMaker
from typing import List, Dict, Callable, Any, Optional


class BracketMaker:
    # Массовое обновление выбранных турниров по условию с предварительным
    # просмотром изменений. Работает с коллекцией турниров, которые должны
    # определять метод set_status для применения обновления.

    def __init__(self, tournaments: List[Dict[str, Any]]):
        self._tournaments = list(tournaments)

    def set_tournaments(self, tournaments: List[Dict[str, Any]]) -> None:
        self._tournaments = list(tournaments)

    def get_tournaments(self) -> List[Dict[str, Any]]:
        return list(self._tournaments)

    def get_tournament(self, key: str) -> Optional[Dict[str, Any]]:
        for tournament in self._tournaments:
            if tournament.get("id") == key:
                return tournament
        return None

    def has_tournament(self, key: str) -> bool:
        return self.get_tournament(key) is not None

    def find_matching_tournaments(self, predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        return [tournament for tournament in self._tournaments if predicate(tournament)]

    def preview_changes(self, predicate: Callable[[Dict[str, Any]], bool],
                        updater: Callable[[Dict[str, Any]], Any]) -> List[Dict[str, Any]]:
        return [
            {
                "id": tournament.get("id"),
                "name": tournament.get("name"),
                "format": tournament.get("format"),
                "status": tournament.get("status"),
                "field": "status",
                "from": tournament.get("status"),
                "to": updater(tournament),
            }
            for tournament in self.find_matching_tournaments(predicate)
        ]

    def apply_changes(self, predicate: Callable[[Dict[str, Any]], bool],
                      updater: Callable[[Dict[str, Any]], Any]) -> List[Dict[str, Any]]:
        applied = []
        for tournament in self.find_matching_tournaments(predicate):
            new_value = updater(tournament)
            if "status" in tournament and new_value is not None:
                tournament["status"] = new_value
                applied.append({
                    "id": tournament.get("id"),
                    "name": tournament.get("name"),
                    "field": "status",
                    "from": None,
                    "to": new_value,
                })
        return applied
