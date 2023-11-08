from authn.models import User


class AuthenticationBackend(object):
    def authenticate(self, request, username, password):
        # this is where the actual authentication code goes into
        pass

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None
