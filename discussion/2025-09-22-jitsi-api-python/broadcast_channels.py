# yourapp/infrastructure/broadcast_channels.py
"""
Broadcaster adapter using Django Channels groups.
Maps domain broadcast calls to Channels group sends.
"""

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from yourapp.domain.reactions import Broadcaster, ReactionEvent

class ChannelsBroadcaster:  # Broadcaster
    """Channels-backed implementation of Broadcaster."""

    # def __init__(self, channel_layer=None):
    #     self.layer = channel_layer or get_channel_layer()

    def _group(self, room_id):
        """Return main group name for a room."""
        # return f"room:{room_id}"
        return None

    def _facilitators_group(self, room_id):
        """Return facilitators-only group name."""
        # return f"room:{room_id}:facilitators"
        return None

    def _participant_group(self, room_id, participant_id):
        """Return single-participant group name."""
        # return f"room:{room_id}:pid:{participant_id}"
        return None

    def send_to_all(self, room_id, event):  # event: ReactionEvent
        """Broadcast to everyone in the room."""
        # async_to_sync(self.layer.group_send)(..., {"type": "reaction.event", "payload": event.to_dict()})
        return None

    def send_to_participant(self, room_id, participant_id, event):
        """Deliver only to a single participant."""
        # async_to_sync(self.layer.group_send)(..., {"type": "reaction.event", "payload": event.to_dict()})
        return None

    def send_to_facilitators(self, room_id, event):
        """Deliver only to facilitators."""
        # async_to_sync(self.layer.group_send)(..., {"type": "reaction.event", "payload": event.to_dict()})
        return None
