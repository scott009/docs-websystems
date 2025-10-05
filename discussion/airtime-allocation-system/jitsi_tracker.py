# jitsi_tracker.py
"""
Stubs only. No logic/implementation.
Infrastructure adapter for tracking Jitsi dominant speaker.
Implements SpeakerTracker interface from airtime.py
"""

# from datetime import datetime
# from django.core.cache import cache
# from airtime import SpeakerTracker  # Interface from domain layer

# ─────────────────────────────────────────────────────────────────────
# Infrastructure Implementation
# ─────────────────────────────────────────────────────────────────────

class CacheSpeakerTracker:  # SpeakerTracker
    """
    Cache-based implementation of SpeakerTracker.
    Uses Redis/Django cache to track current speaker and timing.
    """

    # def __init__(self, cache_backend=None):
    #     # self.cache = cache_backend or cache
    #     pass

    # def get_current_speaker(self, room_id: str) -> str | None:
    #     """Return participant_id of current dominant speaker"""
    #     # return self.cache.get(f"speaker:{room_id}:current")
    #     pass

    # def start_tracking(self, room_id: str, participant_id: str) -> None:
    #     """Begin tracking speaking time for participant"""
    #     # Store current speaker
    #     # self.cache.set(f"speaker:{room_id}:current", participant_id)
    #
    #     # Store start time
    #     # self.cache.set(f"speaker:{room_id}:{participant_id}:start", datetime.now().timestamp())
    #     pass

    # def stop_tracking(self, room_id: str, participant_id: str) -> int:
    #     """Stop tracking and return duration in seconds"""
    #     # start_time = self.cache.get(f"speaker:{room_id}:{participant_id}:start")
    #     # if not start_time: return 0
    #     #
    #     # end_time = datetime.now().timestamp()
    #     # duration = int(end_time - start_time)
    #     #
    #     # Clean up cache
    #     # self.cache.delete(f"speaker:{room_id}:{participant_id}:start")
    #     # if self.cache.get(f"speaker:{room_id}:current") == participant_id:
    #     #     self.cache.delete(f"speaker:{room_id}:current")
    #     #
    #     # return duration
    #     pass

    # def _cache_key_speaker_current(self, room_id: str) -> str:
    #     """Generate cache key for current speaker"""
    #     pass

    # def _cache_key_speaker_start(self, room_id: str, participant_id: str) -> str:
    #     """Generate cache key for speaking start time"""
    #     pass
    pass


# ─────────────────────────────────────────────────────────────────────
# Jitsi Integration Helpers
# ─────────────────────────────────────────────────────────────────────

class JitsiEventHandler:
    """
    Helper class for handling Jitsi iframe API events.
    Maps Jitsi events to SpeakerTracker calls.
    """

    # def __init__(self, speaker_tracker: SpeakerTracker):
    #     pass

    # def on_dominant_speaker_changed(self, room_id: str, participant_id: str | None):
    #     """
    #     Called when Jitsi fires 'dominantSpeakerChanged' event.
    #     Frontend sends this event via WebSocket.
    #     """
    #     # previous_speaker = speaker_tracker.get_current_speaker(room_id)
    #     #
    #     # if previous_speaker:
    #     #     duration = speaker_tracker.stop_tracking(room_id, previous_speaker)
    #     #     # Trigger callback: save session, update allocation
    #     #
    #     # if participant_id:
    #     #     speaker_tracker.start_tracking(room_id, participant_id)
    #     pass

    # def on_participant_joined(self, room_id: str, participant_id: str):
    #     """Called when participant joins meeting"""
    #     pass

    # def on_participant_left(self, room_id: str, participant_id: str):
    #     """Called when participant leaves meeting"""
    #     # If they were speaking, stop tracking
    #     # current_speaker = speaker_tracker.get_current_speaker(room_id)
    #     # if current_speaker == participant_id:
    #     #     speaker_tracker.stop_tracking(room_id, participant_id)
    #     pass
    pass


# ─────────────────────────────────────────────────────────────────────
# WebSocket Consumer Integration (future)
# ─────────────────────────────────────────────────────────────────────

class AirtimeConsumer:  # AsyncJsonWebsocketConsumer
    """
    WebSocket consumer for airtime events.
    Receives Jitsi events from frontend, updates tracking.
    """

    # async def connect(self):
    #     # Accept connection
    #     # Initialize speaker tracker
    #     # self.speaker_tracker = CacheSpeakerTracker()
    #     # self.event_handler = JitsiEventHandler(self.speaker_tracker)
    #     pass

    # async def receive_json(self, content, **kwargs):
    #     """Handle messages from frontend"""
    #     # message_type = content.get("type")
    #     #
    #     # if message_type == "dominant_speaker_changed":
    #     #     room_id = content["room_id"]
    #     #     participant_id = content.get("participant_id")
    #     #     self.event_handler.on_dominant_speaker_changed(room_id, participant_id)
    #     #
    #     # elif message_type == "request_stats":
    #     #     # Send current airtime stats to client
    #     #     pass
    #     pass

    # async def send_warning(self, event):
    #     """Send time warning to client"""
    #     # await self.send_json({
    #     #     "type": "airtime.warning",
    #     #     "payload": event["payload"]
    #     # })
    #     pass

    # async def send_mute_command(self, event):
    #     """Send mute command to client"""
    #     # await self.send_json({
    #     #     "type": "airtime.mute",
    #     #     "payload": event["payload"]
    #     # })
    #     pass
    pass
