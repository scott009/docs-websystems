# reactions.py
"""
Stubs only. No logic/implementation.
A Django-friendly structure for a 12-reaction system driven by a shared base,
policies, and a registry. UI lives outside the Jitsi iframe; this file focuses
on backend domain objects and orchestration seams (WS/Channels, storage, etc.).
"""

# --- Domain enums / constants (stubs) -----------------------------------------

class VisibilityMode:
    """Enum stub: anonymous | accredited | secret."""
    ANONYMOUS = "anonymous"
    ACCREDITED = "accredited"
    SECRET = "secret"


class ReactionCode:
    """Canonical reaction identifiers (string constants)."""
    LIKE = "like"
    LOVE = "love"
    DISLIKE = "dislike"
    HATE = "hate"
    AGREE = "agree"
    DISAGREE = "disagree"
    GO_ON = "go_on"
    HURRY_UP = "hurry_up"
    BORING = "boring"
    INTERESTING = "interesting"
    SYMPATHY = "sympathy"
    LAUGH = "laugh"


# --- Lightweight value objects (stubs) ----------------------------------------

class ReactionContext:
    """
    Immutable context stub supplied at creation time.
    Includes: room_id, sender_user_id (or session), jitsi_participant_id,
    visibility_mode, target (e.g., 'current_speaker' or explicit pid),
    timestamp, and any request metadata.
    """
    # __init__(...) -> None
    # properties only; no behavior


class RecipientSet:
    """
    Computed recipients (stubs). May include:
      - all_participants
      - speaker_participant_id
      - facilitator_participant_ids
      - others
    """
    # from_room_state(...) -> RecipientSet


class RoomState:
    """
    Server-side snapshot stub: participants, roles, current speaker, etc.
    """
    # fetch(...) -> RoomState


class ReactionEvent:
    """
    Wire/event payload stub ready for dispatch (WS/Channels/DataChannel).
    Fields: code, visibility, payload, sender (per policy), counts, etc.
    """
    # to_dict() -> dict


# --- Service seams / ports (stubs) --------------------------------------------

class Policy:
    """
    Encapsulates anonymity, accreditation, secret visibility, permissions,
    rate limits, and aggregation rules. No implementation here.
    """
    # validate(reaction, room_state) -> None
    # redact_sender(reaction) -> None
    # rate_limit_key(reaction) -> str
    # aggregate_key(reaction) -> str


class Repository:
    """
    Persistence seam (Django ORM under the hood).
    """
    # save_reaction(reaction) -> None
    # increment_counters(reaction) -> None
    # fetch_recent_for_aggregation(key) -> list


class Broadcaster:
    """
    Dispatch seam (e.g., Django Channels, group names).
    """
    # send_to_all(room_id, event: ReactionEvent) -> None
    # send_to_participant(room_id, participant_id, event) -> None
    # send_to_facilitators(room_id, event) -> None


class JitsiDirectory:
    """
    Maps your users <-> Jitsi participant IDs; exposes speaker/facilitator lookup.
    """
    # current_speaker(room_id) -> str | None
    # facilitators(room_id) -> list[str]
    # participant_ids(room_id) -> list[str]


# --- Base class (stubs) -------------------------------------------------------

class BaseReaction:
    """
    Abstract base for all reactions. Concrete subclasses override class-level
    attributes and (optionally) hooks; shared pipeline lives here.
    """
    code: str = "base"
    emoji: str | None = None
    severity: int | None = None  # optional ordering/priority knob

    def __init__(self, ctx: ReactionContext):
        """Store context; do not compute anything yet."""
        # self.ctx = ctx

    # ----- lifecycle hooks (stubs; no logic) -----

    def validate(self, policy: Policy, room_state: RoomState) -> None:
        """Raise on invalid visibility/permissions; enforce per-reaction rules."""
        pass

    def resolve_target(self, directory: JitsiDirectory) -> RecipientSet:
        """
        Compute recipients based on ctx.target + room state (e.g., current speaker).
        Return a RecipientSet; no dispatch here.
        """
        # return RecipientSet()
        pass

    def build_event(self, policy: Policy) -> ReactionEvent:
        """
        Construct the event payload to broadcast, applying anonymity/accreditation.
        Aggregation metadata may be embedded (e.g., window, key).
        """
        # return ReactionEvent()
        pass

    def persist(self, repo: Repository) -> None:
        """Record reaction for analytics/audit; may also maintain counters."""
        pass

    def dispatch(self, recipients: RecipientSet, broadcaster: Broadcaster, event: ReactionEvent) -> None:
        """Fan out to appropriate audiences (all, speaker-only, facilitator-only)."""
        pass

    # ----- optional overrides (stubs) -----

    def extra_policy_checks(self, policy: Policy, room_state: RoomState) -> None:
        """Subclass-specific constraints; default is no-op."""
        pass

    def aggregate_hint(self) -> str | None:
        """Return an aggregation key hint (e.g., code + target) or None."""
        return None


