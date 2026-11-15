# === Stage 7: Текстовый поиск ===
# Project: BracketMaker
import re


def highlight_matches(text, needles):
    if not text:
        return text
    result = list(text)
    for needle in needles:
        if not needle:
            continue
        pattern = re.escape(needle)
        regex = re.compile(pattern, re.IGNORECASE)
        for match in regex.finditer(text):
            start = match.start()
            end = match.end()
            for index in range(start, end):
                if result[index] == text[index]:
                    result[index] = "\033[7m" + result[index] + "\033[0m"
    return "".join(result)


def render_bracket_table(tournaments):
    rows = []
    for tournament in tournaments:
        title = tournament.get("title", "")
        status = tournament.get("status", "")
        seed = tournament.get("seed", "")
        participants = tournament.get("participants", [])
        needles = []
        if title:
            needles.append(title.lower())
        if status:
            needles.append(status.lower())
        if seed:
            needles.append(seed.lower())
        highlighted_title = highlight_matches(title, needles)
        highlighted_status = highlight_matches(status, needles)
        highlighted_seed = highlight_matches(seed, needles)
        participant_line = ", ".join(
            highlight_matches(str(participant), needles) for participant in participants
        )
        rows.append([highlighted_title, status, highlighted_seed, participant_line])
    return rows
