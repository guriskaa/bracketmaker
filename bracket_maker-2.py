# === Stage 2: Проверка полей ===
# Project: BracketMaker
import re


BRACKET_STATUSES = ("открыт", "идёт", "завершён")
BRACKET_FORMATS = ("single", "double", "consolation")


def normalize_text(value):
    text = value.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_status(value):
    normalized = normalize_text(value).lower()
    for option in BRACKET_STATUSES:
        if normalized == option:
            return option
    return None


def normalize_format(value):
    normalized = normalize_text(value).lower()
    for option in BRACKET_FORMATS:
        if normalized == option:
            return option
    return None


def normalize_participants(value):
    raw = value.strip()
    if not raw:
        return []
    parts = [chunk.strip() for chunk in re.split(r"[,;]", raw)]
    participants = []
    for chunk in parts:
        if not chunk:
            continue
        participants.append(normalize_text(chunk))
    participants = [participant for participant in participants if participant]
    return participants


def validate_tournament(name, fmt, participants, status):
    errors = []
    if not name or not name.strip():
        errors.append("Название турнира не может быть пустым.")
    else:
        name = normalize_text(name)
        if len(name) > 100:
            errors.append("Название турнира не должно превышать 100 символов.")

    fmt = normalize_format(fmt)
    if fmt is None:
        errors.append(
            "Формат турнира должен быть одним из: single, double, consolation."
        )

    participants = normalize_participants(participants)
    if not participants:
        errors.append("Турнир должен содержать хотя бы одного участника.")
    elif len(participants) > 512:
        errors.append("Максимальное число участников — 512.")
    elif len(participants) != len(set(participants)):
        errors.append("Участники должны быть уникальными.")

    status = normalize_status(status)
    if status is None:
        errors.append(
            "Статус турнира должен быть одним из: открыт, идёт, завершён."
        )

    return errors
