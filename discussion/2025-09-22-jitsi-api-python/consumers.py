# yourapp/apps/reactions/consumers.py
"""
Channels consumer that terminates at the domain service.
Translates WS JSON <-> domain payloads; no business logic here.
"""

# from channels.generic.websocket import AsyncJsonWebsocketConsumer
# from yourapp.domain.reactions import ReactionService
# from yourapp.infrastructure.repo_django import DjangoRepository
# from yourapp.infrastructure.broadcast_channels import ChannelsBroadcaster
# from yourapp.infrastructure.directory_cache import DirectoryCache
# from yourapp.apps.reactions.policy_impl import DefaultPolicy  # your concrete Policy

class ReactionsConsumer:  # AsyncJsonWebsocketConsumer
    """WS endpoint for reaction handshakes and submissions."""

    async def connect(self):
        """Authenticate (if needed), accept, and register presence."""
        # await self.accept()
        # build service with adapters
        # self.service = ReactionService(DefaultPolicy(), DjangoRepository(), ChannelsBroadcaster(), DirectoryCache())
        # await self._register_presence()
        return None

    async def disconnect(self, code):
        """Cleanup presence."""
        # await self._unregister_presence()
        return None

    async def receive_json(self, content, **kwargs):
        """Route messages: 'handshake', 'submit_reaction', 'speaker_update', etc."""
        # kind = content.get("type")
        # if kind == "submit_reaction":
        #     event = self.service.handle_submit(content.get("payload", {}))
        #     await self.send_json({"ok": True, "event": getattr(event, "to_dict", lambda: {})()})
        return None

    async def reaction_event(self, event):
        """Handler for group sends -> forward to client."""
        # await self.send_json({"type": "reaction.event", "payload": event.get("payload")})
        return None
