# === Stage 9: Теги ===
# Project: BracketMaker
class TournamentTag:
    def __init__(self, name, slug=None):
        self.name = name
        self.slug = slug or name.lower().replace(" ", "-").replace("_", "-")

    def __repr__(self):
        return f"TournamentTag('{self.name}', '{self.slug}')"

    def __eq__(self, other):
        return isinstance(other, TournamentTag) and self.slug == other.slug

    def __hash__(self):
        return hash(self.slug)


class TournamentTagManager:
    def __init__(self):
        self._tags = {}
        self._tournament_tags = {}

    def add_tag(self, name, slug=None):
        slug = slug or name.lower().replace(" ", "-").replace("_", "-")
        if slug in self._tags:
            return self._tags[slug]
        tag = TournamentTag(name, slug)
        self._tags[slug] = tag
        return tag

    def remove_tag(self, slug):
        tag = self._tags.pop(slug, None)
        if tag is not None:
            self._tournament_tags = {
                t: tags for t, tags in self._tournament_tags.items()
                if slug not in tags
            }
        return tag is not None

    def get_tag(self, slug):
        return self._tags.get(slug)

    def add_tag_to_tournament(self, tournament, slug):
        tag = self._tags.get(slug)
        if tag is not None and slug not in tournament.tags:
            tournament.tags.append(slug)
            self._tournament_tags[tournament.id] = tournament.tags
        return tag

    def remove_tag_from_tournament(self, tournament, slug):
        if slug in tournament.tags:
            tournament.tags.remove(slug)
            self._tournament_tags[tournament.id] = tournament.tags
        return True

    def search_tags(self, query):
        query = query.lower()
        return sorted(
            [
                TournamentTag(name, slug)
                for slug, tag in self._tags.items()
                if query in tag.name.lower() or query in slug
            ],
            key=lambda t: t.name.lower()
        )

    def get_tournament_tags(self, tournament):
        return [
            self._tags.get(slug, TournamentTag(slug, slug))
            for slug in tournament.tags
        ]
