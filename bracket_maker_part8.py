# === Stage 8: Поиск по нескольким словам ===
# Project: BracketMaker
def normalize_token(token):
    return token.strip().lower()


def split_query(query):
    tokens = []
    for raw in query.replace('"', ' ').split():
        if raw.startswith('-'):
            tokens.append(('exclude', normalize_token(raw[1:])))
        else:
            tokens.append(('include', normalize_token(raw)))
    return tokens


def _match_includes(record, includes):
    haystack = set(record.get('name', '').lower().split())
    if includes:
        return all(word in haystack for word in includes)
    return True


def _match_excludes(record, excludes):
    haystack = set(record.get('name', '').lower().split())
    if excludes:
        return not any(word in haystack for word in excludes)
    return True


def search_tournaments(query, tournaments):
    tokens = split_query(query)
    includes = [t for t in tokens if t[0] == 'include']
    excludes = [t for t in tokens if t[0] == 'exclude']
    results = []
    for record in tournaments:
        if _match_includes(record, includes) and _match_excludes(record, excludes):
            results.append(record)
    return results


if __name__ == '__main__':
    examples = [
        {'name': 'Spring Open Cup', 'format': 'single'},
        {'name': 'Fall Grand Slam', 'format': 'double'},
        {'name': 'Summer Championship', 'format': 'single'},
        {'name': 'Winter Masters', 'format': 'triple'},
    ]
    print(search_tournaments('championship -winter', examples))
    print(search_tournaments('spring -open', examples))
    print(search_tournaments('spring open', examples))
    print(search_tournaments('', examples))
