# airtime.py
"""
Stubs only. No logic/implementation.
Domain models for airtime tracking and allocation in InquiryCircle meetings.
"""

# from datetime import datetime, timedelta
# from enum import Enum
# from dataclasses import dataclass
# from typing import Protocol

# ─────────────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────────────

class EnforcementLevel:  # Enum
    """Level of enforcement for airtime rules"""
    # ADVISORY = "advisory"      # Stats only, no control
    # SOFT = "soft"              # Warnings and prompts
    # HARD = "hard"              # Auto-mute when time expires
    pass


class MeetingType:  # Enum
    """Type of meeting for duration calculation"""
    # SCHEDULED = "scheduled"    # Has defined start/end time
    # ADHOC = "adhoc"           # Duration calculated retrospectively
    pass


# ─────────────────────────────────────────────────────────────────────
# Value Objects
# ─────────────────────────────────────────────────────────────────────

# @dataclass
class TimeAllocation:
    """Represents time allocated to a participant"""
    # participant_id: str
    # allocated_seconds: int
    # used_seconds: int = 0
    # borrowed_seconds: int = 0    # Time borrowed from others
    # lent_seconds: int = 0        # Time lent to others

    # def remaining_seconds(self) -> int:
    #     """Calculate remaining speaking time"""
    #     pass

    # def is_exhausted(self) -> bool:
    #     """Check if participant has used all their time"""
    #     pass

    # def to_dict(self) -> dict:
    #     pass
    pass


# @dataclass
class SpeakingSession:
    """Represents a single speaking session by a participant"""
    # participant_id: str
    # started_at: datetime
    # ended_at: datetime | None = None
    # duration_seconds: int = 0

    # def end_session(self) -> int:
    #     """End session and calculate duration"""
    #     pass

    # def to_dict(self) -> dict:
    #     pass
    pass


# @dataclass
class MeetingContext:
    """Context information about the meeting"""
    # room_id: str
    # meeting_type: MeetingType
    # start_time: datetime
    # end_time: datetime | None
    # facilitator_id: str
    # participant_ids: list[str]

    # def duration_seconds(self) -> int | None:
    #     """Calculate meeting duration (None for ongoing adhoc)"""
    #     pass

    # def is_ongoing(self) -> bool:
    #     pass

    # def to_dict(self) -> dict:
    #     pass
    pass


# @dataclass
class TimeWarning:
    """Warning event when participant approaches time limit"""
    # participant_id: str
    # remaining_seconds: int
    # warning_level: str  # "yellow" (50% left), "orange" (25% left), "red" (5% left)
    # timestamp: datetime

    # def to_dict(self) -> dict:
    #     pass
    pass


# @dataclass
class MuteCommand:
    """Command to mute/unmute a participant"""
    # participant_id: str
    # should_mute: bool
    # reason: str  # "time_exhausted", "override", "rule_violation"
    # timestamp: datetime

    # def to_dict(self) -> dict:
    #     pass
    pass


# ─────────────────────────────────────────────────────────────────────
# Interfaces (Domain Contracts)
# ─────────────────────────────────────────────────────────────────────

class AirtimeRepository:  # Protocol
    """Interface for persisting airtime data"""

    # def save_allocation(self, allocation: TimeAllocation) -> None:
    #     pass

    # def get_allocation(self, room_id: str, participant_id: str) -> TimeAllocation | None:
    #     pass

    # def save_session(self, session: SpeakingSession) -> None:
    #     pass

    # def get_sessions(self, room_id: str, participant_id: str) -> list[SpeakingSession]:
    #     pass

    # def get_total_speaking_time(self, room_id: str, participant_id: str) -> int:
    #     """Get total seconds spoken by participant in meeting"""
    #     pass
    pass


class SpeakerTracker:  # Protocol
    """Interface for tracking who is currently speaking (via Jitsi)"""

    # def get_current_speaker(self, room_id: str) -> str | None:
    #     """Return participant_id of current dominant speaker"""
    #     pass

    # def start_tracking(self, room_id: str, participant_id: str) -> None:
    #     """Begin tracking speaking time for participant"""
    #     pass

    # def stop_tracking(self, room_id: str, participant_id: str) -> int:
    #     """Stop tracking and return duration in seconds"""
    #     pass
    pass


class AirtimeBroadcaster:  # Protocol
    """Interface for broadcasting airtime events to clients"""

    # def send_warning(self, room_id: str, warning: TimeWarning) -> None:
    #     """Send time warning to participant"""
    #     pass

    # def send_mute_command(self, room_id: str, command: MuteCommand) -> None:
    #     """Send mute/unmute command to client"""
    #     pass

    # def send_allocation_update(self, room_id: str, allocation: TimeAllocation) -> None:
    #     """Broadcast updated time allocation to all participants"""
    #     pass
    pass


# ─────────────────────────────────────────────────────────────────────
# Services
# ─────────────────────────────────────────────────────────────────────

class AirtimeTracker:
    """Service for tracking speaking time in real-time"""

    # def __init__(
    #     self,
    #     repository: AirtimeRepository,
    #     speaker_tracker: SpeakerTracker,
    #     broadcaster: AirtimeBroadcaster
    # ):
    #     pass

    # def on_speaker_changed(self, room_id: str, previous_speaker: str | None, current_speaker: str | None):
    #     """Handle dominant speaker change event from Jitsi"""
    #     # 1. If previous_speaker exists, stop tracking and save session
    #     # 2. If current_speaker exists, start tracking
    #     # 3. Update allocations
    #     # 4. Check for warnings
    #     # 5. Broadcast updates
    #     pass

    # def check_warnings(self, allocation: TimeAllocation) -> TimeWarning | None:
    #     """Check if participant should receive time warning"""
    #     pass

    # def get_participant_stats(self, room_id: str, participant_id: str) -> dict:
    #     """Get current speaking time statistics for participant"""
    #     pass
    pass


class AllocationCalculator:
    """Service for calculating time allocations based on rules"""

    # def calculate_equal_share(self, meeting_ctx: MeetingContext) -> dict[str, TimeAllocation]:
    #     """Equal share: duration / num_participants"""
    #     pass

    # def calculate_custom_allocation(
    #     self,
    #     meeting_ctx: MeetingContext,
    #     custom_allocations: dict[str, int]
    # ) -> dict[str, TimeAllocation]:
    #     """Custom allocation (e.g., invited speaker gets more time)"""
    #     pass

    # def recalculate_on_participant_join(
    #     self,
    #     room_id: str,
    #     new_participant_id: str
    # ) -> dict[str, TimeAllocation]:
    #     """Recalculate allocations when someone joins mid-meeting"""
    #     pass
    pass


class TimeLendingService:
    """Service for transferring time between participants"""

    # def __init__(
    #     self,
    #     repository: AirtimeRepository,
    #     broadcaster: AirtimeBroadcaster
    # ):
    #     pass

    # def lend_time(
    #     self,
    #     room_id: str,
    #     lender_id: str,
    #     borrower_id: str,
    #     seconds: int
    # ) -> tuple[TimeAllocation, TimeAllocation]:
    #     """Transfer time from lender to borrower"""
    #     # 1. Validate lender has time to lend
    #     # 2. Check lending cap (e.g., max 50% of own allocation)
    #     # 3. Update allocations
    #     # 4. Save to repository
    #     # 5. Broadcast updates
    #     # 6. Return updated allocations
    #     pass

    # def get_lendable_seconds(self, allocation: TimeAllocation, cap_percentage: float = 0.5) -> int:
    #     """Calculate how much time participant can lend"""
    #     pass
    pass
