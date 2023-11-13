from datetime import timedelta
import json
import logging

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from authn.models import UserSession
from helpers import get_current_datetime, generate_session_id

logger = logging.getLogger("modle::authn")


@require_http_methods(["POST"])
def create_session(request):
    try:
        body = json.loads(request.body)
    except json.decoder.JSONDecodeError as e:
        logger.error("error decoding json body")
        return JsonResponse(data={"detail": "improper data"}, status=400)

    username = body.get("username")
    password = body.get("password")

    user = authenticate(request, username=username, password=password)
    print(f"user: {user.username}")
    if user is not None:
        print(f"user: {username}=>is_authenticated: {user.is_authenticated}")
        login(request=request, user=user)

        session_id = generate_session_id()
        print(f"session_id: {session_id}")
        user_session = UserSession(
            user_id=user.id,
            session_id=session_id,
            expires_at=get_current_datetime() + timedelta(days=3),
        )
        user_session.save()

        return JsonResponse(data={"token": user_session.session_id}, status=201)

    return JsonResponse(data={"detail": "failure"}, status=401)
