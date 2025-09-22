# yourapp/apps/reactions/views.py
"""
HTTP view alternative to WS submit, useful for simple integrations or debugging.
Translates HTTP POST JSON into a call to ReactionService.
"""

# from django.views import View
# from django.http import JsonResponse, HttpRequest
# from yourapp.domain.reactions import ReactionService
# from yourapp.infrastructure.repo_django import DjangoRepository
# from yourapp.infrastructure.broadcast_channels import ChannelsBroadcaster
# from yourapp.infrastructure.directory_cache import DirectoryCache
# from yourapp.apps.reactions.policy_impl import DefaultPolicy

class SubmitReactionView:  # View
    """POST /api/reactions"""

    # def post(self, request: HttpRequest):
    #     payload = ...  # parse JSON
    #     service = ReactionService(DefaultPolicy(), DjangoRepository(), ChannelsBroadcaster(), DirectoryCache())
    #     event = service.handle_submit(payload)
    #     return JsonResponse({"ok": True, "event": getattr(event, "to_dict", lambda: {})()})
    pass
