# yourapp/infrastructure/directory_cache.py
"""
Directory adapter backed by a cache (e.g., Redis).
Holds transient mappings: user <-> jitsi participant IDs, current speaker,
facilitators list, and room rosters.
"""

# import typing as t
# from django.core.cache import cache
# from yourapp.domain.reactions import JitsiDirectory

class DirectoryCache:  # JitsiDirectory
    """Cache-backed implementation of JitsiDirectory."""

    # ---- lookups required by the interface ----

    def current_speaker(self, room_id):
        """Return the participant_id of the current speaker, if any."""
        # return cache.get(f"room:{room_id}:speaker")
        return None

    def facilitators(self, room_id):
        """Return a list of participant_ids who are facilitators."""
        # return cache.get(f"room:{room_id}:facilitators") or []
        return None

    def participant_ids(self, room_id):
        """Return the list of participant_ids currently in the room."""
        # return cache.get(f"room:{room_id}:participants") or []
        return None

    # ---- optional helpers (called by your WS consumer) ----

    def register_presence(self, room_id, user_id, display_name, participant_id, role):
        """Write a presence record when a client handshakes."""
        # pass
        return None

    def set_current_speaker(self, room_id, participant_id):
        """Update current speaker per dominantSpeakerChanged."""
        # pass
        return None

    def set_facilitators(self, room_id, participant_ids):
        """Update facilitator roster."""
        # pass
        return None

    def remove_participant(self, room_id, participant_id):
        """Cleanup on disconnect."""
        # pass
        return None
