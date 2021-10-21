from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class UserIdAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user_id = request.META.get('HTTP_X_USERID')
        if not user_id:
            return None
        try:
            user = User.objects.get(pk=user_id)
            
            # Здесь лучше всего добавить валидацию пароля для предотварщения накрутки, 
            # в HTTP_X_USERID кроме id нужно будет передать и пароль

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
