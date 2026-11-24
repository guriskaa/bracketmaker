# === Stage 11: Поиск дубликатов ===
# Project: BracketMaker
def normalize(value):
    if value is None:
        return ""
    return str(value).strip().lower()


def normalize_name(value):
    return normalize(value).replace(" ", "").replace("ё", "е").replace("ё", "е")


def normalize_format(value):
    if not value:
        return ""
    text = normalize(value)
    mapping = {
        "single": "single",
        "single elimination": "single",
        "double elimination": "double",
        "double-elimination": "double",
        "swiss": "swiss",
        "round robin": "roundrobin",
        "round-robin": "roundrobin",
        "singles": "single",
        "singles elimination": "single",
    }
    return mapping.get(text, text)


def normalize_status(value):
    if not value:
        return ""
    text = normalize(value)
    mapping = {
        "open": "open",
        "open bracket": "open",
        "closed": "closed",
        "finalized": "closed",
        "in progress": "in_progress",
        "in-progress": "in_progress",
        "upcoming": "upcoming",
        "pending": "upcoming",
    }
    return mapping.get(text, text)


def normalize_participants(value):
    if value is None:
        return 0
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return 0


def normalize_title(value):
    return normalize_name(value)


def normalize_fields(tournament):
    return {
        "title": normalize_title(getattr(tournament, "title", None)),
        "format": normalize_format(getattr(tournament, "format", None)),
        "participants": normalize_participants(getattr(tournament, "participants", None)),
        "status": normalize_status(getattr(tournament, "status", None)),
    }


def build_key(tournament):
    fields = normalize_fields(tournament)
    return (fields["title"], fields["format"], fields["participants"], fields["status"])


def normalize_tournament(tournament):
    return normalize_fields(tournament)


def find_duplicates(tournaments):
    if not tournaments:
        return []
    seen = {}
    for tournament in tournaments:
        key = build_key(tournament)
        if key not in seen:
            seen[key] = []
        seen[key].append(tournament)
    duplicates = [group for group in seen.values() if len(group) > 1]
    return duplicates


def find_duplicates_by_fields(tournaments, fields_fn=normalize_fields):
    if not tournaments:
        return []
    seen = {}
    for tournament in tournaments:
        key = tuple(fields_fn(tournament).items())
        if key not in seen:
            seen[key] = []
        seen[key].append(tournament)
    duplicates = [group for group in seen.values() if len(group) > 1]
    return duplicates