# --- Concrete reactions (stubs; no logic) -------------------------------------

class LikeReaction(BaseReaction):
    code = ReactionCode.LIKE
    emoji = "👍"


class LoveReaction(BaseReaction):
    code = ReactionCode.LOVE
    emoji = "❤️"


class DislikeReaction(BaseReaction):
    code = ReactionCode.DISLIKE
    emoji = "👎"


class HateReaction(BaseReaction):
    code = ReactionCode.HATE
    emoji = "💢"


class AgreeReaction(BaseReaction):
    code = ReactionCode.AGREE
    emoji = "✅"


class DisagreeReaction(BaseReaction):
    code = ReactionCode.DISAGREE
    emoji = "❌"


class GoOnReaction(BaseReaction):
    code = ReactionCode.GO_ON
    emoji = "👉"


class HurryUpReaction(BaseReaction):
    code = ReactionCode.HURRY_UP
    emoji = "⏩"


class BoringReaction(BaseReaction):
    code = ReactionCode.BORING
    emoji = "🥱"


class InterestingReaction(BaseReaction):
    code = ReactionCode.INTERESTING
    emoji = "✨"


class SympathyReaction(BaseReaction):
    code = ReactionCode.SYMPATHY
    emoji = "🤝"


class LaughReaction(BaseReaction):
    code = ReactionCode.LAUGH
    emoji = "😂"


# --- Factory / registry (stubs) -----------------------------------------------

class ReactionFactory:
    """
    Centralized construction from inbound DTOs (WS/HTTP).
    """
    REGISTRY = {
        ReactionCode.LIKE: LikeReaction,
        ReactionCode.LOVE: LoveReaction,
        ReactionCode.DISLIKE: DislikeReaction,
        ReactionCode.HATE: HateReaction,
        ReactionCode.AGREE: AgreeReaction,
        ReactionCode.DISAGREE: DisagreeReaction,
        ReactionCode.GO_ON: GoOnReaction,
        ReactionCode.HURRY_UP: HurryUpReaction,
        ReactionCode.BORING: BoringReaction,
        ReactionCode.INTERESTING: InterestingReaction,
        ReactionCode.SYMPATHY: SympathyReaction,
        ReactionCode.LAUGH: LaughReaction,
    }

    @classmethod
    def from_payload(cls, payload: dict) -> BaseReaction:
        """
        Parse/validate minimal DTO (code, visibility, target, room_id, sender, etc.)
        and return an instance of the appropriate reaction subclass.
        """
        # code = payload["code"]
        # ctx = ReactionContext(...)
        # return cls.REGISTRY[code](ctx)
        pass


# --- Orchestrator (application service) stubs ---------------------------------

class ReactionService:
    """
    High-level pipeline glue. Called by consumer (WS/HTTP view).
    """
    # __init__(policy: Policy, repo: Repository, broadcaster: Broadcaster, directory: JitsiDirectory)

    def handle_submit(self, payload: dict) -> ReactionEvent:
        """
        1) Build reaction via factory.
        2) Fetch room state.
        3) Validate + extra checks.
        4) Persist.
        5) Compute recipients.
        6) Build event.
        7) Dispatch.
        8) Return event for caller (e.g., echo back to sender).
        """
        # reaction = ReactionFactory.from_payload(payload)
        # room_state = RoomState.fetch(...)
        # reaction.validate(self.policy, room_state)
        # reaction.extra_policy_checks(self.policy, room_state)
        # reaction.persist(self.repo)
        # recipients = reaction.resolve_target(self.directory)
        # event = reaction.build_event(self.policy)
        # reaction.dispatch(recipients, self.broadcaster, event)
        # return event
        pass


# --- Django integration seams (stubs) -----------------------------------------

class ChannelsBroadcaster(Broadcaster):
    """
    Channels-based broadcaster stub. Maps room_id to group names.
    """
    # send_to_all(...)
    # send_to_participant(...)
    # send_to_facilitators(...)
    pass


class DjangoRepository(Repository):
    """
    ORM-backed repository stub. Define your models elsewhere or inline here later.
    """
    # save_reaction(...)
    # increment_counters(...)
    # fetch_recent_for_aggregation(...)
    pass


# --- Optional: admin/metrics facades (stubs) ----------------------------------

class ReactionMetrics:
    """
    Read-model facade (per room/speaker/minute counts, histograms, etc.).
    """
    # get_counts(room_id, window) -> dict
    # top_reacted_segments(room_id) -> list
    pass
