# yourapp/apps/reactions/policy_impl.py
"""
Concrete Policy implementation.
Encodes visibility rules, permissions, rate-limit keys, and redaction behavior.
"""

# from yourapp.domain.reactions import Policy, VisibilityMode

class DefaultPolicy:  # Policy
    """Production policy for visibility, permissions, rate limiting, and redaction."""

    def validate(self, reaction, room_state):
        """Raise if disallowed (e.g., secret without facilitator role)."""
        # pass
        return None

    def redact_sender(self, reaction_event):
        """Remove PII for anonymous visibility; return modified event."""
        # return reaction_event
        return None

    def rate_limit_key(self, reaction):
        """Return a string key for rate limiting, or None to disable."""
        # return f"rl:{reaction.ctx.room_id}:{reaction.code}:{reaction.ctx.sender_user_id}"
        return None

    def aggregate_key(self, reaction):
        """Return a string key for burst aggregation windows, or None."""
        # return f"agg:{reaction.ctx.room_id}:{reaction.code}:{reaction.ctx.target}"
        return None
