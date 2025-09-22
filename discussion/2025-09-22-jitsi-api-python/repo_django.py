# yourapp/infrastructure/repo_django.py
"""
Django ORM adapter for the Repository interface.
Implements persistence for reactions and simple counters.
No business logic here—pure storage concerns.
"""

# from yourapp.domain.reactions import Repository  # interface
# from yourapp.domain.reactions import ReactionEvent, BaseReaction  # types (if needed)
# from yourapp.apps.reactions.models import ReactionModel, ReactionCounter  # your Django models

class DjangoRepository:  # Repository
    """Django-backed implementation of Repository."""

    def save_reaction(self, reaction):  # reaction: BaseReaction
        """Insert a row for the submitted reaction (audit/analytics)."""
        # pass
        return None

    def increment_counters(self, reaction):
        """Update per-room/per-speaker/per-reaction counters (atomic where needed)."""
        # pass
        return None

    def fetch_recent_for_aggregation(self, key):
        """Return recent reaction records matching an aggregation key/window."""
        # return []
        return None

    # Optional read-model helpers (could live in a separate Metrics adapter)
    def get_counts(self, room_id, window):
        """Return aggregated counts for dashboards/exports."""
        # return {}
        return None
