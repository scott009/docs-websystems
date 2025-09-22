# tests/conftest.py
"""
Pytest wiring for domain-only tests (no Django required).
Provides fake adapters and common fixtures to test reactions.py in isolation.
"""

import pytest

# Adjust this import to your project layout:
# from yourapp.domain.reactions import (
#     ReactionService, VisibilityMode, ReactionCode,
#     Policy, Repository, Broadcaster, JitsiDirectory,
# )

# ---- Fake adapters (no logic, just shape-compatible) -------------------------

class FakePolicy:  # Policy
    """No-op policy; override in tests as needed."""
    def validate(self, reaction, room_state):  # pragma: no cover - stub
        return None

    def redact_sender(self, reaction_event):  # pragma: no cover - stub
        return reaction_event

    def rate_limit_key(self, reaction):  # pragma: no cover - stub
        return None

    def aggregate_key(self, reaction):  # pragma: no cover - stub
        return None


class FakeRepository:  # Repository
    """In-memory sink for persistence assertions."""
    def __init__(self):
        self.saved = []
        self.counters = []

    def save_reaction(self, reaction):  # pragma: no cover - stub
        self.saved.append(reaction)

    def increment_counters(self, reaction):  # pragma: no cover - stub
        self.counters.append(reaction)

    def fetch_recent_for_aggregation(self, key):  # pragma: no cover - stub
        return []

    # Optional read-model helper for tests
    def get_counts(self, room_id, window):  # pragma: no cover - stub
        return {}


class FakeBroadcaster:  # Broadcaster
    """Captures outbound events for assertions."""
    def __init__(self):
        self.to_all = []
        self.to_pid = []
        self.to_fac = []

    def send_to_all(self, room_id, event):  # pragma: no cover - stub
        self.to_all.append((room_id, event))

    def send_to_participant(self, room_id, participant_id, event):  # pragma: no cover - stub
        self.to_pid.append((room_id, participant_id, event))

    def send_to_facilitators(self, room_id, event):  # pragma: no cover - stub
        self.to_fac.append((room_id, event))


class FakeDirectory:  # JitsiDirectory
    """Deterministic mappings for tests."""
    def __init__(self):
        self._speaker = "pid-speaker"
        self._facilitators = ["pid-fac-1"]
        self._participants = ["pid-speaker", "pid-fac-1", "pid-111", "pid-222"]

    def current_speaker(self, room_id):  # pragma: no cover - stub
        return self._speaker

    def facilitators(self, room_id):  # pragma: no cover - stub
        return list(self._facilitators)

    def participant_ids(self, room_id):  # pragma: no cover - stub
        return list(self._participants)

    # Optional mutators for specific tests
    def set_current_speaker(self, pid):  # pragma: no cover - stub
        self._speaker = pid

    def set_facilitators(self, pids):  # pragma: no cover - stub
        self._facilitators = list(pids)


class FakeRoomState:
    """Minimal snapshot; expand as needed in tests."""
    pass


# ---- Common fixtures ---------------------------------------------------------

@pytest.fixture
def policy():
    return FakePolicy()

@pytest.fixture
def repo():
    return FakeRepository()

@pytest.fixture
def broadcaster():
    return FakeBroadcaster()

@pytest.fixture
def directory():
    return FakeDirectory()

@pytest.fixture
def room_state():
    return FakeRoomState()

@pytest.fixture
def service(policy, repo, broadcaster, directory):
    """
    Build the domain service with fakes.
    Replace the return with a real ReactionService() when implemented.
    """
    # return ReactionServic
