# === Stage 4: Редактирование записей ===
# Project: BracketMaker
import re

ALLOWED_TOURNAMENT_FIELDS = {
    "name",
    "format",
    "participants",
    "status",
}

FIELD_NAME = "name"
FIELD_FORMAT = "format"
FIELD_PARTICIPANTS = "participants"
FIELD_STATUS = "status"

STATUS_VALUES = ("open", "in_progress", "finished")

BRACKET_TYPES = ("round_robin", "single_elimination", "double_elimination", "swiss")


def validate_tournament_update(payload):
    if not isinstance(payload, dict):
        return False, "payload должен быть словарем"

    changed = set(payload.keys())
    unknown = changed - ALLOWED_TOURNAMENT_FIELDS
    if unknown:
        return False, f"неизвестные поля: {', '.join(sorted(unknown))}"

    name = payload.get(FIELD_NAME)
    if name is not None:
        if not isinstance(name, str) or not re.match(r"^\S+$", name):
            return False, "поле name: должно быть непустой строкой без пробелов"
        payload[FIELD_NAME] = name

    fmt = payload.get(FIELD_FORMAT)
    if fmt is not None:
        if not isinstance(fmt, str) or fmt not in BRACKET_TYPES:
            return False, f"поле format: допустимые значения {', '.join(BRACKET_TYPES)}"
        payload[FIELD_FORMAT] = fmt

    parts = payload.get(FIELD_PARTICIPANTS)
    if parts is not None:
        if not isinstance(parts, int) or parts < 0 or parts > 1024:
            return False, "поле participants: целое число от 0 до 1024"
        payload[FIELD_PARTICIPANTS] = parts

    status = payload.get(FIELD_STATUS)
    if status is not None:
        if not isinstance(status, str) or status not in STATUS_VALUES:
            return False, f"поле status: допустимые значения {', '.join(STATUS_VALUES)}"
        payload[FIELD_STATUS] = status

    return True, "ok"
