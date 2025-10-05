# allocation_rules.py
"""
Stubs only. No logic/implementation.
Different rule implementations for airtime allocation.
Each rule determines how speaking time is distributed among participants.
"""

# from dataclasses import dataclass
# from typing import Protocol
# from airtime import TimeAllocation, MeetingContext

# ─────────────────────────────────────────────────────────────────────
# Base Interface
# ─────────────────────────────────────────────────────────────────────

class AllocationRule:  # Protocol or ABC
    """Base interface for allocation rules"""

    # def calculate_allocations(self, meeting_ctx: MeetingContext) -> dict[str, TimeAllocation]:
    #     """Calculate time allocations for all participants"""
    #     pass

    # def adjust_for_participant_join(
    #     self,
    #     current_allocations: dict[str, TimeAllocation],
    #     new_participant_id: str,
    #     meeting_ctx: MeetingContext
    # ) -> dict[str, TimeAllocation]:
    #     """Adjust allocations when someone joins mid-meeting"""
    #     pass

    # def adjust_for_participant_leave(
    #     self,
    #     current_allocations: dict[str, TimeAllocation],
    #     leaving_participant_id: str,
    #     meeting_ctx: MeetingContext
    # ) -> dict[str, TimeAllocation]:
    #     """Adjust allocations when someone leaves"""
    #     pass

    # @property
    # def name(self) -> str:
    #     """Human-readable name of this rule"""
    #     pass

    # @property
    # def description(self) -> str:
    #     """Description of how this rule works"""
    #     pass
    pass


# ─────────────────────────────────────────────────────────────────────
# Concrete Rule Implementations
# ─────────────────────────────────────────────────────────────────────

class EqualShareRule:  # AllocationRule
    """Each participant gets equal share: duration / num_participants"""

    # def calculate_allocations(self, meeting_ctx: MeetingContext) -> dict[str, TimeAllocation]:
    #     # duration = meeting_ctx.duration_seconds()
    #     # per_person = duration // len(meeting_ctx.participant_ids)
    #     # return {pid: TimeAllocation(pid, per_person) for pid in meeting_ctx.participant_ids}
    #     pass

    # @property
    # def name(self) -> str:
    #     return "Equal Share"

    # @property
    # def description(self) -> str:
    #     return "Each participant receives an equal share of total meeting time"
    pass


class CustomAllocationRule:  # AllocationRule
    """
    Custom allocations set by facilitator.
    Example: invited speaker gets 20 minutes, others get 5 minutes each.
    """

    # def __init__(self, custom_allocations: dict[str, int]):
    #     """custom_allocations: {participant_id: seconds}"""
    #     pass

    # def calculate_allocations(self, meeting_ctx: MeetingContext) -> dict[str, TimeAllocation]:
    #     # Use custom_allocations dict
    #     # For participants not in dict, use default (e.g., remaining_time / remaining_participants)
    #     pass

    # @property
    # def name(self) -> str:
    #     return "Custom Allocation"
    pass


class ProgressiveStackRule:  # AllocationRule
    """
    Progressive Stack: participants who've spoken less get priority/more time.
    Common in activist circles.
    """

    # def __init__(self, base_allocation_seconds: int):
    #     pass

    # def calculate_allocations(self, meeting_ctx: MeetingContext) -> dict[str, TimeAllocation]:
    #     # Base allocation for all
    #     # Bonus time for those who've spoken less
    #     pass

    # def adjust_based_on_usage(
    #     self,
    #     allocations: dict[str, TimeAllocation],
    #     usage_stats: dict[str, int]
    # ) -> dict[str, TimeAllocation]:
    #     """Give more time to those who've used less"""
    #     pass

    # @property
    # def name(self) -> str:
    #     return "Progressive Stack"
    pass


class RoundRobinRule:  # AllocationRule
    """
    Round-robin: each participant gets fixed time slots in rotation.
    Example: 2-minute slots, cycle through all participants.
    """

    # def __init__(self, slot_duration_seconds: int):
    #     pass

    # def calculate_allocations(self, meeting_ctx: MeetingContext) -> dict[str, TimeAllocation]:
    #     # All get same slot duration
    #     # Speaking order managed separately
    #     pass

    # def get_speaking_order(self, participant_ids: list[str]) -> list[str]:
    #     """Return order participants should speak"""
    #     pass

    # @property
    # def name(self) -> str:
    #     return "Round Robin"
    pass


class ReactionBasedRule:  # AllocationRule
    """
    Reaction-based allocation: positive reactions increase time, negative decrease.
    Requires integration with reaction system.
    """

    # def __init__(
    #     self,
    #     base_allocation_seconds: int,
    #     reaction_weights: dict[str, int],  # {"LIKE": +30, "DISLIKE": -15, etc.}
    #     decay_rate: float = 0.9  # Recent reactions matter more
    # ):
    #     pass

    # def calculate_allocations(self, meeting_ctx: MeetingContext) -> dict[str, TimeAllocation]:
    #     # Base allocation for all
    #     pass

    # def adjust_for_reactions(
    #     self,
    #     allocations: dict[str, TimeAllocation],
    #     reaction_scores: dict[str, int]  # {participant_id: score}
    # ) -> dict[str, TimeAllocation]:
    #     """Adjust allocations based on reaction scores"""
    #     # Add/subtract time based on reaction score
    #     # Apply decay (recent reactions weighted higher)
    #     pass

    # @property
    # def name(self) -> str:
    #     return "Reaction-Based Allocation"
    pass


class AdvisoryOnlyRule:  # AllocationRule
    """
    Non-enforcement: just track and report, no actual limits.
    System shows stats but doesn't control speaking.
    """

    # def calculate_allocations(self, meeting_ctx: MeetingContext) -> dict[str, TimeAllocation]:
    #     # Return allocations but mark as advisory
    #     # enforcement_level = EnforcementLevel.ADVISORY
    #     pass

    # def get_usage_report(self, room_id: str) -> dict:
    #     """Generate usage report for advisory display"""
    #     # "Alice has used 120% of expected share"
    #     # "Bob has spoken 10 minutes less than average"
    #     pass

    # @property
    # def name(self) -> str:
    #     return "Advisory Only"
    pass


# ─────────────────────────────────────────────────────────────────────
# Helper Classes
# ─────────────────────────────────────────────────────────────────────

# @dataclass
class RulesetConfig:
    """Configuration for a complete ruleset"""
    # rule: AllocationRule
    # enforcement_level: EnforcementLevel
    # facilitator_override_enabled: bool = True
    # warning_thresholds: dict[str, float] = None  # {"yellow": 0.5, "orange": 0.25, "red": 0.05}

    # def to_dict(self) -> dict:
    #     pass
    pass


class RulesetLibrary:
    """Factory for creating common rulesets"""

    # @staticmethod
    # def equal_share_soft() -> RulesetConfig:
    #     """Equal share with soft enforcement (warnings only)"""
    #     pass

    # @staticmethod
    # def equal_share_hard() -> RulesetConfig:
    #     """Equal share with hard enforcement (auto-mute)"""
    #     pass

    # @staticmethod
    # def progressive_stack() -> RulesetConfig:
    #     """Progressive stack with soft enforcement"""
    #     pass

    # @staticmethod
    # def round_robin(slot_duration: int = 120) -> RulesetConfig:
    #     """Round-robin with specified slot duration"""
    #     pass

    # @staticmethod
    # def advisory_only() -> RulesetConfig:
    #     """No enforcement, stats only"""
    #     pass
    pass
