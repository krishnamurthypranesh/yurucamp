from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from authn.models import User, UserSession


class AuthenticationMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        auth_header = request.headers.get("Authorization")

        if auth_header is None:
            if request.path_info.lstrip("/") not in ["v1/user-sessions/"]:
                return JsonResponse(data={"detail": "Unauthorized"}, status=401)
            else:
                return None

        else:
            _, token = auth_header.split(" ")
            user_session = UserSession.objects.get(session_id=token)
            user = User.objects.get(id=user_session.user_id)

            request.user = user
