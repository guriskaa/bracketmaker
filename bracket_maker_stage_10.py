# === Stage 10: Быстрые фильтры ===
# Project: BracketMaker
import datetime

TODAY = datetime.date.today()


def _parse_date(value):
    try:
        return datetime.date.fromisoformat(value.strip())
    except (ValueError, AttributeError):
        return None


def _match_date_range(day):
    start = TODAY + datetime.timedelta(days=day)
    end = start + datetime.timedelta(days=6)
    return lambda start_date: start <= start_date <= end


def is_today(start_date):
    return start_date == TODAY


def is_this_week(start_date):
    return _match_date_range(0)(start_date)


def is_due_this_week(start_date):
    return _match_date_range(7)(start_date)


def is_overdue(start_date):
    return start_date < TODAY


def filter_tournaments_by_date(tournaments, day=None):
    if day is None:
        return tournaments
    predicate = {
        "today": is_today,
        "this_week": is_this_week,
        "due_this_week": is_due_this_week,
        "overdue": is_overdue,
    }.get(day)
    if predicate is None:
        raise ValueError(f"Неизвестный фильтр: {day!r}")
    return [t for t in tournaments if predicate(_parse_date(t.get("start_date")))]


def build_tournament_filters():
    return {
        "today": filter_tournaments_by_date,
        "this_week": filter_tournaments_by_date,
        "due_this_week": filter_tournaments_by_date,
        "overdue": filter_tournaments_by_date,
    }
